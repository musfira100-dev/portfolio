"""Dummy data (local images ke saath). Dobara chalane se kuch duplicate nahi hota:
sirf khali jagah bharta hai aur Unsplash/khali images ko local images se badalta hai."""
import random
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from portfolio.models import ContactMessage, Project, Service, SiteProfile, Skill, TimelineEntry

PALETTES = [  # (bg top, bg bottom, accent 1, accent 2)
    ((8, 20, 36), (10, 60, 90), (0, 240, 255), (60, 120, 255)),
    ((14, 16, 10), (40, 56, 10), (212, 255, 0), (0, 200, 120)),
    ((30, 14, 16), (90, 30, 34), (230, 200, 150), (255, 120, 90)),
    ((18, 10, 38), (60, 24, 90), (190, 110, 255), (255, 90, 170)),
    ((6, 24, 22), (10, 80, 70), (0, 255, 157), (114, 239, 221)),
    ((36, 14, 6), (110, 44, 12), (255, 183, 3), (255, 77, 77)),
]

PROJECTS = [
    ("NEURAL CANVAS PLATFORM", "FULL STACK / PYTHON & DJANGO",
     "An AI-driven real-time canvas generator backended by Django REST framework, PostgreSQL, Redis channels, and WebGL rendering shaders.",
     "Python, Django, Redis, Three.js, Tailwind", "2025 // CREATIVE AI LABS"),
    ("FINTECH ALGO DASHBOARD", "API ENGINEERING & DATA VISUALIZATION",
     "High-frequency quantitative analytics web portal processing microsecond market feeds via WebSocket Django Channels.",
     "Django REST, PostgreSQL, React, D3.js", "2024 // QUANT CAPITAL"),
    ("AETHERIA CREATIVE ARCHIVE", "EDITORIAL DIGITAL EXPERIENCE",
     "Award-nominated digital architecture exhibition space featuring fluid GLSL shaders and smooth scroll velocity interactions.",
     "GSAP, WebGL, Tailwind, Python Backend", "2024 // AETHERIA"),
    ("SYNTHETIC VOICE ENGINE", "SYSTEM ENGINE & AI PLATFORM",
     "Bespoke speech synthesis API interface with Django custom model routing and latency-optimized dynamic queues.",
     "Python, FastAPI, Django Admin, React", "2023 // VOICE LABS"),
    ("ORBIT E-COMMERCE SUITE", "FULL STACK / COMMERCE",
     "Headless storefront with a Django admin back office, Stripe payments, inventory sync and a blazing-fast React catalogue.",
     "Django, PostgreSQL, Stripe, React", "2023 // ORBIT RETAIL"),
    ("PULSE HEALTH TRACKER", "MOBILE-FIRST WEB APP",
     "Privacy-first wellness tracker with offline sync, encrypted records and clean visual dashboards for daily habits.",
     "Django REST, Celery, Chart.js, PWA", "2022 // PULSE STUDIO"),
]
SERVICES = [
    ("FULL STACK DEVELOPMENT", "End-to-end design and implementation of Django backend systems coupled with state-of-the-art frontend UI experiences."),
    ("PYTHON / DJANGO ENGINEERING", "Scalable REST APIs, custom ORM query optimization, caching strategies with Redis, and robust security protocols."),
    ("API ENGINEERING", "High-throughput REST and GraphQL endpoints optimized for low-latency client consumers."),
    ("FRONTEND ENGINEERING", "Awwwards-level creative direction utilizing GSAP, Canvas APIs, smooth scroll velocity physics, and bespoke typography."),
    ("DATABASE SYSTEMS", "PostgreSQL database design, indexing strategies, Docker containerization, and cloud deployment pipelines."),
    ("UI / UX DESIGN", "Interface concepts, design systems and interactive prototypes that stay faithful from Figma to production."),
]
SKILLS = [
    ("Python / Django", "Backend", 95, "4 Yrs", 0.30, 0.40), ("React / Next.js", "Frontend", 90, "3 Yrs", 0.70, 0.30),
    ("PostgreSQL / ORM", "Database", 88, "4 Yrs", 0.20, 0.70), ("WebGL / GSAP", "Graphics", 85, "2 Yrs", 0.80, 0.70),
    ("Redis / Docker", "Infra", 82, "3 Yrs", 0.50, 0.80), ("REST / GraphQL", "APIs", 94, "4 Yrs", 0.50, 0.20),
    ("Tailwind CSS", "Frontend", 92, "3 Yrs", 0.88, 0.45), ("Celery / RabbitMQ", "Backend", 78, "2 Yrs", 0.12, 0.30),
    ("Git / CI-CD", "Infra", 86, "4 Yrs", 0.65, 0.88), ("Figma / Design", "Graphics", 80, "2 Yrs", 0.35, 0.85),
]
TIMELINE = [
    ("2023", "System Architecture & Python Foundations", "Mastered Python core internals, Django ORM, REST principles, and database indexing."),
    ("2024", "Full-Stack Web Orchestration", "Built enterprise-grade Django API systems, paired with rich React frontend states & GLSL canvas mechanics."),
    ("2025", "High-Performance Interactive Systems", "Architecting award-level digital experiences, WebGL creative direction, and high-load backend pipelines."),
    ("2026", "Senior Digital Architect", "Leading creative web engineering commissions and bespoke digital art direction."),
    ("NEXT", "Open Source & Mentoring", "Publishing reusable Django packages and mentoring early-career developers."),
]


def make_art(path, size, idx):
    """Local abstract artwork (internet ki zaroorat nahi)."""
    from PIL import Image, ImageDraw, ImageFilter
    rnd = random.Random(idx * 97 + 13)
    pal = PALETTES[idx % len(PALETTES)]
    w, h = size
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    for y in range(h):
        k = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(pal[0][c] * (1 - k) + pal[1][c] * k) for c in range(3)))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for _ in range(4):
        r = rnd.randint(h // 5, h // 2)
        x, y = rnd.randint(0, w), rnd.randint(0, h)
        g.ellipse((x - r, y - r, x + r, y + r), fill=pal[2 + rnd.randint(0, 1)] + (150,))
    glow = glow.filter(ImageFilter.GaussianBlur(h // 7))
    img = Image.alpha_composite(base.convert("RGBA"), glow)
    over = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    o = ImageDraw.Draw(over)
    step, lw = w // 12, max(2, w // 400)
    for x in range(0, w, step):
        o.line([(x, 0), (x, h)], fill=(255, 255, 255, 18))
    for y in range(0, h, step):
        o.line([(0, y), (w, y)], fill=(255, 255, 255, 18))
    cx, cy, R = int(w * rnd.uniform(.55, .75)), int(h * rnd.uniform(.32, .5)), int(h * .27)
    o.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(255, 255, 255, 130), width=lw)
    o.ellipse((cx - R // 2, cy - R // 2, cx + R // 2, cy + R // 2), fill=pal[2] + (210,))
    x0, y0, x1, y1 = int(w * .08), int(h * .6), int(w * .46), int(h * .86)
    o.rounded_rectangle((x0, y0, x1, y1), radius=h // 30, outline=(255, 255, 255, 150), width=lw, fill=(255, 255, 255, 28))
    for n, frac in enumerate((.8, .55, .7)):
        yy = y0 + (y1 - y0) * (.22 + .24 * n)
        o.rounded_rectangle((x0 + w * .03, yy, x0 + w * .03 + (x1 - x0 - w * .06) * frac, yy + h * .02),
                            radius=h // 80, fill=(255, 255, 255, 120))
    o.line([(int(w * .08), int(h * .12)), (int(w * .3), int(h * .12))], fill=pal[2] + (255,), width=lw * 2)
    Image.alpha_composite(img, over).convert("RGB").save(path, "JPEG", quality=86)


def art(kind, idx, size):
    rel = f"dummy/{kind}-{idx + 1}.jpg"
    full = Path(settings.MEDIA_ROOT) / rel
    if not full.exists():
        full.parent.mkdir(parents=True, exist_ok=True)
        make_art(full, size, idx + (0 if kind == "project" else 3))
    return rel


def needs_art(obj):
    return not obj.image and (not obj.image_url or "unsplash.com" in obj.image_url)


class Command(BaseCommand):
    help = "Dummy data + local dummy images (safe to re-run)."

    def handle(self, *args, **opts):
        SiteProfile.load()

        # Projects
        existing = list(Project.objects.all())
        titles = {p.title for p in existing}
        for i, (t, c, d, s, y) in enumerate(PROJECTS):
            if len(existing) + 0 >= len(PROJECTS) and t not in titles:
                continue
            if t not in titles:
                existing.append(Project.objects.create(title=t, category=c, description=d, stack=s, year_label=y, order=i))
        for i, p in enumerate(Project.objects.all()):
            if needs_art(p):
                p.image.name = art("project", i, (1200, 800)); p.image_url = ""; p.save()

        # Services
        existing = list(Service.objects.all())
        titles = {s.title for s in existing}
        for i, (t, d) in enumerate(SERVICES):
            if len(existing) >= len(SERVICES) and t not in titles:
                continue
            if t not in titles:
                existing.append(Service.objects.create(title=t, description=d, order=i))
        for i, s in enumerate(Service.objects.all()):
            if needs_art(s):
                s.image.name = art("service", i, (900, 675)); s.image_url = ""; s.save()

        # Skills / Timeline (top-up)
        names = set(Skill.objects.values_list("name", flat=True))
        if Skill.objects.count() < len(SKILLS):
            for i, (n, c, l, e, x, y) in enumerate(SKILLS):
                if n not in names:
                    Skill.objects.create(name=n, category=c, level=l, experience=e, x=x, y=y, order=i)
        years = set(TimelineEntry.objects.values_list("year", flat=True))
        if TimelineEntry.objects.count() < len(TIMELINE):
            for i, (y, t, x) in enumerate(TIMELINE):
                if y not in years:
                    TimelineEntry.objects.create(year=y, title=t, text=x, order=i)

        if not ContactMessage.objects.exists():
            m = ContactMessage.objects.create(
                name="SOPHIA CHEN", email="sophia@nexus.io",
                message="Interested in hiring for custom digital architecture commission.")
            ContactMessage.objects.filter(pk=m.pk).update(created_at="2026-10-02T10:00:00Z")

        self.stdout.write(self.style.SUCCESS(
            f"Ready: {Project.objects.count()} projects, {Service.objects.count()} services, "
            f"{Skill.objects.count()} skills, {TimelineEntry.objects.count()} timeline entries."))
