from django.urls import path

from users.views import KakaoSignInView, KakaoCallBackView, ProfileView, SalaryView

urlpatterns = [
    path('/signin/kakao',KakaoSignInView.as_view()),
    path('/signin/kakao/callback',KakaoCallBackView.as_view()),
    path('/profile',ProfileView.as_view()),
    path('/salary/<int:occupation_id>',SalaryView.as_view()),
]
