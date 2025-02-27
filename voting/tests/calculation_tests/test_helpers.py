from django.test import TestCase
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from organisations.models import Organisation, Department, DepartmentWeight
from users.models import User, Profile
from voting.models import VoteEvent, VoteRound, VoteRoundDetails

class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organisation = Organisation.objects.create(name="Test Organisation")

        cls.department1 = Department.objects.create(title = "IT", organisation = cls.organisation)
        cls.department2 = Department.objects.create(title="management", organisation=cls.organisation)
        cls.department3 = Department.objects.create(title="accounting", organisation=cls.organisation)

        cls.vote_event = VoteEvent.objects.create(
            frequency='month',
            start_day=1,
            end_day=15,
            organisation=cls.organisation
        )

        cls.vote_round = VoteRound.objects.create(
            vote_event=cls.vote_event,
            start_at=timezone.now(),
            end_at=timezone.now() + relativedelta(months=6)
        )

        user_data = [
            ("Jane", "Smith", "jane@example.com", cls.department1, 3),
            ("John", "Doe", "john@example.com", cls.department1, 6),
            ("Alice", "Brown", "alice@example.com", cls.department1, 3),
            ("Bob", "White", "bob@example.com", cls.department1, 3),
            ("Charlie", "Black", "charlie@example.com", cls.department2, 3),
            ("Eva", "Green", "eva@example.com", cls.department3, 3),
        ]

        cls.users = []
        for i, (first_name, last_name, email, department, weight_vote) in enumerate(user_data, start=1):
            user = User.objects.create(
                id=i,
                first_name=first_name,
                last_name=last_name,
                email=email,
                organisation=cls.organisation,
                department = department,
                weight_vote = weight_vote,
                password="password123",
            )
            setattr(cls, f"user{i}", user)
            cls.users.append(user)

        Profile.objects.create(user=cls.user1, salary=450)
        Profile.objects.create(user=cls.user2, salary=580)
        Profile.objects.create(user=cls.user3, salary=450)
        Profile.objects.create(user=cls.user4, salary=480)
        Profile.objects.create(user=cls.user5, salary=600)
        Profile.objects.create(user=cls.user6, salary=500)

        estimations = {
            cls.user1.id: [6, 5, 5, 6],
            cls.user2.id: [6, 4, 4, 5, 4],
            cls.user3.id: [5, 7, 5, 6],
            cls.user4.id: [4, 5, 5, 5, 5],
            cls.user5.id: [4, 5, 4, 4, 6],
            cls.user6.id: [5, 5, 5, 5, 6]
        }

        votes = []
        for judge in cls.users:
            rated_users = [user for user in cls.users if user != judge]
            for rated_user, estimation in zip(rated_users, estimations[judge.id]):
                votes.append(VoteRoundDetails(
                    estimation=estimation,
                    judge=judge,
                    rated_user=rated_user,
                    vote_round=cls.vote_round
                ))

        VoteRoundDetails.objects.bulk_create(votes)

        DepartmentWeight.objects.create(
            judge_department = cls.department2,
            rated_department = cls.department1,
            weight_vote = 10)

        DepartmentWeight.objects.create(
            judge_department = cls.department2,
            rated_department = cls.department3,
            weight_vote = 6)

        DepartmentWeight.objects.create(
            judge_department = cls.department1,
            rated_department = cls.department2,
            weight_vote = 10)

        DepartmentWeight.objects.create(
            judge_department = cls.department1,
            rated_department = cls.department3,
            weight_vote = 10)

        DepartmentWeight.objects.create(
            judge_department = cls.department3,
            rated_department = cls.department2,
            weight_vote = 6)

        DepartmentWeight.objects.create(
            judge_department = cls.department3,
            rated_department = cls.department1,
            weight_vote = 10)
