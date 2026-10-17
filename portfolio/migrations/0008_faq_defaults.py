from django.db import migrations

FAQS = [
    ("What kind of work do you take on?",
     "I design and build complete web products: business websites, portfolios, dashboards, e-commerce stores and custom management systems, from the database and backend to the final interface."),
    ("Which technologies do you use?",
     "My main stack is Python and Django on the backend, with modern HTML, CSS and JavaScript on the front. I pick the simplest tools that fit your project, so it stays fast and easy to maintain."),
    ("How long does a project take?",
     "A simple website usually takes one to two weeks. Larger systems with logins, dashboards or payments take longer. After I understand your requirements, I give you a clear timeline before any work begins."),
    ("How do we get started?",
     "Send me a short message about your idea using the contact form below. We discuss goals, features and budget, I share a plan, and once you approve it, development starts with regular progress updates."),
    ("Do you work with remote and international clients?",
     "Yes. I work remotely and stay in touch through email and chat, so location is never a problem."),
    ("Do you offer support after launch?",
     "Yes. I help with deployment, fixes and updates after launch, and can keep maintaining the project as it grows."),
]


def add_faqs(apps, schema_editor):
    FAQ = apps.get_model("portfolio", "FAQ")
    if FAQ.objects.exists():
        return
    for i, (question, answer) in enumerate(FAQS):
        FAQ.objects.create(question=question, answer=answer, order=i)


def remove_faqs(apps, schema_editor):
    FAQ = apps.get_model("portfolio", "FAQ")
    FAQ.objects.filter(question__in=[q for q, _ in FAQS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0007_faq"),
    ]

    operations = [
        migrations.RunPython(add_faqs, remove_faqs),
    ]
    