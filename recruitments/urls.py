from django.urls import path

from recruitments.views      import CategoryView, RecruitmentsList

urlpatterns = [
    path("/categories", CategoryView.as_view()),
    path("", RecruitmentsList.as_view()),
]
