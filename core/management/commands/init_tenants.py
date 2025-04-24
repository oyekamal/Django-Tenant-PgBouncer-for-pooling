from django.core.management.base import BaseCommand
from django.db import connection
from django_tenants.utils import schema_context
from core.models import Client, Domain

class Command(BaseCommand):
    help = 'Initialize the database for django-tenants'

    def handle(self, *args, **options):
        # First create the public schema
        self.stdout.write("Creating public schema...")
        with connection.cursor() as cursor:
            cursor.execute('CREATE SCHEMA IF NOT EXISTS public')
            cursor.execute('SET search_path TO public')

        # Run migrations for all schemas
        from django.core.management import call_command
        self.stdout.write("Running migrations for all schemas...")
        call_command('migrate_schemas')  # This will migrate all schemas including public

        # After migrations are complete, create the public tenant
        self.stdout.write("Creating public tenant...")
        if not Client.objects.filter(schema_name='public').exists():
            public_tenant = Client(
                schema_name='public',
                name='Public',
                paid_until='2024-12-31',
                on_trial=False
            )
            public_tenant.save()

            domain = Domain()
            domain.domain = 'localhost'
            domain.tenant = public_tenant
            domain.is_primary = True
            domain.save()
            
            self.stdout.write(self.style.SUCCESS('Successfully created public tenant and domain'))
        else:
            self.stdout.write("Public tenant already exists")
