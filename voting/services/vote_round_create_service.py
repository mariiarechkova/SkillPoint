from django.utils import timezone
from dateutil.relativedelta import relativedelta
from voting.models import VoteRound, VoteEvent


def create_vote_round(vote_event_id):
    current_datetime = timezone.now()
    end_date = current_datetime + relativedelta(months=+6)

    try:
        vote_event = VoteEvent.objects.get(id=vote_event_id)
    except:
        raise ValueError(f"VoteEvent with id {vote_event_id} not found.")

    vote_round = VoteRound.objects.create(
        vote_event = vote_event,
        start_at = current_datetime,
        end_at =end_date
    )
    return vote_round