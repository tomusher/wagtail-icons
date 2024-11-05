from wagtail_icons.providers.github_provider import (
    GithubIconProvider,
    GithubIconProviderSettings,
)


class HeroiconsIconProvider(GithubIconProvider):
    name = "heroicons"
    settings_type = GithubIconProviderSettings

    ICONS_URL = "https://api.github.com/repositories/242754476/contents/src/24/solid"
    SVG_BASE_URL = "https://raw.githubusercontent.com/tailwindlabs/heroicons/master/src/24/{style}/{name}.svg"
