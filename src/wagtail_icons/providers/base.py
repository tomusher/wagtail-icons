import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def get_icon_providers():
    provider_config = settings.WAGTAIL_ICONS_PROVIDERS
    providers = {}
    for alias, config in provider_config.items():
        config = config.copy()
        cls = config.pop("class")
        provider_class = import_string(cls)
        providers[alias] = provider_class(**config)
    return providers


@dataclass
class IconProviderSettings:
    pass


@dataclass
class Icon:
    name: str
    label: str
    svg: str
    provider: str
    style: str = ""
    aliases: str = ""


SettingsType = TypeVar("SettingsType", bound=IconProviderSettings)


class IconProvider(ABC, Generic[SettingsType]):
    name: str
    settings_type: type[SettingsType]

    def __init__(self, **kwargs):
        try:
            self.settings = self.settings_type(**kwargs)
        except TypeError as e:
            raise ValueError(f"Invalid settings for {self.__class__.__name__}") from e

    @abstractmethod
    def get_all_icons(self) -> list[Icon]:
        """
        Retrieve all icons from the provider.

        Returns:
            A list of all Icon objects available from this provider.
        """
        pass
