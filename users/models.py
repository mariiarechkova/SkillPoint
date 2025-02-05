from django.contrib.auth.models import AbstractUser
from django.db import models

from organisations.models import Organisation, Department


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='users')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.CharField(null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    salary = models.CharField(max_length=20, null=True, blank=True)
    start_work_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

