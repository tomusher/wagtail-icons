from dataclasses import dataclass

import requests

from .base import Icon, IconProvider, IconProviderSettings


@dataclass
class FontAwesomeIconProviderSettings(IconProviderSettings):
    api_token: str
    api_url: str = "https://api.fontawesome.com/"


class FontAwesomeIconProvider(IconProvider[FontAwesomeIconProviderSettings]):
    name = "FontAwesome"
    alias = "fontawesome"

    settings_type = FontAwesomeIconProviderSettings

    def _extract_aliases(self, icon: dict) -> str:
        aliases = icon.get("aliases", {}) or {}
        return ", ".join(aliases.get("names", []))

    def _to_icons(self, icons: list[dict]) -> list[Icon]:
        styles = self.get_styles()
        icon_objs = []
        for family, style in styles:
            for icon in icons:
                matching_svg = next(
                    (
                        svg
                        for svg in icon["svgs"]
                        if svg["familyStyle"]["family"] == family
                        and svg["familyStyle"]["style"] == style
                    ),
                    None,
                )
                if matching_svg:
                    icon_objs.append(
                        Icon(
                            name=icon["id"],
                            label=icon["label"],
                            svg=matching_svg["html"],
                            provider=self.alias,
                            style=f"{family}-{style}",
                            aliases=self._extract_aliases(icon),
                        )
                    )
        return icon_objs

    def do_graphql_request(self, query: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.settings.api_url, json={"query": query}, headers=headers, timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_access_token(self) -> str:
        headers = {
            "Authorization": f"Bearer {self.settings.api_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{self.settings.api_url}/token", headers=headers, timeout=10
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def get_styles(self) -> list[tuple[str, str]]:
        query = """
        query {
          release(version: "6.0.0") {
            familyStyles {
                family
                style
            }
          }
        }
        """

        data = self.do_graphql_request(query)
        styles = data["data"]["release"]["familyStyles"]
        return [(style["family"], style["style"]) for style in styles]

    def get_all_icons(self) -> list[Icon]:
        query = """
        query {
          release(version: "6.0.0") {
            icons {
                id
                label
                aliases {
                    names
                }
                svgs {
                    html
                    familyStyle {
                        family
                        style
                    }
                }
            }
          }
        }
        """

        data = self.do_graphql_request(query)
        icons = data["data"]["release"]["icons"]

        return self._to_icons(icons)
