
def get_awards(estimations, stability, salary):
        stable_estimates  = {}
        for user, estimation in estimations.items():
            if estimation > 2:
                estimation -= 2
            stable_estimates [user] = round(estimation ** stability, 4)

        sum_stable_estimates = sum(stable_estimates.values())

        weight_with_salary = {}

        for user, estimation in stable_estimates.items():
            weight_with_salary[user] = round(stable_estimates [user] * salary[user] / sum_stable_estimates, 3)

        sum_weight_with_salary = sum(weight_with_salary.values())

        result = {}

        for user, weight in weight_with_salary.items():
            result[user] = round(weight / sum_weight_with_salary, 4)

        total = sum(result.values())

        if total < 1:
            difference = 1 - total
            for item in result.keys():
                result[item] += difference / len(result)
        elif total > 1:
            difference = total - 1
            for item in result.keys():
                result[item] -= difference / len(result)

        return result