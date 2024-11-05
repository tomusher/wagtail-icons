from dataclasses import dataclass

from wagtail_icons.providers.base import IconProviderSettings
from wagtail_icons.providers.github_provider import (
    GithubIconProvider,
)


@dataclass
class TablerIconProviderSettings(IconProviderSettings):
    default_style: str = "filled"


class TablerIconProvider(GithubIconProvider[TablerIconProviderSettings]):
    name = "tabler"
    settings_type = TablerIconProviderSettings

    ICONS_URL = "https://api.github.com/repos/tabler/tabler-icons/contents/icons/filled"
    SVG_BASE_URL = "https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/{style}/{name}.svg"
