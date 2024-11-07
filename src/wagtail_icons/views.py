from django.urls import reverse
from wagtail.admin.views.generic.chooser import (
    BaseChooseView,
    ChooseResultsViewMixin,
    ChooseViewMixin,
    CreationFormMixin,
)
from wagtail.admin.viewsets.chooser import ChooserViewSet

from wagtail_icons.components.icon import IconComponent
from wagtail_icons.components.icon_grid import IconGridComponent
from wagtail_icons.models import Icon, IconSvgColumn


class BaseIconChooseView(BaseChooseView):
    results_template_name = "icon_chooser/results.html"
    per_page = 50

    @property
    def columns(self):
        return [
            IconSvgColumn("svg"),
            self.title_column,
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        results = context["results"]

        icon_components = []
        for icon in results:
            url = reverse("icon_chooser:chosen", args=[icon.id])
            icon_components.append(
                IconComponent(icon, url, attrs={"data-chooser-modal-choice": True})
            )
        icon_grid = IconGridComponent(icon_components)
        context["icon_grid"] = icon_grid
        return context


class IconChooseView(ChooseViewMixin, CreationFormMixin, BaseIconChooseView):
    pass


class IconChooseResultsView(
    ChooseResultsViewMixin, CreationFormMixin, BaseIconChooseView
):
    pass


class IconChooserViewSet(ChooserViewSet):
    model = Icon
    choose_one_text = "Choose an icon"
    choose_another_text = "Choose another icon"
    edit_item_text = "Edit this icon"

    choose_view_class = IconChooseView
    choose_results_view_class = IconChooseResultsView


icon_chooser_viewset = IconChooserViewSet("icon_chooser")
