from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from organisations.models import Organisation
from .models import VoteEvent


class VoteEventsViewTestCase(APITestCase):

    def setUp(self):
        # Создание тестовых данных
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.vote_event = VoteEvent.objects.create(
            frequency='month',
            start_day=1,
            end_day=15,
            organisation=self.organisation
        )
        # Создание пользователя для аутентификации
        self.user = User.objects.create(
            email="test@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="Test",
            organisation=self.organisation,
            is_staff = True
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vote_event(self):
        """Test GET /vote_event/{pk}/"""
        url = reverse('vote-events-list', kwargs={'pk': self.vote_event.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.vote_event.id)

    def test_get_all_vote_events(self):
        """Test GET /vote_events/"""
        url = reverse('vote-events-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # только один event в базе на данный момент

    def test_create_vote_event(self):
        """Test POST /vote_events/"""
        url = reverse('vote-events-list')
        data = {
            'frequency': 'week',
            'start_day': 5,
            'end_day': 10,
            'organisation': self.organisation.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VoteEvent.objects.count(), 2)

    def test_create_vote_event_without_permission(self):
        """Test that non-admin users cannot create vote events."""

        user = User.objects.create(
            email="user@example.com",
            password="userpassword123",
            first_name="Normal",
            last_name="User",
            organisation=self.organisation,
            is_staff = False
        )
        self.client.force_authenticate(user=user)

        url = reverse('vote-events-list')
        data = {
            'frequency': 'week',
            'start_day': 5,
            'end_day': 10,
            'organisation': self.organisation.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_vote_event(self):
        """Test PUT /vote_event/{pk}/"""
        url = reverse('vote-events-list', kwargs={'pk': self.vote_event.pk})
        data = {
            'frequency': 'year',
            'start_day': 1,
            'end_day': 30,
            'organisation': self.organisation.id
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['frequency'], 'year')

    def test_partial_update_vote_event(self):
        """Test PATCH /vote_event/{pk}/"""
        url = reverse('vote-events-list', kwargs={'pk': self.vote_event.pk})
        data = {
            'frequency': 'quarter'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['frequency'], 'quarter')

    def test_delete_vote_event(self):
        """Test DELETE /vote_event/{pk}/"""
        url = reverse('vote-events-list', kwargs={'pk': self.vote_event.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VoteEvent.objects.count(), 0)
