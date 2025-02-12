from django.test import TestCase
from organisations.models import Organisation
from voting.models import VoteEvent, VoteRound
from voting.services.vote_round_create_service import create_vote_round

class VoteRoundServicesTest(TestCase):
    def setUp(self):
        # Creating test data
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.vote_event = VoteEvent.objects.create(
            frequency='month',
            start_day=1,
            end_day=15,
            organisation=self.organisation
        )

    def test_create_vote_round(self):
        # Creating a voting round
        vote_round = create_vote_round(self.vote_event.id)

        # check that the returned object is an instance of the Vote Round class.
        self.assertIsInstance(vote_round, VoteRound)
        self.assertEqual(vote_round.vote_event.id, self.vote_event.id)