from rest_framework.test import APITestCase
from rest_framework import status
from skillpoint_api.models import Department, Organisation, User

class DepartmentAPITestCase(APITestCase):
    def setUp(self):
        # Создаем организацию и пользователя
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.user = User.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            organisation=self.organisation,
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые отделы
        self.department1 = Department.objects.create(title="HR", organisation=self.organisation)
        self.department2 = Department.objects.create(title="development", organisation=self.organisation)

    def test_get_departments(self):
        # Тест для GET /departments/
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], self.department1.title)