import json

from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import (
    ContactMessage,
    Project,
    Service,
    SiteProfile,
    Skill,
    StackCard,
    TerminalCommand,
    TimelineEntry,
)


def _stats(p):
    return [
        ("Experience", p.stat_years, "+", "Years in development"),
        ("Production work", p.stat_projects, "+", "Projects shipped"),
        ("System uptime", p.stat_uptime, "%", "Architectural reliability"),
        ("Commits logged", p.stat_commits, "+", "Git repository logs"),
    ]


def _stack():
    cards = list(
        StackCard.objects.filter(is_published=True).prefetch_related("rings")
    )
    commands = list(TerminalCommand.objects.all())
    cols = []

    for n in (1, 2, 3):
        column_cards = [card for card in cards if card.column == n]
        has_terminal = n == 2 and bool(commands)

        if column_cards or has_terminal:
            cols.append({
                "cards": column_cards,
                "terminal": has_terminal,
                "mid": n == 2,
            })

    return cols, [
        {"cmd": command.command, "out": command.output}
        for command in commands
    ]



def index(request):
    p = SiteProfile.load()
    parts = p.name.split()
    groups = {}
    stack_cols, terminal_cmds = _stack()
    for s in Skill.objects.all():
        groups.setdefault(s.category, []).append(s)
    return render(request, "portfolio/index.html", {
        "profile": p,
         "stack_cols": stack_cols,
        "terminal_cmds": terminal_cmds,
        "terminal_names": ", ".join(c["cmd"] for c in terminal_cmds),
        "hero_image": p.hero_image.url if p.hero_image else "",
        "name_first": parts[0] if parts else "",
        "name_second": " ".join(parts[1:]),
        "initials": "".join(w[0] for w in parts[:2]).upper(),
        "tags": [t.strip() for t in p.manifesto_tags.split("•") if t.strip()],
        "entries": TimelineEntry.objects.all(),
        "groups": list(groups.items()),
        "services": list(enumerate(Service.objects.filter(is_published=True), 1)),
        "projects": list(enumerate(Project.objects.filter(is_published=True), 1)),
        "stats": _stats(p),
        "keywords": [k.strip() for k in p.hero_keywords.split("•") if k.strip()],
        "marquee": [k.strip() for k in p.hero_keywords.split("•") if k.strip()] + [s.name for s in Skill.objects.all()],
        "show_cms_button": getattr(settings, "SHOW_CMS_BUTTON", True),
    })


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message")


@require_POST
def contact(request):
    ip = request.META.get("REMOTE_ADDR", "unknown")
    key = f"contact:{ip}"
    if cache.get(key, 0) >= 5:  # 5 messages / ghanta / IP
        return JsonResponse({"ok": False, "error": "Too many messages. Try later."}, status=429)

    try:
        data = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

    form = ContactForm(data)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    msg = form.save()
    cache.set(key, cache.get(key, 0) + 1, 3600)

    try:
        EmailMessage(
            subject=f"Portfolio message from {msg.name}",
            body=f"Name: {msg.name}\nEmail: {msg.email}\n\n{msg.message}",
            to=[settings.CONTACT_NOTIFY_EMAIL],
            reply_to=[msg.email],
        ).send()
    except Exception:
        pass  # mail fail ho to bhi form chalta rahe, message database mein save hai

    return JsonResponse({"ok": True})


# ---------------------------------------------------------------------------
# Alag (inner) pages — landing page ke har section ka apna page
# ---------------------------------------------------------------------------
PAGES = [  # (url name, number, label)
    ("about", "02", "Manifesto"),
    ("timeline", "03", "Timeline"),
    ("skills", "04", "Skills"),
    ("services", "05", "Services"),
    ("projects", "06", "Work"),
    ("stats", "08", "Metrics"),
    ("contact_page", "10", "Contact"),
]


def _page(request, template, current, **extra):
    names = [n for n, _, _ in PAGES]
    idx = names.index(current)
    nxt = PAGES[(idx + 1) % len(PAGES)]
    ctx = {
        "profile": SiteProfile.load(),
        "nav": [{"url": reverse(f"portfolio:{n}"), "num": num, "label": label, "active": n == current}
                for n, num, label in PAGES],
        "page_num": PAGES[idx][1],
        "page_label": PAGES[idx][2],
        "next_page": {"url": reverse(f"portfolio:{nxt[0]}"), "label": nxt[2], "num": nxt[1]},
    }
    ctx.update(extra)
    return render(request, f"portfolio/pages/{template}.html", ctx)


def about(request):
    p = SiteProfile.load()
    tags = [t.strip() for t in p.manifesto_tags.split("•") if t.strip()]
    return _page(request, "about", "about", tags=tags)


def timeline(request):
    return _page(request, "timeline", "timeline", entries=TimelineEntry.objects.all())


def skills(request):
    groups = {}
    for s in Skill.objects.all():
        groups.setdefault(s.category, []).append(s)
    return _page(request, "skills", "skills", groups=list(groups.items()))


def services(request):
    return _page(request, "services", "services",
                 items=list(enumerate(Service.objects.filter(is_published=True), 1)))


def projects(request):
    return _page(request, "projects", "projects",
                 items=list(enumerate(Project.objects.filter(is_published=True), 1)))


def project_detail(request, pk):
    qs = list(Project.objects.filter(is_published=True))
    proj = get_object_or_404(Project, pk=pk, is_published=True)
    i = qs.index(proj)
    return _page(request, "project_detail", "projects", project=proj, num=f"{i + 1:02d}",
                 stack=[t.strip() for t in proj.stack.split(",") if t.strip()],
                 prev_project=qs[i - 1] if i > 0 else None,
                 next_project=qs[i + 1] if i < len(qs) - 1 else None)


def stats(request):
    return _page(request, "stats", "stats", items=_stats(SiteProfile.load()))


def contact_page(request):
    return _page(request, "contact", "contact_page")
