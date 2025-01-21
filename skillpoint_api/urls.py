from django.urls import path
from skillpoint_api.views.departments import *
from skillpoint_api.views.metrics import MetricsStaffView, MetricsVoteView
from skillpoint_api.views.organisations import OrganisationsView
from skillpoint_api.views.users import *
from skillpoint_api.views.registration import *
from skillpoint_api.views.vote_events import *



urlpatterns = [
    path('organisations/', OrganisationsView.as_view(), name='organisations-list'),
    path('departments/', DepartmentListCreate.as_view(), name='departments-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),
    path('users/', UserList.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('sign_up/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('users/available-to-vote/', AvailibleUsers.as_view(), name='available-to-vote'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('vote-events/', VoteEventsView.as_view(), name='vote-events-list'),
    path('vote-events/<int:pk>/', VoteEventsView.as_view(), name='vote-events-list'),
    path('vote-events/<int:pk>/details/', VoteDetailsView.as_view(), name='vote-details'),
    path('metrics/staff/', MetricsStaffView.as_view(), name='metrics-staff'),
    path('metrics/vote/', MetricsVoteView.as_view(), name='metrics-vote')
]