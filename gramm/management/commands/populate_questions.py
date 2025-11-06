from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        ...