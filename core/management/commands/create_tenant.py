from django.core.management.base import BaseCommand
from core.models import Client, Domain

class Command(BaseCommand):
    help = 'Creates the public tenant and domain'

    def handle(self, *args, **options):
        if Client.objects.filter(schema_name='public').exists():
            self.stdout.write(self.style.SUCCESS('Public tenant already exists'))
            return

        # Create public tenant
        public_tenant = Client(
            schema_name='public',
            name='Public',
            paid_until='2024-12-31',
            on_trial=False
        )
        public_tenant.save()

        # Create domain for public tenant
        domain = Domain()
        domain.domain = 'localhost'
        domain.tenant = public_tenant
        domain.is_primary = True
        domain.save()

        self.stdout.write(self.style.SUCCESS('Successfully created public tenant and domain'))