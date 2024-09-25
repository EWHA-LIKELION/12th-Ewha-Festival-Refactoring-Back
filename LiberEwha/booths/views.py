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
    
class BoothScrapView(views.APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)
        
        booth = get_object_or_404(Booth, pk=pk)

        data = {
            "booth": booth.id,
            "user": request.user.id
        }
        if Booth_scrap.objects.filter(booth=booth, user=request.user).exists():
            return Response({"message":"이미 스크랩 하셨습니다."}, status=HTTP_400_BAD_REQUEST)

        scrapSerializer = BoothScrapSerializer(data = data)
        if scrapSerializer.is_valid():
            booth.increaseScrapCount()
            scrapSerializer.save()
            return Response({'message': '스크랩 성공'}, status=HTTP_200_OK)
            
        else:
            return Response(scrapSerializer.errors, status=HTTP_400_BAD_REQUEST)
            
    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)
        
        if not Booth_scrap.objects.filter(booth=booth, user=request.user).exists():
            return Response({"message": "취소할 스크랩이 없습니다."}, status=HTTP_400_BAD_REQUEST)

        boothScrap = get_object_or_404(Booth_scrap, user=request.user.id, booth=pk)
        booth = get_object_or_404(Booth, pk=pk)

        booth.decreaseScrapCount()
        boothScrap.delete()
        return Response({"message": "스크랩 삭제"}, status=HTTP_200_OK)
        


class MenuScrapView(views.APIView):
    def post(self, request, pk, menu_id):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)
        
        menu = get_object_or_404(Menu, pk=menu_id)

        data = {
            "menu": menu.id,
            "user": request.user.id
        }

        if Menu_scrap.objects.filter(menu=menu, user=request.user).exists():
            return Response({"이미 스크랩 하셨습니다."}, status=HTTP_400_BAD_REQUEST)

        scrapSerializer = MenuScrapSerializer(data = data)
        if scrapSerializer.is_valid():
            menu.increaseScrapCount()
            scrapSerializer.save()
            return Response({'message': '스크랩 성공'}, status=HTTP_200_OK)
            
        else:
            return Response(scrapSerializer.errors, status=HTTP_400_BAD_REQUEST)
            
    def delete(self, request, pk, menu_id):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)
        
        menuScrap = get_object_or_404(Menu_scrap, user=request.user.id, menu=menu_id)
        menu = get_object_or_404(Menu, pk=menu_id)

        if not Booth_scrap.objects.filter(menu=menu, user=request.user).exists():
            return Response({"message": "취소할 스크랩이 없습니다."}, status=HTTP_400_BAD_REQUEST)


        menu.decreaseScrapCount()
        menuScrap.delete()
        return Response({"message": "스크랩 삭제"}, status=HTTP_200_OK)
        

