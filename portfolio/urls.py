from django.urls import path

from . import views

app_name = "portfolio"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("timeline/", views.timeline, name="timeline"),
    path("skills/", views.skills, name="skills"),
    path("services/", views.services, name="services"),
    path("projects/", views.projects, name="projects"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("stats/", views.stats, name="stats"),
    path("contact/", views.contact_page, name="contact_page"),
]
