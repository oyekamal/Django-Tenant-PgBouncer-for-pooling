from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context

class Command(BaseCommand):
    help = 'Creates a superuser for the public tenant'

    def handle(self, *args, **options):
        with schema_context('public'):
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin'
                )
                self.stdout.write(self.style.SUCCESS('Successfully created public superuser'))
            else:
                self.stdout.write('Superuser already exists')