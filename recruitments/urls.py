from django.urls import path

from recruitments.views      import CategoryView, RecruitmentsList, RecruitmentsDetailView, SubCategoryView, ApplicationView


urlpatterns = [
    path("/categories", CategoryView.as_view()),
    path("", RecruitmentsList.as_view()),
    path("/<int:recruitment_id>",RecruitmentsDetailView.as_view()),
    path("/subcategories", SubCategoryView.as_view()),
    path("/applications/<int:recruitment_id>", ApplicationView.as_view()),
]
