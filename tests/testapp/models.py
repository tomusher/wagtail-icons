from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_icons import blocks


class ExamplePage(Page):
    body = StreamField(
        [
            ("heading", blocks.IconChooserBlock()),
        ],
        blank=True,
    )

    content_panels = [*Page.content_panels, FieldPanel("body")]
