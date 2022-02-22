from django.urls import path, include

urlpatterns = [
    path("recruitments", include("recruitments.urls")),
    path('users',include('users.urls')),
    path('companies',include('companies.urls')),
]
