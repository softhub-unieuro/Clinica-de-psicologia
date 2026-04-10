from django.core.management.base import BaseCommand
from axes.models import AccessAttempt

class Command(BaseCommand):
    def handle(self, *args, **options):
        count = AccessAttempt.objects.filter(locked=True).delete()[0]
        self.stdout.write(f'✅ {count} tentativas bloqueadas limpas')