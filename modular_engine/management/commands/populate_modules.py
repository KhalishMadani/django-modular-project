from django.core.management.base import BaseCommand
from modular_engine.models import Module

class Command(BaseCommand):
    def handle(self, *args, **options):
        modules = ["product_module"]
        for m in modules:
            Module.objects.get_or_create(name=m, defaults={"installed": False})
        self.stdout.write(self.style.SUCCESS("module populated successfully"))