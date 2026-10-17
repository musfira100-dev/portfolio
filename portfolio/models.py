from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SiteProfile(models.Model):
    """Poori site ki general settings (sirf ek record, admin se edit hota hai)."""

    page_title = models.CharField("Browser tab title", max_length=150,
                                  default="ALEXANDER VANCE // CREATIVE DIGITAL ARCHITECT")
    hero_image = models.ImageField("Hero photo", upload_to="hero/", blank=True)
    resume = models.FileField("Resume (PDF)", upload_to="resume/", blank=True,
                          help_text="PDF upload karein — navbar mein 'Resume' button isi se banta hai.")
    name = models.CharField(max_length=80, default="ALEXANDER VANCE",
                            help_text="Pehla lafz hero mein bara, doosra outline mein dikhta hai.")
    tagline = models.CharField(max_length=120, default="CREATIVE SYSTEM ARCHITECT")
    hero_keywords = models.CharField(max_length=200,
                                     default="PYTHON • DJANGO • FRONTEND GRAPHICS • SYSTEM DESIGN")
    status_tag = models.CharField(max_length=120, default="AVAILABLE FOR SELECT COMMISSIONS")
    design_philosophy = models.CharField(max_length=200,
                                         default="Bespoke Architectural Engineering & High-Performance UI")

    bio = models.TextField("Manifesto headline",
                           default="I BUILD DIGITAL EXPERIENCES THAT TURN BOLD IDEAS INTO MEMORABLE INTERACTIONS.")
    manifesto_quote = models.TextField(
        default="Where robust Python/Django system architecture meets fluid, art-directed frontend canvas mechanics.")
    manifesto_text = models.TextField(
        default="A complete departure from generic cards and prefabricated templates. Every project is built as a "
                "custom digital experience tailored to convey exact identity, visual clarity, and technical excellence.")
    manifesto_tags = models.CharField(
        max_length=250,
        default="DJANGO REST • GSAP ANIMATION ENGINE • WEBGL CANVAS • TAILWIND ARCHITECTURE")

    email = models.EmailField(default="alexander@vance.digital")
    github_url = models.URLField(blank=True, default="https://github.com")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com")
    twitter_url = models.URLField("X / Twitter URL", blank=True, default="https://twitter.com")
    facebook_url = models.URLField("Facebook URL", blank=True, default="")
    instagram_url = models.URLField("Instagram URL", blank=True, default="")

    latitude = models.FloatField(default=37.7749, help_text="Header mein LAT dikhta hai.")
    longitude = models.FloatField(default=-122.4194, help_text="Header mein LNG dikhta hai.")

    stat_years = models.PositiveIntegerField("Years in development", default=4)
    stat_projects = models.PositiveIntegerField("Projects shipped", default=24)
    stat_uptime = models.PositiveIntegerField("Architectural reliability %", default=99)
    stat_commits = models.PositiveIntegerField("Commits logged", default=1800)

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1  # hamesha ek hi record
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class _ImageMixin(models.Model):
    image = models.ImageField(upload_to="uploads/", blank=True,
                              help_text="Image upload karein, YA neeche image URL daalein.")
    image_url = models.URLField(max_length=500, blank=True)

    class Meta:
        abstract = True

    @property
    def image_src(self):
        if self.image:
            return self.image.url
        return self.image_url


class Project(_ImageMixin):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=150, help_text="E.g. FULL STACK / PYTHON & DJANGO")
    description = models.TextField()
    stack = models.CharField(max_length=250, help_text="E.g. Python, Django, Redis")
    year_label = models.CharField("Year // client", max_length=120, help_text="E.g. 2025 // CREATIVE AI LABS")
    link = models.CharField("Live link", max_length=500, blank=True, default="#")
    order = models.PositiveIntegerField(default=0, db_index=True, help_text="Chota number pehle dikhta hai.")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Service(_ImageMixin):
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=40, help_text="Backend, Frontend, Database, Graphics, Infra, APIs ...")
    level = models.PositiveIntegerField(default=80, validators=[MaxValueValidator(100)])
    experience = models.CharField(max_length=30, default="1 Yrs")
    x = models.FloatField("Position X", default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)],
                          help_text="0 se 1 tak (0 = left, 1 = right)")
    y = models.FloatField("Position Y", default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)],
                          help_text="0 se 1 tak (0 = top, 1 = bottom)")
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name
    

    
def _csv(value):
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def _lines(value):
    return [v.strip() for v in (value or "").splitlines() if v.strip()]


class StackCard(models.Model):
    """Landing page ke Command the Stack section ka card."""

    COLUMNS = [(1, "Left"), (2, "Middle"), (3, "Right")]
    CHARTS = [
        ("none", "No chart"),
        ("line", "Growth line"),
        ("bars", "Bar chart"),
    ]

    title = models.CharField(max_length=80, help_text="E.g. Python/Django")
    subtitle = models.CharField(max_length=80, blank=True)
    icon = models.CharField(max_length=8, blank=True)
    column = models.PositiveSmallIntegerField(choices=COLUMNS, default=1)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_published = models.BooleanField(default=True)

    side_title = models.CharField(max_length=60, blank=True)
    show_big_percent = models.BooleanField(default=False)
    highlights = models.TextField(blank=True)
    chips = models.CharField(max_length=200, blank=True)

    chart_type = models.CharField(
        max_length=8, choices=CHARTS, default="none"
    )
    chart_title = models.CharField(max_length=60, blank=True)
    chart_values = models.CharField(max_length=200, blank=True)
    chart_labels = models.CharField(max_length=200, blank=True)

    checklist_title = models.CharField(max_length=60, blank=True)
    checklist = models.TextField(blank=True)

    class Meta:
        ordering = ["column", "order", "id"]
        verbose_name = "Stack card"
        verbose_name_plural = "Stack cards"

    def __str__(self):
        return self.title

    @property
    def ring_list(self):
        return list(self.rings.all())

    @property
    def ring_count(self):
        return len(self.ring_list)

    @property
    def first_percent(self):
        rings = self.ring_list
        return rings[0].percent if rings else 0

    @property
    def highlight_pairs(self):
        result = []
        for line in _lines(self.highlights):
            key, _, value = line.partition(":")
            result.append(
                (key.strip(), value.strip()) if value else ("", key.strip())
            )
        return result

    @property
    def chip_list(self):
        return _csv(self.chips)

    @property
    def checklist_items(self):
        return _lines(self.checklist)

    @property
    def nums(self):
        result = []
        for value in _csv(self.chart_values):
            try:
                result.append(float(value))
            except ValueError:
                pass
        return result

    @property
    def label_list(self):
        return _csv(self.chart_labels)

    @property
    def bars_in_side(self):
        return (
            self.chart_type == "bars"
            and self.ring_count == 1
            and bool(self.nums)
        )

    @property
    def show_side(self):
        return bool(
            self.side_title
            or self.highlights.strip()
            or self.chips.strip()
            or self.show_big_percent
            or self.bars_in_side
        )

    @property
    def bars(self):
        numbers = self.nums
        if not numbers:
            return []

        maximum = max(numbers) or 1
        labels = self.label_list

        return [
            {
                "h": max(8, round(value / maximum * 100)),
                "label": labels[i] if i < len(labels) else "",
            }
            for i, value in enumerate(numbers)
        ]

    def _line_points(self):
        numbers = self.nums
        if len(numbers) < 2:
            return []

        minimum = min(numbers)
        maximum = max(numbers)
        span = (maximum - minimum) or 1
        step = 200 / (len(numbers) - 1)

        return [
            (
                round(i * step, 2),
                round(52 - (value - minimum) / span * 44, 2),
            )
            for i, value in enumerate(numbers)
        ]

    @property
    def line_path(self):
        points = self._line_points()
        if not points:
            return ""

        path = f"M{points[0][0]},{points[0][1]}"

        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            middle_x = round((x0 + x1) / 2, 2)
            path += (
                f" C{middle_x},{y0} "
                f"{middle_x},{y1} {x1},{y1}"
            )

        return path

    @property
    def area_path(self):
        return f"{self.line_path} L200,60 L0,60 Z" if self.line_path else ""

    @property
    def show_line(self):
        return self.chart_type == "line" and bool(self.line_path)

    @property
    def show_bars_below(self):
        return (
            self.chart_type == "bars"
            and not self.bars_in_side
            and bool(self.bars)
        )


class StackRing(models.Model):
    """StackCard ke andar progress ring."""

    card = models.ForeignKey(
        StackCard,
        on_delete=models.CASCADE,
        related_name="rings",
    )
    label = models.CharField(max_length=60)
    percent = models.PositiveIntegerField(
        default=80,
        validators=[MaxValueValidator(100)],
    )
    caption = models.CharField(max_length=40, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label} {self.percent}%"


class TerminalCommand(models.Model):
    """Landing page terminal commands aur unka output."""

    command = models.CharField(max_length=40, unique=True)
    output = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Terminal command"
        verbose_name_plural = "Terminal commands"

    def __str__(self):
        return self.command



class TimelineEntry(models.Model):
    year = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Timeline entries"

    def __str__(self):
        return f"{self.year} — {self.title}"

class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
