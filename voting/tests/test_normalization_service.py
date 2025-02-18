from django.test import TestCase

from organisations.models import Organisation
from users.models import User
from voting.models import VoteEvent, VoteRound, VoteRoundDetails
from voting.services.calculation_services.normalization_service import NormalizationService, EstimationsRepository
from dateutil.relativedelta import relativedelta
from django.utils import timezone

class CalculationNormalizationTestCase(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(name="Test Organisation")

        self.vote_event = VoteEvent.objects.create(
            frequency='month',
            start_day=1,
            end_day=15,
            organisation=self.organisation
        )
        self.vote_round = VoteRound.objects.create(
            vote_event=self.vote_event,
            start_at=timezone.now(),
            end_at=timezone.now() + relativedelta(months=6)
        )

        user_data = [
            ("Jane", "Smith", "jane@example.com"),
            ("John", "Doe", "john@example.com"),
            ("Alice", "Brown", "alice@example.com"),
            ("Bob", "White", "bob@example.com"),
            ("Charlie", "Black", "charlie@example.com"),
            ("Eva", "Green", "eva@example.com"),
        ]

        for i, (first_name, last_name, email) in enumerate(user_data, start=1):
            setattr(self, f"user{i}", User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                organisation=self.organisation,
                password="password123",
            ))

        users = [self.user1, self.user2, self.user3, self.user4, self.user5, self.user6]

        estimations = {
            self.user1.id: [6, 5, 5, 6],
            self.user2.id: [6, 4, 4, 5, 4],
            self.user3.id: [5, 7, 5, 6],
            self.user4.id: [4, 5, 5, 5, 5],
            self.user5.id: [4, 5, 4, 4, 6],
            self.user6.id: [5, 5, 5, 5, 6]
        }

        votes = []
        for judge in users:
            rated_users = [user for user in users if user != judge]
            for rated_user, estimation in zip(rated_users, estimations[judge.id]):
                votes.append(VoteRoundDetails(
                    estimation=estimation,
                    judge=judge,
                    rated_user=rated_user,
                    vote_round=self.vote_round
                ))

        VoteRoundDetails.objects.bulk_create(votes)

    def test_get_judges_with_estimations(self):
        result = EstimationsRepository.get_judges_with_estimations()

        expected_result = {
            self.user1.id: [6, 5, 5, 6],
            self.user2.id: [6, 4, 4, 5, 4],
            self.user3.id: [5, 7, 5, 6],
            self.user4.id: [4, 5, 5, 5, 5],
            self.user5.id: [4, 5, 4, 4, 6],
            self.user6.id: [5, 5, 5, 5, 6]
        }
        self.assertEqual(result, expected_result)

    def test_calculate_normalization_coefficient(self):
        """Test the calculation of the normalization coefficient."""

        normalization_service = NormalizationService()
        result = normalization_service.calculate_normalization_coefficient()

        expected_coefficient = {
            self.user1.id: 0.9259,
            self.user2.id: 1.0714,
            self.user3.id: 0.8929,
            self.user4.id: 1.0345,
            self.user5.id: 1.0714,
            self.user6.id: 0.9677
        }

        self.assertEqual(result, expected_coefficient)

    def test_empty_estimations(self):
        VoteRoundDetails.objects.all().delete()

        normalization_service = NormalizationService()

        with self.assertRaises(ValueError) as context:
            normalization_service.calculate_normalization_coefficient()

        self.assertEqual(str(context.exception), "The estimations data is empty.")
