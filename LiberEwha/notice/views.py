from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notice
from .serializers import NoticeSerializer, NoticeListSerializer
from .pagination import NoticePagination
from django.db import models
from django.db.models import Q


class NoticeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.is_tf:
            serializer = NoticeSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class NoticeListView(APIView):
    pagination_class = NoticePagination

    def get(self, request):
        notice_type = request.query_params.get('type')  # 공지 유형을 쿼리로 받음
        notices = Notice.objects.all()  # 기본적으로 모든 공지 조회

        # 공지사항 필터링
        if notice_type in ['operational', 'event']:
            notices = notices.filter(notice_type=notice_type)
        elif notice_type:  # notice_type이 있지만 잘못된 값일 경우
            return Response({"detail": "유효하지 않은 타입입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 검색 기능 추가 (title 또는 content에 포함된 텍스트 검색)
        search_query = request.query_params.get('q')
        if search_query:
            notices = notices.filter(
                models.Q(title__icontains=search_query) | models.Q(
                    content__icontains=search_query)
            )

        paginator = self.pagination_class()
        paginated_notices = paginator.paginate_queryset(notices, request)
        serializer = NoticeListSerializer(paginated_notices, many=True)

        return paginator.get_paginated_response(serializer.data)


class NoticeDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            notice = Notice.objects.get(pk=pk)
            serializer = NoticeSerializer(notice)
            return Response(serializer.data)
        except Notice.DoesNotExist:
            return Response({"detail": "공지사항을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            notice = Notice.objects.get(pk=pk)
            if request.user.is_authenticated and request.user.is_tf:  # 인증된 사용자 및 is_tf 권한 확인
                serializer = NoticeSerializer(
                    notice, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "이 사용자에게는 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        except Notice.DoesNotExist:
            return Response({"detail": "공지사항을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            notice = Notice.objects.get(pk=pk)
            if request.user.is_authenticated and request.user.is_tf:  # 인증된 사용자 및 is_tf 권한 확인
                notice.delete()
                return Response({"detail": "삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "이 사용자에게는 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        except Notice.DoesNotExist:
            return Response({"detail": "공지사항을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
