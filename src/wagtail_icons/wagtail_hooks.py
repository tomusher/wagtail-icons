import logging

from wagtail import hooks

from wagtail_icons.views import icon_chooser_viewset

logger = logging.getLogger(__name__)


@hooks.register("register_admin_viewset")
def register_icon_chooser_viewset():
    return icon_chooser_viewset
