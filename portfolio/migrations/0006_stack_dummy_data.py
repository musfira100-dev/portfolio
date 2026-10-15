
from django.db import migrations

CARDS = [
    dict(
        title="Python/Django", subtitle="Backend", icon="🐍",
        column=1, order=0, side_title="Proficiency",
        show_big_percent=True,
        highlights="Recent: API microservice\nFocus: Scalability",
        chart_type="line", chart_title="Growth",
        chart_values="15,24,22,38,55,80",
        chart_labels="Start,3m,6m,1y,18m,Now",
        rings=[("Python/Django", 80, "2 yrs")]
    ),
    dict(
        title="PostgreSQL", subtitle="Database", icon="🗄️",
        column=1, order=1,
        chart_type="bars", chart_title="Micro-benchmark",
        chart_values="30,45,38,70,52,85",
        chart_labels="Q1,Q2,Q3,Q4,Q5,Q6",
        checklist_title="Complex schema",
        checklist="Indexing strategies\nJoins, views & migrations\nQuery tuning",
        rings=[("PostgreSQL", 88, "2 yrs")]
    ),
    dict(
        title="HTML, CSS, JS", subtitle="Frontend", icon="🌐",
        column=2, order=0,
        checklist_title="Best practices",
        checklist="Semantic, accessible markup\nClean reusable CSS\nMobile-first layouts\nBuilt-in components\nPerformance-minded assets",
        rings=[
            ("HTML", 92, "3 yrs"),
            ("CSS", 90, "3 yrs"),
            ("JavaScript", 70, "2 yrs")
        ]
    ),
    dict(
        title="CSS Frameworks", subtitle="Proficiency in",
        icon="🎨", column=3, order=0,
        rings=[
            ("Bootstrap CSS", 92, "2 yrs"),
            ("Tailwind CSS", 80, "1 yr")
        ]
    ),
    dict(
        title="Redis/Docker", subtitle="Infra", icon="🐳",
        column=3, order=1,
        side_title="Container health",
        chips="🐳, ❤️, ✅, 📦",
        highlights="Focus: Caching & deploys",
        rings=[("Redis / Docker", 82, "2 yrs")]
    ),
]

COMMANDS = [
    (
        "skill_deep_dive",
        "Python/Django  ████████░░  80%\n"
        "PostgreSQL     ████████░░  88%\n"
        "Redis/Docker   ████████░░  82%\n"
        "HTML, CSS, JS  █████████░  90%"
    ),
    (
        "recommend_stack",
        "Backend   -> Django + PostgreSQL\n"
        "Cache     -> Redis\n"
        "Infra     -> Docker\n"
        "Frontend  -> HTML/CSS/JS + Bootstrap"
    ),
    (
        "current_learning",
        "Scaling Django APIs\n"
        "Docker orchestration\n"
        "Advanced PostgreSQL indexing"
    ),
]


def seed(apps, schema_editor):
    Card = apps.get_model("portfolio", "StackCard")
    Ring = apps.get_model("portfolio", "StackRing")
    Cmd = apps.get_model("portfolio", "TerminalCommand")

    if not Card.objects.exists():
        for data in CARDS:
            rings = data.pop("rings")
            card = Card.objects.create(**data)

            for i, (label, pct, cap) in enumerate(rings):
                Ring.objects.create(
                    card=card,
                    label=label,
                    percent=pct,
                    caption=cap,
                    order=i
                )

    if not Cmd.objects.exists():
        for i, (command, output) in enumerate(COMMANDS):
            Cmd.objects.create(
                command=command,
                output=output,
                order=i
            )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0005_stack_section"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
