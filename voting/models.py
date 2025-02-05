from django.db import models
from django.utils.translation import gettext_lazy as _
from organisations.models import Organisation
from users.models import User


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

class VoteDetails(models.Model):
    estimation = models.FloatField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vote_event = models.ForeignKey(VoteEvent, on_delete=models.CASCADE, related_name='vote_event')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated_user')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='judge')

