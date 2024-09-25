from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notice
from .serializers import NoticeSerializer, NoticeListSerializer
from .pagination import NoticePagination

class NoticeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.is_tf:
            serializer = NoticeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail" : "이 사용자에게는 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)




class NoticeListView(APIView):
    def get(self, request):
        notices = Notice.objects.all()
        serializer = NoticeListSerializer(notices, many=True)  
        return Response(serializer.data)
    

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
                serializer = NoticeSerializer(notice, data=request.data, partial=True)
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
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "이 사용자에게는 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        except Notice.DoesNotExist:
            return Response({"detail": "공지사항을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

