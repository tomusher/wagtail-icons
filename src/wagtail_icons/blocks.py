from wagtail.snippets.blocks import SnippetChooserBlock

from wagtail_icons.models import Icon


class IconChooserBlock(SnippetChooserBlock):
    icon = "pick"

    def __init__(self, **kwargs):
        super().__init__(Icon, **kwargs)
