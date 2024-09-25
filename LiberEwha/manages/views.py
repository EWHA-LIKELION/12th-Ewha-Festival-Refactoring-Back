from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
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