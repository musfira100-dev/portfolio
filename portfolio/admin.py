
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ContactMessage,
    FAQ,
    Project,
    Service,
    SiteProfile,
    Skill,
    StackCard,
    StackRing,
    TerminalCommand,
    TimelineEntry,
)

admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Portfolio content manager"


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": (
            "page_title", "name", "tagline", "hero_keywords",
            "status_tag", "design_philosophy", "hero_image", "resume"
        )}),
        ("Manifesto", {"fields": (
            "bio", "manifesto_quote", "manifesto_text", "manifesto_tags"
        )}),
        ("Contact & social", {"fields": (
            "email", "github_url", "linkedin_url", "facebook_url",
            "instagram_url", "twitter_url"
        )}),
        ("Header coordinates", {"fields": ("latitude", "longitude")}),
        ("Stats counters", {"fields": (
            "stat_years", "stat_projects", "stat_uptime", "stat_commits"
        )}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        obj = SiteProfile.load()
        return redirect("admin:portfolio_siteprofile_change", obj.pk)


class ThumbMixin:
    @admin.display(description="Preview")
    def thumb(self, obj):
        if obj.image_src:
            return format_html(
                '<img src="{}" style="height:44px;border-radius:4px">',
                obj.image_src
            )
        return "—"


@admin.register(Project)
class ProjectAdmin(ThumbMixin, admin.ModelAdmin):
    list_display = (
        "title", "thumb", "category", "year_label", "order", "is_published"
    )
    list_editable = ("order", "is_published")
    search_fields = ("title", "category", "stack")


@admin.register(Service)
class ServiceAdmin(ThumbMixin, admin.ModelAdmin):
    list_display = ("title", "thumb", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "level", "experience", "x", "y", "order"
    )
    list_editable = ("level", "x", "y", "order")


class StackRingInline(admin.TabularInline):
    model = StackRing
    extra = 1
    max_num = 3


@admin.register(StackCard)
class StackCardAdmin(admin.ModelAdmin):
    list_display = (
        "title", "subtitle", "column", "order", "is_published"
    )
    list_editable = ("column", "order", "is_published")
    inlines = [StackRingInline]

    fieldsets = (
        ("Card", {"fields": (
            "title", "subtitle", "icon", "column", "order", "is_published"
        )}),
        ("Side info (ring ke saath)", {"fields": (
            "side_title", "show_big_percent", "highlights", "chips"
        )}),
        ("Chart (optional)", {"fields": (
            "chart_type", "chart_title", "chart_values", "chart_labels"
        )}),
        ("Checklist (optional)", {"fields": (
            "checklist_title", "checklist"
        )}),
    )


@admin.register(TerminalCommand)
class TerminalCommandAdmin(admin.ModelAdmin):
    list_display = ("command", "order")
    list_editable = ("order",)


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ("year", "title", "order")
    list_editable = ("order",)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_published")
    list_editable = ("order", "is_published")
    search_fields = ("question", "answer")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")
    actions = ["mark_read"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
