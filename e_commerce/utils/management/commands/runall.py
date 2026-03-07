from django.core.management import BaseCommand, call_command
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = "run all initial commands if any changes happen with models."

    def handle(self, *args, **options):
      if getattr(settings, 'DEBUG'):
          try:
            call_command("makemigrations")
            call_command("migrate")

            if not User.objects.filter(is_superuser=True).exists():
                call_command("createsuperuser")

            call_command("runserver")
          except Exception as e:
            print(str(e))
