from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken


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
