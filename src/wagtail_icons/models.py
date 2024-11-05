from django.db import models
from django.utils.safestring import mark_safe
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import Column
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


class Icon(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    svg = models.TextField()
    provider = models.CharField(max_length=255)
    style = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    aliases = models.CharField(max_length=511, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("label"),
        FieldPanel("svg"),
        FieldPanel("provider"),
        FieldPanel("style"),
        FieldPanel("is_deleted"),
        FieldPanel("aliases"),
    ]

    search_fields = [
        index.AutocompleteField("name"),
        index.AutocompleteField("label"),
        index.AutocompleteField("aliases"),
        index.FilterField("provider"),
        index.FilterField("style"),
        index.FilterField("is_deleted"),
    ]

    class Meta:
        unique_together = ("name", "provider", "style")
        indexes = [
            models.Index(fields=["name", "provider", "style"]),
            models.Index(fields=["provider", "style"]),
        ]

    def __str__(self):
        return f"{self.provider} - {self.name} ({self.style})"


class IconFilterSet(WagtailFilterSet):
    class Meta:
        model = Icon
        fields = ["provider", "style"]


class IconSvgColumn(Column):
    def __init__(self, **kwargs):
        super().__init__(
            "svg",
            label="SVG",
        )

    def get_value(self, instance):
        return instance.svg

    def render_cell_html(self, instance, parent_context):
        return mark_safe(
            f"<td><div class='icon' style='width: 20px; height: 20px;'>{instance.svg}</div></td>"
        )


class IconViewSet(SnippetViewSet):
    model = Icon
    filterset_class = IconFilterSet
    list_display = [
        "name",
        IconSvgColumn(),
        "provider",
        "style",
    ]


register_snippet(IconViewSet)
