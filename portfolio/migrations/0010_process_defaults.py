from django.db import migrations

STEPS = [
    ("Planning", "🧭",
     "We define the goals, audience and features, and agree on scope, timeline and budget before a single line of code is written.",
     "Requirements gathering\nScope and timeline\nProject roadmap"),
    ("Design", "🎨",
     "Wireframes and visual design turn the plan into a clear, modern interface that you can review and approve.",
     "Wireframes\nUI design\nDesign approval"),
    ("Development", "💻",
     "The product is built in small working increments: a clean backend, a responsive front end and regular progress updates.",
     "Backend and database\nResponsive interface\nProgress updates"),
    ("Testing", "🧪",
     "Every feature is checked on real devices and edge cases, so bugs are caught long before your users see them.",
     "Functional testing\nCross-device checks\nBug fixing"),
    ("Review", "🔍",
     "You go through the working product and share feedback, and we refine it until everything matches your expectations.",
     "Client feedback\nRevisions\nFinal sign-off"),
    ("Deploy", "🚀",
     "The project goes live on a secure, optimised server with your domain, HTTPS and backups all configured.",
     "Server setup\nDomain and HTTPS\nGo-live"),
    ("Monitoring & Maintenance", "🛠️",
     "After launch I keep an eye on performance and uptime, fix issues quickly and ship updates as your needs grow.",
     "Uptime monitoring\nSecurity updates\nNew features"),
]


def add_steps(apps, schema_editor):
    ProcessStep = apps.get_model("portfolio", "ProcessStep")
    if ProcessStep.objects.exists():
        return
    for i, (title, icon, description, points) in enumerate(STEPS):
        ProcessStep.objects.create(
            title=title, icon=icon, description=description, points=points, order=i,
        )


def remove_steps(apps, schema_editor):
    ProcessStep = apps.get_model("portfolio", "ProcessStep")
    ProcessStep.objects.filter(title__in=[s[0] for s in STEPS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0009_processstep"),
    ]

    operations = [
        migrations.RunPython(add_steps, remove_steps),
    ]