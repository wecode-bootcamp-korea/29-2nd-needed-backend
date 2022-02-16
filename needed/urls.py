from django.urls import path, include

urlpatterns = [
    path("recruitments", include("recruitments.urls")),
]
