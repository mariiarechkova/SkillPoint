import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend-project.settings')
django.setup()

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Department, Organisation
from users.models import User

class DepartmentAPITestCase(APITestCase):
    def setUp(self):
        # Создаем организацию и пользователя
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.user = User.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            organisation=self.organisation,
            password="password123",
            is_staff = True
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые отделы
        self.department1 = Department.objects.create(title="HR", organisation=self.organisation)
        self.department2 = Department.objects.create(title="development", organisation=self.organisation)

    def test_get_departments(self):
        # Тест для GET /departments/
        url = reverse('departments-list')  # Использование reverse для получения правильного URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], self.department1.title)

    def test_create_department(self):
        # Test for POST /departments/

        url = reverse('departments-list')
        data = {
            'title': 'New Department',
            'organisation': self.organisation.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Department')
        department = Department.objects.get(id=response.data['id'])
        self.assertEqual(department.organisation.id, self.organisation.id)
