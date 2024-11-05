from django import forms

from wagtail_icons.models import Icon


class IconQueryForm(forms.Form):
    query = forms.CharField(required=False)
    provider = forms.CharField(required=False)
    style = forms.CharField(required=False)

    def get_icons(self):
        icons = Icon.objects.filter(is_deleted=False)

        query = self.cleaned_data.get("query")
        provider = self.cleaned_data.get("provider")
        style = self.cleaned_data.get("style")

        if query:
            icons = icons.filter(name__icontains=query)
        if provider:
            icons = icons.filter(provider=provider)
        if style:
            icons = icons.filter(style=style)

        return icons
