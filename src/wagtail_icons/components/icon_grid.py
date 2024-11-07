from wagtail_icons.components.base import ColocatedComponent
from wagtail_icons.components.icon import IconComponent


class IconGridComponent(ColocatedComponent):
    template = """
{% load wagtailadmin_tags %}
<div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
    {% for icon in icons %}
        {% component icon %}
    {% endfor %}
</div>
"""

    def __init__(self, icons: list[IconComponent]):
        self.icons = icons

    def get_context_data(self, parent_context=None):
        return {"icons": self.icons}
