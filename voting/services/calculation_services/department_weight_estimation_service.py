from organisations.models import DepartmentWeight
from users.models import User
from voting.services.calculation_services.normalization_service import NormalizationService


class DepartmentWeightEstimationService:
    def __init__(self):
        self.users = User.objects.values("id", "department", "weight_vote")
        self.department_weight = DepartmentWeight.objects.values("judge_department", "rated_department", "weight_vote")

    def get_department_weight(self):
        weight_dict = {}
        for item in self.department_weight:
            judge_dept = item["judge_department"]
            rated_dept = item["rated_department"]
            weight_dict[(judge_dept, rated_dept)] = item["weight_vote"] / 10

        def get_user_data(user):
            """function for extracting user data."""
            return user["id"], user["department"]

        result = {}

        for item in self.users:
            rated_user, user_dept = get_user_data(item)
            result[rated_user] = {}

            for other_user in self.users:
                other_user_id, other_dept = get_user_data(other_user)

                if rated_user == other_user_id:
                    weight = 1
                else:
                    weight = weight_dict.get((user_dept,other_dept), 1)

                result[rated_user][other_user_id] = weight

        return result

    def get_common_weight(self):
        user_weight = {}

        for item in self.users:
            user = item['id']
            weight = item['weight_vote']
            user_weight[user] = weight

        user_department_weight = self.get_department_weight()

        for rated_user, judges  in user_department_weight.items():
            for judge in judges.keys():
                user_department_weight[rated_user][judge] *= user_weight[judge]
                user_department_weight[rated_user][judge] = float(round(user_department_weight[rated_user][judge], 1))

        return user_department_weight

    def get_sum_weight(self):
        user_department_weight = self.get_common_weight()
        result = {}

        for rated_user, judges  in user_department_weight.items():
            result[rated_user] = sum(judges.values())

        return result

    def calculate_weight_estimation(self,estimations):
        common_weight = self.get_common_weight()
        sum_weight = self.get_sum_weight()

        result = {}

        for rated_user, row in estimations.items():
            result[rated_user] = {}
            for judge in row.keys():
                result[rated_user][judge] = (estimations[rated_user][judge] *
                                             common_weight[rated_user][judge])/sum_weight[rated_user]

        for rated_user, judges  in result.items():
            result[rated_user] = round(sum(judges.values()),2)

        return result
