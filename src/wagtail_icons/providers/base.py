import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def get_icon_providers():
    providers = settings.WAGTAIL_ICONS_PROVIDERS
    for alias, config in providers.items():
        config = config.copy()
        cls = config.pop("class")
        provider_class = import_string(cls)
        yield provider_class(**config)


@dataclass
class IconProviderSettings:
    pass


@dataclass
class Icon:
    name: str
    label: str
    svg: str
    provider: str


class IconProvider(ABC):
    settings_type: type[IconProviderSettings] = IconProviderSettings

    def __init__(self, **kwargs):
        try:
            self.settings = self.settings_type(**kwargs)
        except TypeError as e:
            raise ValueError(f"Invalid settings for {self.__class__.__name__}") from e

    @abstractmethod
    def get_icons(self) -> list[Icon]:
        """
        Retrieve a list of icons from the provider.

        Returns:
            A list of Icon objects.
        """
        pass

    @abstractmethod
    def get_icon(self, name: str) -> Icon:
        """
        Retrieve a specific icon by name.

        Args:
            name: The name of the icon to retrieve.

        Returns:
            An Icon object.

        Raises:
            ValueError: If the icon with the given name is not found.
        """
        pass
