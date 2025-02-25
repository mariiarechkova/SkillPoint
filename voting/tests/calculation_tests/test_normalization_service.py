from django.test import TestCase
from organisations.models import Organisation
from users.models import User
from voting.models import VoteEvent, VoteRound, VoteRoundDetails
from voting.services.calculation_services.normalization_service import (NormalizationService, JudgeEstimationsRepository,
                                                                        RatedUserEstimationsRepository)
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from voting.tests.calculation_tests.test_helpers import BaseTestCase


class CalculationNormalizationTestCase(BaseTestCase):
    def test_get_judges_with_estimations(self):
        result = JudgeEstimationsRepository.get_judges_with_estimations()

        expected_result = {
            1: [6, 5, 5, 6],
            2: [6, 4, 4, 5, 4],
            3: [5, 7, 5, 6],
            4: [4, 5, 5, 5, 5],
            5: [4, 5, 4, 4, 6],
            6: [5, 5, 5, 5, 6]
        }
        self.assertEqual(result, expected_result)

    def test_calculate_normalization_coefficient(self):
        """Test the calculation of the normalization coefficient."""

        normalization_service = NormalizationService()
        result = normalization_service.calculate_normalization_coefficient()

        expected_coefficient = {
            1: 0.9259,
            2: 1.0714,
            3: 0.8929,
            4: 1.0345,
            5: 1.0714,
            6: 0.9677
        }

        self.assertEqual(result, expected_coefficient)

    def test_empty_estimations(self):
        VoteRoundDetails.objects.all().delete()

        normalization_service = NormalizationService()

        with self.assertRaises(ValueError) as context:
            normalization_service.calculate_normalization_coefficient()

        self.assertEqual(str(context.exception), "The estimations data is empty.")

    def test_get_rated_users_with_estimations(self):
        result = RatedUserEstimationsRepository.get_rated_users_with_estimations()

        expected_result = {
            1: {2: 6.0, 3: 5.0, 4: 4.0, 5: 4.0, 6: 5.0},
            2: {1: 6.0, 3: 7.0, 4: 5.0, 5: 5.0, 6: 5.0},
            3: {1: 5.0, 2: 4.0, 4: 5.0, 5: 4.0, 6: 5.0},
            4: {1: 5.0, 2: 4.0, 3: 5.0, 5: 4.0, 6: 5.0},
            5: {1: 6.0, 2: 5.0, 3: 6.0, 4: 5.0, 6: 6.0},
            6: {2: 4.0, 4: 5.0, 5: 6.0},
        }
        self.assertEqual(result, expected_result)

    def test_calculate_updated_estimations(self):
        normalization_service = NormalizationService()
        result = normalization_service.calculate_updated_estimations()
        expected_result = {
            1: {1: 4.63, 2: 6.43, 3: 4.46, 4: 4.14, 5: 4.29, 6: 4.84},
            2: {1: 5.56, 2: 5.36, 3: 6.25, 4: 5.17, 5: 5.36, 6: 4.84},
            3: {1: 4.63, 2: 4.29, 3: 4.46, 4: 5.17, 5: 4.29, 6: 4.84},
            4: {1: 4.63, 2: 4.29, 3: 4.46, 4: 5.17, 5: 4.29, 6: 4.84},
            5: {1: 5.56, 2: 5.36, 3: 5.36, 4: 5.17, 5: 5.36, 6: 5.81},
            6: {2: 4.29, 4: 5.17, 5: 6.43, 6: 4.84},
        }

        self.assertEqual(result, expected_result)