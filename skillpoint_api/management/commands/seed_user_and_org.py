import random
import string
from django.core.management.base import BaseCommand
from skillpoint_api.models import Organisation, User
from faker import Faker

fake = Faker()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Генерация рандомных данных для организации
        org_name = fake.company()

        # Проверяем, существует ли такая организация
        organisation, org_created = Organisation.objects.get_or_create(
            name=org_name
        )

        if org_created:
            self.stdout.write(self.style.SUCCESS(f'Organization "{org_name}" created'))
        else:
            self.stdout.write(self.style.WARNING(f'Organization "{org_name}" already exists'))

        # Генерация рандомных данных для пользователя
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@test.com"
        password = f"{first_name}{last_name}123"

        user, user_created = User.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'last_name': last_name, 'organisation': organisation}
        )

        if user_created:
            user.set_password(password)  # Хешируем пароль
            user.save()  # Сохраняем пользователя с хешированным паролем
            self.stdout.write(self.style.SUCCESS(f'User with email "{email}" created for organization "{org_name}"'))
        else:
            self.stdout.write(self.style.WARNING(f'User with email"{email}" already exists in organization "{org_name}"'))
