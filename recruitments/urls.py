from django.urls import path

from .views      import *

urlpatterns = [
    path("/categories", CategoryView.as_view()),
]
