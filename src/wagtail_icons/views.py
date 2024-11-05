from django.urls import path
from django.views.generic import TemplateView
from wagtail.admin.viewsets.base import ViewSet

from wagtail_icons.components.icon import IconComponent
from wagtail_icons.components.icon_grid import IconGridComponent
from wagtail_icons.forms import IconQueryForm
from wagtail_icons.models import Icon


class IconQueryView(TemplateView):
    template_name = "icon_chooser/query.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = IconQueryForm(self.request.GET)
        if form.is_valid():
            icons = form.get_icons()
            icon_components = [IconComponent(icon) for icon in icons]
            icon_grid = IconGridComponent(icon_components)
            context["icon_grid"] = icon_grid
        return context


class IconListingView(TemplateView):
    template_name = "icon_chooser/listing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        providers = (
            Icon.objects.filter(is_deleted=False)
            .values_list("provider", flat=True)
            .distinct()
        )
        context["providers"] = providers
        return context


class IconChooserViewSet(ViewSet):
    @property
    def query_view(self):
        return self.construct_view(IconQueryView)

    @property
    def listing_view(self):
        return self.construct_view(IconListingView)

    def get_urlpatterns(self):
        return [
            path("query/", self.query_view, name="query"),
            path("chooser/", self.listing_view, name="chooser"),
        ]


icon_chooser_viewset = IconChooserViewSet("icon-chooser")
