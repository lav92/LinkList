import random

from django.core.management import BaseCommand
from random import choice
from django.contrib.auth.models import User
from links.models import Link


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Create links')
        all_users = User.objects.all()
        for i in range(1, 111):
            link = Link.objects.create(
                url=f'http://example.com/{i}',
                title=f'Ссылка {i}',
            )
            link.owners = random.choice(all_users)
            link.save()
            self.stdout.write(f'Ссылка {link.title} добавлена')

        self.stdout.write('Done')