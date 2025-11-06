from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--ratio', dest="ratio", type=str, required=True)

    def handle(self, *args, **options):
        users_to_create = []
        options["ratio"]

        for i in range(10_000):
            username = f"z_{i}@m.ru"
            user = User(email=username, username=username)
            users_to_create.append(user)

        created_users = User.objects.bulk_create(users_to_create, batch_size=150)
        print(f"Было создано {len(created_users)} пользователей")
