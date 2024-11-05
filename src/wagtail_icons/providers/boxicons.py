from wagtail_icons.providers.github_provider import (
    GithubIconProvider,
    GithubIconProviderSettings,
)


class BoxiconsIconProvider(GithubIconProvider):
    name = "boxicons"
    settings_type = GithubIconProviderSettings

    ICONS_URL = "https://api.github.com/repos/atisawd/boxicons/contents/svg/solid"
    SVG_BASE_URL = "https://raw.githubusercontent.com/atisawd/boxicons/master/svg/{style}/{name}.svg"
