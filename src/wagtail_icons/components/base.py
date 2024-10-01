from typing import ClassVar

from django.template import Template, Context
from laces.components import Component


class ColocatedComponent(Component):
    template: ClassVar[str]

    def render_html(self, parent_context=None):
        context_data = self.get_context_data(parent_context)
        if context_data is None:
            raise TypeError("Expected a dict from get_context_data, got None")

        template = Template(self.template)
        context = Context(context_data)
        return template.render(context=context)
