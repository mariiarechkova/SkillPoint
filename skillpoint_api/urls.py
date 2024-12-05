from django.urls import path
from .views import DepartmentListCreate, DepartmentDetail, UserListCreate, UserDetail

urlpatterns = [
    path('departments/', DepartmentListCreate.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),
    path('users/', UserListCreate.as_view(), name='department-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='department-detail'),
]