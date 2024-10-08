from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from manages.serializers import *

# Create your views here.
class ShowsDetailView(views.APIView): #부스 상세 페이지
    permission_classes = [IsAuthenticatedOrReadOnly] #모든 사용자 읽기권한, 부스 운영자 쓰기권한

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)

    def get(self, request, pk):
        show = get_object_or_404(Booth, pk=pk)
        serializer= ShowsDetailSerializer(show)

        data = serializer.data

        booth = get_object_or_404(Booth, pk = pk)
        boothSerializer = BoothNoticeCountSerializer(booth)

        notice_list = {}

        notices = Booth_notice.objects.filter(booth = pk)
        i=0
        for notice in notices:
            i += 1
            noticeSerializer = BoothNoticeSerializer(notice)
            notice_list[i] = noticeSerializer.data


        data['notice'] = notice_list

        return Response({'message': '공연 상세 조회 성공',
                        'data': data},
                        status=HTTP_200_OK)

class ShowsMainView(views.APIView): #부스 목록 페이지
    serializer_class = ShowsMainSerializer

    def get(self, request):
        category = request.GET.get('category')
        place = request.GET.get('place')
        dayofweek = request.GET.get('dayofweek')
        is_show= request.GET.get('is_show')

        # 부스 정렬 기준
        shows = Booth.objects.all()

        shows = shows.filter(is_show = True)

        if category :
            if category is not None:
                shows = shows.filter(category=category)

        if dayofweek:  # dayofweek가 요청되면
            shows = shows.filter(days__dayofweek=dayofweek)

        shows = shows.order_by("id") #오름차순 정렬
        serializer = ShowsMainSerializer(shows, many=True)

        data = serializer.data

        for booth in data:
            booth_id = booth['id']
            is_scraped = Booth_scrap.objects.filter(user=request.user, booth_id=booth_id).exists()
            booth['is_scraped'] = is_scraped
        return Response({'message': "공연 목록 불러오기 성공!",
                         'data': serializer.data},
                        status=HTTP_200_OK)