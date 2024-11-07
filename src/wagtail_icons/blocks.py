from wagtail_icons.views import icon_chooser_viewset

IconChooserBlock = icon_chooser_viewset.get_block_class(
    name="IconChooserBlock", module_path="wagtail_icons.blocks"
)
