from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from voting.models import VoteRoundDetails, VoteRound


class AvailableUsersService:
    def __init__(self, vote_event, user):
        self.vote_round = VoteRoundService.actual_round(vote_event)
        self.user = user


    def is_user_voted(self):
        """Checks whether the user has voted on this vote.
        Returns True if the user has already voted, otherwise False."""

        try:
            VoteRoundDetails.objects.get(vote_round = self.vote_round, judge = self.user)
            return True
        except ObjectDoesNotExist:
            return False

    def is_eligible_user_vote(self):
        return False if self.is_user_voted() else True


class VoteRoundService:
    @staticmethod
    def actual_round(vote_event):
        vote_round = VoteRound.objects.filter(vote_event=vote_event).first()
        return vote_round

class ParticipantService:
    @staticmethod
    def get_available_users_for_voting(organisation, user):
        """Retrieves the list of the organization's users, except for the current user."""
        return User.objects.filter(organisation=organisation).exclude(id=user.id)