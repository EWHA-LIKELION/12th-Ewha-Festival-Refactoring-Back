from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import redirect    
from rest_framework_simplejwt.tokens import AccessToken          
from allauth.socialaccount.providers.kakao import views as kakao_views 
import requests                       
from django.shortcuts import redirect 
from .models import User  
from django.http import JsonResponse
import jwt, logging


class SignUpView(views.APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # user를 저장
            token = RefreshToken.for_user(user)  # 저장된 user로 토큰 생성

            return Response({
                'message': '회원가입 성공',
                'data': serializer.data,
                'token': str(token.access_token),
                'refresh_token': str(token)
            }, status=status.HTTP_201_CREATED)
        return Response({'message': '회원가입 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': '로그인 성공', 'data': serializer.validated_data})
        return Response({'message': '로그인 실패', 'error': serializer.errors})

# code 요청

# def kakao_login(request):
#     app_rest_api_key = '41c26ffbb480fe0fe222568af308ede8'
#     redirect_uri = "http://127.0.0.1:8000" + "/accounts/login/kakao/callback/"
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
#     )

class KakaoLoginView(views.APIView):
    def get(self, request):
        client_id = '41c26ffbb480fe0fe222568af308ede8'
        redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback/"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
        
class KakaoLoginCallbackView(views.APIView):
    SECRET_KEY = '1139200'

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"message": "코드가 제공되지 않았습니다."}, status=400)

        client_id = '41c26ffbb480fe0fe222568af308ede8'
        redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback/"

        # Access Token 요청
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )

        token_json = token_request.json()
        logging.info(f"Kakao token response: {token_json}")  # 응답 로그 추가

        if token_request.status_code != 200 or "access_token" not in token_json:
            return JsonResponse({"message": "INVALID_CODE"}, status=400)

        access_token = token_json["access_token"]

        # 사용자 정보 요청
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        logging.info(f"Kakao profile response: {profile_json}")  # 응답 로그 추가

        if profile_request.status_code != 200:
            return JsonResponse({"message": "사용자 프로필 요청 실패", "error": profile_json}, status=400)

        kakao_account = profile_json.get("kakao_account")
        if kakao_account is None:
            return JsonResponse({"message": "Kakao 계정 정보가 없습니다."}, status=400)

        nickname = kakao_account.get("profile", {}).get("nickname")
        id = profile_json.get("id")

        if not nickname or not id:
            return JsonResponse({"message": "Kakao 계정 정보가 부족합니다.", "kakao_account": kakao_account, "profile_json": profile_json}, status=400)

        # 사용자 데이터 처리
        user, created = User.objects.get_or_create(
            id=id,  # 사용자 ID
            defaults={'nickname': nickname}
        )

        # JWT 생성
        token = AccessToken.for_user(user)  # Simple JWT를 사용하여 토큰 생성

        return JsonResponse({"token": str(token)}, status=200)