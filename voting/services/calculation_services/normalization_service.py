from django.contrib.postgres.aggregates import ArrayAgg
from voting.models import VoteRoundDetails

class NormalizationService:
    def __init__(self):
        self.judge_estimations = JudgeEstimationsRepository.get_judges_with_estimations()
        self.rated_estimations = RatedUserEstimationsRepository.get_rated_users_with_estimations()

    def calculate_normalization_coefficient(self):
        if not self.judge_estimations:
            raise ValueError("The estimations data is empty.")
        normalization_coefficients = {}

        for judge_id, estimations in self.judge_estimations.items():
            normalization_coefficients[judge_id] = round(((len(estimations) + 1) * 5) / (sum(estimations) + 5), 4)

        return normalization_coefficients

    def calculate_updated_estimations(self):
        normalization_coefficients = self.calculate_normalization_coefficient()
        rated_estimations = self.rated_estimations
        for key in normalization_coefficients.keys():
            for rated_user, row in rated_estimations.items():
                if key == rated_user and key not in row.keys():
                    row[key] = 5.0


        updated_estimations = {}

        for rated_user, judges in rated_estimations.items():
            updated_estimations[rated_user] = {}
            for key in judges.keys() & normalization_coefficients.keys():
                updated_estimations[rated_user][key] = round((judges[key] * normalization_coefficients[key]),2)

        return updated_estimations

class JudgeEstimationsRepository:
    @staticmethod
    def get_judges_with_estimations():
        estimations_list = VoteRoundDetails.objects.values('judge__id').annotate(estimation = ArrayAgg('estimation'))
        estimations = {item['judge__id']: item['estimation'] for item in estimations_list}
        return estimations

class RatedUserEstimationsRepository:
    @staticmethod
    def get_rated_users_with_estimations():
        estimations_list = (VoteRoundDetails.objects.values('rated_user__id', 'judge__id', 'estimation').
                            order_by('rated_user__id', 'judge__id'))

        rated_user_estimations = {}
        for item in estimations_list:
            rated_user_id = item['rated_user__id']
            judge_id = item['judge__id']
            estimation = item['estimation']

            # Grouping by rated_user_id
            if rated_user_id not in rated_user_estimations:
                rated_user_estimations[rated_user_id] = {}

            rated_user_estimations[rated_user_id][judge_id] = estimation

        return rated_user_estimations