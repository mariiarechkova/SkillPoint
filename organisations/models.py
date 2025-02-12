from django.db import models

class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stability = models.FloatField(blank=True, default=1.5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class DepartmentWeight(models.Model):
    judge_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='judging_weights')
    rated_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rated_weights')
    weight_vote = models.FloatField()