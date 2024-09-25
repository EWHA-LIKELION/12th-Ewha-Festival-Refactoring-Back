from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import *
from .serializers import *
from manages.views import *

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

# 일반 사용자 방명록 작성 뷰
class GuestBookUserView(views.APIView):
    permission_classes = [IsAuthenticated]
    # 로그인하지 않으면 401 Unauthorized 뜸

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)

    def post(self, request, pk, format=None):
        if request.user.is_anonymous:
            return Response({"error": "로그인 후 방명록을 작성할 수 있습니다."}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        booth = self.get_object(pk)
        serializer = GuestBookSerializer(data=request.data, context={'request': request, 'booth_id': booth.id})

        if serializer.is_valid():
            guestbook_instance = serializer.save(user=user, booth=booth)
            response_serializer = GuestBookSerializer(guestbook_instance)
            return Response({"message": "방명록 작성 성공!", 
                             "data": response_serializer.data}, 
                            status=status.HTTP_201_CREATED)
        return Response({"error": "방명록 작성 실패"},
                         status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):
        booth = self.get_object(pk)
        guestbook= Guestbook.objects.filter(booth=booth)
        serializer = GuestBookSerializer(guestbook, many=True)
        return Response({"message": "부스 방명록 가져오기 성공!", 
                         "data": serializer.data}, 
                         status=HTTP_200_OK)

class GuestBookDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]
    # 로그인하지 않으면 401 Unauthorized 뜸

    def get_booth(self, pk):
        return get_object_or_404(Booth, pk=pk)
    
    def delete(self, request, pk, guestbook_id):
        booth = self.get_booth(pk)
        guestbook_entry = get_object_or_404(Guestbook, booth=booth, id=guestbook_id)

        if guestbook_entry.user != request.user:
            return Response({"error": "자신이 작성한 방명록만 삭제할 수 있습니다."}, 
                            status=status.HTTP_403_FORBIDDEN)

        guestbook_entry.delete()
        return Response({"message": "방명록 삭제 성공!"}, 
                        status=status.HTTP_204_NO_CONTENT)


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
        
        
        boothScrap = get_object_or_404(Booth_scrap, user=request.user.id, booth=pk)
        booth = get_object_or_404(Booth, pk=pk)

        if not Booth_scrap.objects.filter(booth=booth, user=request.user).exists():
            return Response({"message": "취소할 스크랩이 없습니다."}, status=HTTP_400_BAD_REQUEST)


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

        if not menuScrap.objects.filter(menu=menu, user=request.user).exists():
            return Response({"message": "취소할 스크랩이 없습니다."}, status=HTTP_400_BAD_REQUEST)


        menu.decreaseScrapCount()
        menuScrap.delete()
        return Response({"message": "스크랩 삭제"}, status=HTTP_200_OK)
        

