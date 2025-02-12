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
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='vote_events')
    created_at = models.DateTimeField(auto_now_add=True)

class VoteRound(models.Model):
    vote_event = models.ForeignKey(VoteEvent, on_delete=models.CASCADE, related_name='vote_rounds')
    stability = models.FloatField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()


class VoteRoundDetails(models.Model):
    estimation = models.FloatField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    vote_round = models.ForeignKey(VoteRound, on_delete=models.CASCADE, related_name='vote_rounds')
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='round_details')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_round_details')

class VoteRoundUserReport(models.Model):
    vote_round = models.ForeignKey(VoteRound, on_delete=models.CASCADE, related_name='vote_round_reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='round_reports')
    percent_bonus = models.DecimalField(max_digits=12, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)
