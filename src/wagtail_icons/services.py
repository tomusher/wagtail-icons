from django.db import transaction
from django.db.models import Q

from wagtail_icons.models import Icon
from wagtail_icons.providers.base import get_icon_providers


def populate_icons():
    providers = get_icon_providers()

    for provider_name, provider in providers.items():
        with transaction.atomic():
            # Fetch all icons from the provider
            new_icons = provider.get_all_icons()

            # Get existing icons for this provider
            existing_icons = Icon.objects.filter(provider=provider_name)

            # Create a set of (name, style) tuples for efficient lookup
            new_icon_keys = {(icon.name, icon.style) for icon in new_icons}
            existing_icon_keys = set(existing_icons.values_list("name", "style"))

            # Prepare bulk create and update lists
            icons_to_create = []
            icons_to_update = []

            for icon in new_icons:
                if (icon.name, icon.style) in existing_icon_keys:
                    icons_to_update.append(
                        Icon(
                            name=icon.name,
                            provider=provider_name,
                            style=icon.style,
                            label=icon.label,
                            aliases=icon.aliases,
                            svg=icon.svg,
                            is_deleted=False,
                        )
                    )
                else:
                    icons_to_create.append(
                        Icon(
                            name=icon.name,
                            provider=provider_name,
                            style=icon.style,
                            label=icon.label,
                            aliases=icon.aliases,
                            svg=icon.svg,
                            is_deleted=False,
                        )
                    )

            # Bulk create new icons
            Icon.objects.bulk_create(icons_to_create)

            # Bulk update existing icons
            Icon.objects.bulk_update(icons_to_update, ["label", "svg", "is_deleted"])

            # Mark icons as deleted if they're not in the new set
            icons_to_delete = existing_icon_keys - new_icon_keys
            if icons_to_delete:
                delete_q = Q()
                for name, style in icons_to_delete:
                    delete_q |= Q(name=name, style=style)
                existing_icons.filter(delete_q).update(is_deleted=True)

            # Unmark icons if they've been re-added
            icons_to_undelete = new_icon_keys & set(
                existing_icons.filter(is_deleted=True).values_list("name", "style")
            )
            if icons_to_undelete:
                undelete_q = Q()
                for name, style in icons_to_undelete:
                    undelete_q |= Q(name=name, style=style)
                existing_icons.filter(undelete_q).update(is_deleted=False)

    print(f"Populated icons from {len(providers)} providers.")
