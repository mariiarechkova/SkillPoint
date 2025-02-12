from django.urls import path
from .views import MetricsStaffView, MetricsVoteView, VoteEventsView, VoteRoundDetailsView, AvailableUsers

urlpatterns = [
    path('vote-events/', VoteEventsView.as_view(), name='vote-events-list'),
    path('vote-events/<int:pk>/', VoteEventsView.as_view(), name='vote-events-list'),
    path('vote-events/<int:pk>/details/', VoteRoundDetailsView.as_view(), name='vote-details'),
    path('metrics/staff/', MetricsStaffView.as_view(), name='metrics-staff'),
    path('metrics/vote/', MetricsVoteView.as_view(), name='metrics-vote'),
    path('vote-events/<int:pk>/users/', AvailableUsers.as_view(), name='available-to-vote'),
]