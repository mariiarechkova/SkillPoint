from django.contrib.postgres.aggregates import ArrayAgg
from voting.models import VoteRoundDetails

class NormalizationService:
    def __init__(self):
        self.estimations = EstimationsRepository.get_judges_with_estimations()

    def calculate_normalization_coefficient(self):
        if not self.estimations:
            raise ValueError("The estimations data is empty.")
        normalization_coefficients = {}

        for judge_id, estimations in self.estimations.items():
            normalization_coefficients[judge_id] = round(((len(estimations) + 1) * 5) / (sum(estimations) + 5), 4)

        return normalization_coefficients

class EstimationsRepository:
    @staticmethod
    def get_judges_with_estimations():
        estimations_list = VoteRoundDetails.objects.values('judge__id').annotate(estimation = ArrayAgg('estimation'))
        estimations = {item['judge__id']: item['estimation'] for item in estimations_list}
        return estimations
