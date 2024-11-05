from wagtail_icons.components.base import ColocatedComponent
from wagtail_icons.models import Icon


class IconComponent(ColocatedComponent):
    template = """
    <div data-icon-name="{{ icon.name }}" class="relative flex items-center justify-center p-4 border border-gray-200 rounded-lg shadow-sm hover:shadow-md hover:border-blue-300 transition-all duration-300 cursor-pointer group">
        <div class="w-10 h-10 flex items-center justify-center">{{ icon.svg|safe }}</div>
        <span class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-70 text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-center">{{ icon.label }}</span>
    </div>
    """

    def __init__(self, icon: Icon):
        self.icon = icon

    def get_context_data(self, parent_context=None):
        return {"icon": self.icon}
