from wagtail_icons.components.base import ColocatedComponent
from wagtail_icons.providers.base import Icon


class IconComponent(ColocatedComponent):
    template = """
<div data-icon-name="{{ icon.name }}">
    <div class="w-10 h-10">{{ icon.svg|safe }}</div>
    <span>{{ icon.label }}</span>
</div>
"""

    def __init__(self, icon: Icon):
        self.icon = icon

    def get_context_data(self, parent_context=None):
        return {"icon": self.icon}
