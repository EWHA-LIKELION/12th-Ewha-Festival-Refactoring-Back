from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('check-username/', UsernameCheckView.as_view(), name='check_username'),

    path('login/kakao/', KakaoLoginView.as_view()),
    path('login/kakao/callback/', KakaoLoginCallbackView.as_view()),
]
