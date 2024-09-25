from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import *
from booths.models import *
from booths.serializers import *
from booths.views import *

# Create your views here.
class ReplyManageView(views.APIView):
    permission_classes = [IsAuthenticated]
    # 로그인하지 않으면 401 Unauthorized 뜸

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)

    def post(self, request, pk, guestbook_id, format=None):
        # 관리자인지 확인
        if not request.user.is_admin:
            return Response({"error": "해당 부스 관리자만 답글을 달 수 있습니다."}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        booth = self.get_object(pk)
        try:
            guestbook_entry = Guestbook.objects.get(id=guestbook_id, booth=booth)
        except Guestbook.DoesNotExist:
            return Response({"error": "해당 방명록 항목을 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReplySerializer(data=request.data, context={'request': request, 'guestbook_id': guestbook_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "답글 작성 성공!",
                             "data": serializer.data}, 
                            status=status.HTTP_201_CREATED)
        
        return Response({"error": "답글 작성 실패"}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, guestbook_id, format=None):
        booth = self.get_object(pk)
        try:
            guestbook_entry = Guestbook.objects.get(id=guestbook_id, booth=booth)
        except Guestbook.DoesNotExist:
            return Response({"error": "해당 방명록 항목을 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)
        
        replies = Reply.objects.filter(guestbook=guestbook_entry)
        serializer = ReplySerializer(replies, many=True)

        return Response({"message": "방명록 답글 가져오기 성공!", 
                         "data": serializer.data}, 
                         status=HTTP_200_OK)
    
class ReplyDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)

    def delete(self, request, pk, guestbook_id, reply_id):
        booth = self.get_object(pk)
        guestbook_entry = get_object_or_404(Guestbook, id=guestbook_id, booth=booth)
        reply_entry = get_object_or_404(Reply, id=reply_id, guestbook=guestbook_entry)

        if reply_entry.user != request.user:
            return Response({"error": "자신이 작성한 댓글만 삭제할 수 있습니다."}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        reply_entry.delete()
        return Response({"message": "답글 삭제 성공!"}, 
                        status=status.HTTP_204_NO_CONTENT)
from .models import *
from manages.serializers import *
from booths.serializers import *

class NoticeView(views.APIView):
  def post(self, request, pk):
    # 로그인이 되어있는지
    if not request.user.is_authenticated:
      return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

    booth = get_object_or_404(Booth, pk=pk)

    # 부스의 user가 내가 맞는지
    if request.user != booth.user:
      return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
    data = request.data
    data['booth'] = booth.id
    
    serializer = BoothNoticeSerializer(data = data)
    if serializer.is_valid():
      booth.increaseNoticeCount()
      serializer.save()
      return Response({'message': '공지를 등록했습니다.'}, status=HTTP_200_OK)
    
    else:
      return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class NoticeDeleteView(views.APIView):
  def delete(self, request, pk, info_id):
    if not request.user.is_authenticated:
      return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

    boothNotice = get_object_or_404(Booth_notice, pk=info_id)
    booth = get_object_or_404(Booth, pk=pk)

    # 부스의 user가 내가 맞는지
    if request.user != booth.user:
      return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
    booth.decreaseNoticeCount()
    boothNotice.delete()
    return Response({"message": "공지 삭제"}, status=HTTP_200_OK)
