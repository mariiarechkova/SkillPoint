from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from organisations.models import Organisation
from users.models import Role, User


class RolesAPITestCase(APITestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            organisation=self.organisation,
            password="password123",
            is_staff=True
        )
        self.role1 = Role.objects.create(
            title = 'director',
            weight_vote = 9.5
        )
        self.role2 = Role.objects.create(
            title='manager',
            weight_vote=7.0
        )

        self.valid_data = {
            'title': "HR",
            'weight_vote': 7.0
        }

        self.user.role.add(self.role1)
        self.client.force_authenticate(user=self.user)

    def test_create_role(self):
        url = reverse('roles-list')
        response = self.client.post(url, self.valid_data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 3)
        self.assertEqual(Role.objects.last().title, 'HR')

    def test_create_role_with_duplicate_title(self):
        url = reverse('roles-list')
        invalid_data = {
            'title': "manager",
            'weight_vote': 7.0
        }
        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['title'][0], 'role with this title already exists.')

    def test_get_role_list(self):
        url = reverse('roles-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_role_details(self):
        url = reverse('roles-detail', args=[self.role1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'director')

    def test_update_role(self):
        url = reverse('roles-detail', args=[self.role2.id])
        updating_data = {'title': 'programmer', 'weight_vote': 8.0}
        response = self.client.put(url, updating_data, format = 'json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role2.refresh_from_db()
        self.assertEqual(self.role2.title, 'programmer')
        self.assertEqual(self.role2.weight_vote, 8.0)

    def test_delete_role(self):
        url = reverse('roles-detail', args=[self.role2.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Role.objects.filter(id=self.role2.id).exists())
