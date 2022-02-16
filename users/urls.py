from django.urls import path

from users.views import KakaoSignInView, KakaoCallBackView

urlpatterns = [
    path('/signin/kakao',KakaoSignInView.as_view()),
    path('/signin/kakao/callback',KakaoCallBackView.as_view()),
]
