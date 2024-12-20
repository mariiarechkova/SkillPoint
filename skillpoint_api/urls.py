from django.urls import path
from .views import DepartmentListCreate, DepartmentDetail, LoginView, ProtectedView, \
    UserList, RegistrationView, AvailibleUsers, ProfileView, UserDetailView, VoteEventsView, VoteDetailsView

urlpatterns = [
    path('departments/', DepartmentListCreate.as_view(), name='departments-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),
    path('users/', UserList.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('users/available-to-vote/', AvailibleUsers.as_view(), name='available-to-vote'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('vote-events/', VoteEventsView.as_view(), name='vote-events-list'),
    path('vote-events/<int:pk>/', VoteEventsView.as_view(), name='vote-events-list'),
    path('vote-events/<int:pk>/details/', VoteDetailsView.as_view(), name='vote-details'),
]