from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from voting.models import VoteEvent, VoteRoundDetails, VoteRound
from organisations.models import Organisation
from users.models import User

class VoteRoundDetailsViewTestCase(APITestCase):
    def setUp(self):
        # Organisation
        self.organisation = Organisation.objects.create(name="Test Organisation")

        # Judge
        self.judge = User.objects.create(
            email="judge@example.com",
            password="password123",
            first_name="Judge",
            last_name="User",
            organisation=self.organisation
        )


        # Rated user
        self.rated_user = User.objects.create(
            email="user@example.com",
            password="password123",
            first_name="Rated",
            last_name="User",
            organisation=self.organisation
        )

        self.vote_event = VoteEvent.objects.create(
            start_day=1,
            end_day=10,
            frequency="month",
            organisation=self.organisation
        )


        self.vote_round = VoteRound.objects.create(
            vote_event=self.vote_event,
            start_at=timezone.now(),
            end_at=timezone.now() + relativedelta(months=6)
        )

        # URL
        self.url = reverse('vote-details', kwargs={'pk': self.vote_event.pk})

    def test_create_vote_round_details_success(self):
        self.client.force_authenticate(user=self.judge)
        data = [
            {
                "estimation": 9.5,
                "comment": "Отличная работа",
                "rated_user": self.rated_user.id,
                "vote_round": self.vote_round.id
            },
            {
                "estimation": 8.0,
                "comment": "Хороший результат",
                "rated_user": self.rated_user.id,
                "vote_round": self.vote_round.id
            }
        ]

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['judge'], self.judge.id)
        self.assertEqual(response.data[0]['vote_round'], self.vote_round.id)

    def test_create_vote_details_unauthorized(self):
        """The error text if the user is unauthorized."""
        data = [
            {
                "estimation": 7.5,
                "comment": "Хорошо",
                "rated_user": self.rated_user.id,
                "vote_round": self.vote_round.id
            }
        ]

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)