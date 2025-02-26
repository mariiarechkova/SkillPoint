from organisations.models import DepartmentWeight
from users.models import User
from voting.services.calculation_services.department_weight_estimation_service import DepartmentWeightEstimationService
from voting.services.calculation_services.normalization_service import NormalizationService
from voting.tests.calculation_tests.test_helpers import BaseTestCase


class DepartmentWeightEstimationTestCase(BaseTestCase):
    def test_get_department_weight(self):
        department_weight = DepartmentWeightEstimationService()
        result = department_weight.get_department_weight()
        expected_result = {
            1: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            2: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            3: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            4: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            5: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0.6},
            6: {1: 1, 2: 1, 3: 1, 4: 1, 5: 0.6, 6: 1},
        }
        self.assertEqual(result, expected_result)

    def test_empty_user_department(self):
        # check the result if the user does not have a department.
        User.objects.all().update(department=None)
        department_weight = DepartmentWeightEstimationService()
        result = department_weight.get_department_weight()
        expected_result = {
            1: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            2: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            3: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            4: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            5: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            6: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
        }
        self.assertEqual(result, expected_result)

    def test_empty_department_weight(self):
        # check the result if the weights of the departments are not defined
        DepartmentWeight.objects.all().delete()

        department_weight = DepartmentWeightEstimationService()
        result = department_weight.get_department_weight()
        expected_result = {
            1: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            2: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            3: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            4: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            5: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            6: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
        }
        self.assertEqual(result, expected_result)

    def test_get_common_weight(self):
        total_weight = DepartmentWeightEstimationService()
        result = total_weight.get_common_weight()

        expected_result = {
            1: {1: 3.0, 2: 6.0, 3: 3.0, 4: 3.0, 5: 3.0, 6: 3.0},
            2: {1: 3.0, 2: 6.0, 3: 3.0, 4: 3.0, 5: 3.0, 6: 3.0},
            3: {1: 3.0, 2: 6.0, 3: 3.0, 4: 3.0, 5: 3.0, 6: 3.0},
            4: {1: 3.0, 2: 6.0, 3: 3.0, 4: 3.0, 5: 3.0, 6: 3.0},
            5: {1: 3.0, 2: 6.0, 3: 3.0, 4: 3.0, 5: 3.0, 6: 1.8},
            6: {1: 3.0, 2: 6.0, 3: 3.0, 4: 3.0, 5: 1.8, 6: 3.0}
            }
        self.assertEqual(result, expected_result)

    def test_get_sum_weight(self):
        sum_weight = DepartmentWeightEstimationService()
        result = sum_weight.get_sum_weight()

        expected_result = {
            1: 21,
            2: 21,
            3: 21,
            4: 21,
            5: 19.8,
            6: 19.8
            }
        self.assertEqual(result, expected_result)

    def test_calculate_weight_estimation(self):
        data = NormalizationService().calculate_updated_estimations()
        estimations = DepartmentWeightEstimationService()
        result = estimations.calculate_weight_estimation(data)

        expected_result = {
            1: 5.03,
            2: 5.41,
            3: 4.57,
            4: 4.57,
            5: 5.4,
            6: 3.4
        }
        self.assertEqual(result, expected_result)

