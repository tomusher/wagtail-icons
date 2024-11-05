from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests

from wagtail_icons.providers.base import Icon, IconProvider, IconProviderSettings


@dataclass
class GithubIconProviderSettings(IconProviderSettings):
    default_style: str = "solid"


class GithubIconProvider(IconProvider[GithubIconProviderSettings], ABC):
    settings_type = GithubIconProviderSettings

    ICONS_URL: str
    SVG_BASE_URL: str

    @property
    @abstractmethod
    def icons_url(self) -> str:
        return self.ICONS_URL

    @property
    @abstractmethod
    def svg_base_url(self) -> str:
        return self.SVG_BASE_URL

    def fetch_icons(self):
        try:
            response = requests.get(self.icons_url, timeout=10)
            response.raise_for_status()
            icons_data = response.json()
            return [
                icon["name"].replace(".svg", "")
                for icon in icons_data
                if icon["name"].endswith(".svg")
            ]
        except requests.RequestException as e:
            print(f"Error fetching icons: {e}")
            return []

    def get_icons(self, query: str) -> list[Icon]:
        icons = []
        for name in self.fetch_icons():
            if query.lower() in name.lower():
                for style in self.get_available_styles():
                    svg = self.render_icon(name, style)
                    icons.append(
                        Icon(
                            name=name,
                            label=name.replace("-", " ").title(),
                            svg=svg,
                            provider=self.name,
                            style=style,
                        )
                    )
        return icons

    def get_icon(self, name: str, style: str = None) -> Icon:
        if name not in self.fetch_icons():
            raise ValueError(f"Icon '{name}' not found in {self.name} set")

        if style is None:
            style = self.settings.default_style

        svg = self.render_icon(name, style)
        return Icon(
            name=name,
            label=name.replace("-", " ").title(),
            svg=svg,
            provider=self.name,
            style=style,
        )

    def render_icon(self, name: str, style: str) -> str:
        url = self.svg_base_url.format(style=style, name=name)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching SVG for icon '{name}': {e}")
            return f"<svg>Error loading icon '{name}'</svg>"

    def get_all_icons(self) -> list[Icon]:
        icons = []
        for name in self.fetch_icons():
            for style in self.get_available_styles():
                svg = self.render_icon(name, style)
                icons.append(
                    Icon(
                        name=name,
                        label=name.replace("-", " ").title(),
                        svg=svg,
                        provider=self.name,
                        style=style,
                    )
                )
        return icons

    @abstractmethod
    def get_available_styles(self) -> list[str]:
        pass
