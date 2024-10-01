from dataclasses import dataclass

import requests

from .base import Icon, IconProvider, IconProviderSettings


@dataclass
class FontAwesomeIconProviderSettings(IconProviderSettings):
    api_token: str
    api_url: str = "https://api.fontawesome.com/"


class FontAwesomeIconProvider(IconProvider):
    name = "FontAwesome"
    alias = "fontawesome"

    settings_type: type[FontAwesomeIconProviderSettings] = (
        FontAwesomeIconProviderSettings
    )

    def _to_icon(self, icon: dict) -> Icon:
        return Icon(
            name=icon["id"],
            label=icon["label"],
            svg=icon["svgs"][0]["html"],
            provider=self.alias,
        )

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

    def get_icons(self) -> list[Icon]:
        query = """
        query {
          search(version: "6.0.0", query: "arrow") {
            id
            label
            styles
            svgs {
              html
            }
          }
        }
        """

        data = self.do_graphql_request(query)
        icons = data["data"]["search"]

        return [self._to_icon(icon) for icon in icons]

    def get_icon(self, name: str) -> Icon:
        query = f"""
        query {{
          search(version: "6.0.0", query: "{name}") {{
            id
            label
            styles
            svgs {{
              html
            }}
          }}
        }}
        """

        data = self.do_graphql_request(query)
        icons = data["data"]["search"]

        for icon in icons:
            if icon["id"] == name:
                return self._to_icon(icon)

        raise ValueError(f"Icon {name} not found")
