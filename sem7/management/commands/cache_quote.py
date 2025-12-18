import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management import BaseCommand


def heavy_lifting():
    response = requests.get(
        "https://api.api-ninjas.com/v2/randomquotes",
        headers={"X-Api-Key": settings.API_KEY}
    )

    if response.status_code == 200:
        quote = response.json()[0]["quote"]
        return quote


class Command(BaseCommand):
    CACHE_KEY = "quote"

    def handle(self, *args, **options):
        quote = heavy_lifting()
        cache.set(self.CACHE_KEY, quote, timeout=20)
