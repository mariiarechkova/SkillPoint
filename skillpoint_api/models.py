from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.db import models

class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class VoteEvent(models.Model):
    class Frequency(models.TextChoices):
        WEEK = 'week', _('Week')
        MONTH = 'month', _('Month')
        QUARTER = 'quarter', _('Quarter')
        YEAR = 'year', _('Year')

    frequency = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.MONTH)
    start_day = models.IntegerField(default=1, blank=True)
    end_day = models.IntegerField(default=15, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def is_authenticated(self):
        True


    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class VoteDetails(models.Model):
    estimation = models.FloatField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vote_event = models.ForeignKey(VoteEvent, on_delete=models.CASCADE, related_name='vote_event')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated_user')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='judge')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.CharField(null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    salary = models.CharField(max_length=20, null=True, blank=True)
    start_work_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Bonus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)


class Role(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)