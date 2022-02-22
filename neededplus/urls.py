from django.urls import path

from neededplus.views      import NeededPlusSubscription

urlpatterns = [
    path("", NeededPlusSubscription.as_view()),
]
