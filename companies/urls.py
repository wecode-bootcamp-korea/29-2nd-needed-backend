from django.urls import path

from companies.views      import CompanyView

urlpatterns = [
    path("/<int:company_id>", CompanyView.as_view()),
]
