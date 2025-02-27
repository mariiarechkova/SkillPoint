from voting.services.calculation_services.awards_service import get_awards
from voting.services.calculation_services.department_weight_estimation_service import DepartmentWeightEstimationService
from voting.services.calculation_services.normalization_service import NormalizationService
from voting.tests.calculation_tests.test_helpers import BaseTestCase


class AwardsServiceTestCase(BaseTestCase):
    def test_get_estimations_with_stability(self):
        normalization = NormalizationService().calculate_updated_estimations()
        service = DepartmentWeightEstimationService()
        data = service.calculate_weight_estimation(normalization)
        stability = self.organisation.stability
        salary = {
            1: 450,
            2: 580,
            3: 450,
            4: 480,
            5: 600,
            6: 500
        }
        result = get_awards(data, stability, salary)

        expected_result = {
            1: 0.1643,
            2: 0.2528,
            3: 0.1283,
            4: 0.1369,
            5: 0.2604,
            6: 0.0573
        }
        self.assertEqual(result, expected_result)
