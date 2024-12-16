from django.urls import path
from .views import DepartmentListCreate, DepartmentDetail, UserDetail, LoginView, ProtectedView, \
    UserList, RegistrationView

urlpatterns = [
    path('departments/', DepartmentListCreate.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),
    path('users/', UserList.as_view(), name='department-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='department-detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]