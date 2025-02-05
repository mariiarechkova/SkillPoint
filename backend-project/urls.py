
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/organisations/", include("organisations.urls")),
    path("api/users/", include('users.urls')),
    path("api/voting", include('voting.urls'))
]
