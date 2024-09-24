from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *

# Create your views here.
class BoothsDetailView(views.APIView): #부스 상세 페이지
    permission_classes = [IsAuthenticatedOrReadOnly] #모든 사용자 읽기권한, 부스 운영자 쓰기권한

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)
    
    def get(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        serializer= BoothsDetailSerializer(booth)
        
        return Response({'message': '부스 상세 조회 성공',
                        'data': serializer.data},
                        status=HTTP_200_OK)

class BoothsMainView(views.APIView): #부스 목록 페이지
    serializer_class = BoothsMainSerializer

    def get(self, request):
        category = request.data.get('category')
        place = request.data.get('place')
        date = request.data.get('date')
        is_show= request.data.get('is_show')

        # 부스 정렬 기준 추가
        booths = Booth.objects.all()
        if is_show and is_show != True:
            booths = booths.filter(is_show = True)

        if place and place != "null":
                booths = booths.filter(place=place)

        booths = booths.order_by("id") #오름차순 정렬
        serializer = BoothsMainSerializer(booths, many=True)
        return Response({'message': "부스 목록 불러오기 성공!",
                         'data': serializer.data},
                        status=HTTP_200_OK)