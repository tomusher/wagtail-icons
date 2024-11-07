from wagtail_icons.components.base import ColocatedComponent
from wagtail_icons.models import Icon


class IconComponent(ColocatedComponent):
    template = """
    <a href="{{ url }}" data-icon-name="{{ icon.name }}" class="relative flex items-center justify-center p-4 border rounded-lg shadow-sm hover:shadow-md hover:border-blue-300 transition-all duration-300 cursor-pointer group" {% for key, value in attrs.items %} {{ key }}="{{ value }}" {% endfor %}>
        <div class="w-10 h-10 flex items-center justify-center fill-[--w-color-text-label]">{{ icon.svg|safe }}</div>
        <span class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-70 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-center">{{ icon.label }}</span>
    </a>
    """

    def __init__(self, icon: Icon, url: str, attrs: dict = None):
        self.icon = icon
        self.url = url
        self.attrs = attrs or {}

    def get_context_data(self, parent_context=None):
        return {"icon": self.icon, "url": self.url, "attrs": self.attrs}
