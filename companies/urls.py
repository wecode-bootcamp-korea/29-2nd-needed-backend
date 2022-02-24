from django.urls import path

from companies.views      import CompanyView, CompanySearchView

urlpatterns = [
    path("/<int:company_id>", CompanyView.as_view()),
    path("", CompanySearchView.as_view()),
]
