from django.urls import path
from .views import *

urlpatterns = [
    path('', UserList.as_view(), name='users-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('sign_up/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('available-to-vote/', AvailibleUsers.as_view(), name='available-to-vote'),
    path('profile/', ProfileView.as_view(), name='profile'),
]