from django.contrib.auth.models import AbstractUser
from django.db import models

from organisations.models import Organisation, Department


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='users')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    username = None
    is_finish_sign_up = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    weight_vote = models.FloatField(null=True, blank=True)
    role = models.ManyToManyField('Role', related_name='users', blank=True)
    is_approve_role = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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

class Role(models.Model):
    title = models.CharField(max_length=255, unique=True)
    weight_vote = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

class Permission(models.Model):
    title = models.CharField(max_length=255, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Bonus(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonuses')

    def __str__(self):
        return self.title

