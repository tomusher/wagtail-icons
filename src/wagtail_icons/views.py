from django.urls import path
from django.views.generic import TemplateView
from wagtail.admin.viewsets.base import ViewSet

from wagtail_icons.providers.base import get_icon_providers
from wagtail_icons.components.icon_grid import IconGridComponent
from wagtail_icons.components.icon import IconComponent


class IconListingView(TemplateView):
    template_name = "icon_chooser/listing.html"

    def get_icons(self):
        icons = []
        for provider in get_icon_providers():
            icons.extend(provider.get_icons())
        return icons

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        icons = self.get_icons()
        icon_components = [IconComponent(icon) for icon in icons]
        icon_grid = IconGridComponent(icon_components)
        context["icon_grid"] = icon_grid
        return context


class IconChooserViewSet(ViewSet):
    @property
    def listing_view(self):
        return self.construct_view(IconListingView)

    def get_urlpatterns(self):
        return [
            path("chooser/", self.listing_view, name="chooser"),
        ]


icon_chooser_viewset = IconChooserViewSet("icon-chooser")
