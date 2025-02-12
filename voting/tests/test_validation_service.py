from dateutil.relativedelta import relativedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone

from organisations.models import Organisation
from users.models import User
from voting.models import VoteEvent, VoteRound, VoteRoundDetails
from voting.services.validation_service import AvailableUsersService, ParticipantService


class AvailableUsersServiceTestCase(APITestCase):
    def setUp(self):
        # Creating test data
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.vote_event = VoteEvent.objects.create(
            frequency='month',
            start_day=1,
            end_day=15,
            organisation=self.organisation
        )
        # Judge
        self.user = User.objects.create(
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
        self.client.force_authenticate(user=self.user)

        self.vote_round = VoteRound.objects.create(
            vote_event=self.vote_event,
            start_at=timezone.now(),
            end_at=timezone.now() + relativedelta(months=6)
        )

    def test_is_user_voted_success(self):
        """check the method correctly determines the fact of voting."""

        VoteRoundDetails.objects.create(
            estimation=8.5,
            judge=self.user,
            rated_user=self.rated_user,
            vote_round=self.vote_round
        )
        validation_service = AvailableUsersService(self.vote_event, self.user)

        self.assertTrue(validation_service.is_user_voted())

    def test_is_user_voted_invalid(self):
        """checking the user did not vote."""

        validation_service = AvailableUsersService(self.vote_event, self.user)

        self.assertFalse(validation_service.is_user_voted())


    def test_is_eligible_user_vote_invalid(self):
        """checks that the user can vote"""

        validation_service = AvailableUsersService(self.vote_event, self.user)

        self.assertTrue(validation_service.is_eligible_user_vote())

    def test_is_eligible_user_vote_false(self):
        """checks that the user CAN NOT vote"""
        VoteRoundDetails.objects.create(
            estimation = 8.5,
            judge = self.user,
            rated_user = self.rated_user,
            vote_round = self.vote_round
        )
        validation_service = AvailableUsersService(self.vote_event, self.user)

        self.assertFalse(validation_service.is_eligible_user_vote())


class ParticipantServiceTestCase(APITestCase):
    def setUp(self):
        # create orgatisation
        self.org1 = Organisation.objects.create(name="Test Organisation")
        self.org2 = Organisation.objects.create(name="Other Organisation")

        # create 3 users
        self.user1 = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            organisation=self.org1,
            password="password123",
        )
        self.user2 = User.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            organisation=self.org1,
            password="password123",
        )

        self.user3 = User.objects.create(
            first_name="Alice",
            last_name="Brown",
            email="alicebrown@example.com",
            organisation=self.org2,
            password="password123",
        )

        self.client.force_authenticate(user=self.user1)

        self.vote_event = VoteEvent.objects.create(
            frequency='month',
            start_day=1,
            end_day=15,
            organisation=self.org1
        )

    def test_excludes_current_user(self):
        available_users = ParticipantService.get_available_users_for_voting(self.org1, self.user1)
        self.assertNotIn(self.user1, available_users)

    def test_returns_only_users_from_same_organisation(self):
        available_users = ParticipantService.get_available_users_for_voting(self.org1, self.user1)
        self.assertIn(self.user2, available_users)
        self.assertNotIn(self.user3, available_users)

    def test_returns_empty_queryset_if_no_other_users(self):
        available_users = ParticipantService.get_available_users_for_voting(self.org2, self.user3)
        self.assertEqual(available_users.count(), 0)


    def test_get_available_users_success(self):
        """Testing getting a list of users to vote on"""
        self.url = reverse('available-to-vote', kwargs={'pk': self.vote_event.id})
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # only 1 user should return(user2)
        self.assertEqual(response.data[0]["email"], "jane@example.com")
