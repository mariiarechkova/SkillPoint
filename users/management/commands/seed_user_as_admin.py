from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Promote users with email starting with "admin" to staff (is_staff=True)'


    def handle(self, *args, **kwargs):
        try:
            users = User.objects.filter(email__startswith = 'admin')

            if not users.exists():
                self.stdout.write(self.style.WARNING("No users found with email starting with 'admin'."))
                return

            for user in users:
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{user.email}' promoted to staff."))

        except Exception as e:
             self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))