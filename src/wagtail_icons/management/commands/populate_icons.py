from django.core.management.base import BaseCommand

from ...services import populate_icons


class Command(BaseCommand):
    help = "Populates the database with icons from all configured providers"

    def handle(self, *args, **options):
        self.stdout.write("Starting icon population...")
        populate_icons()
        self.stdout.write(self.style.SUCCESS("Successfully populated icons"))
