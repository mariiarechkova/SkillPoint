from django.urls import path
from .views import OrganisationsView, DepartmentListCreate, DepartmentDetail

urlpatterns = [
    path('', OrganisationsView.as_view(), name='organisations-list'),
    path('departments/', DepartmentListCreate.as_view(), name='departments-list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail')
]