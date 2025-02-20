from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('', UserList.as_view(), name='users-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('sign_up/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]