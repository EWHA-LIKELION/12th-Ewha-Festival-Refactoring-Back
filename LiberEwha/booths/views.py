from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import *

from notice.models import *
from notice.serializers import *

from .serializers import *
from manages.views import *
from manages.serializers import *

# Create your views here.
class BoothsDetailView(views.APIView): #부스 상세 페이지
    permission_classes = [IsAuthenticatedOrReadOnly] #모든 사용자 읽기권한, 부스 운영자 쓰기권한

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)
    
    def get(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        serializer= BoothsDetailSerializer(booth)
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
        
        return Response({'message': '부스 상세 조회 성공',
                        'data': data},
                        status=HTTP_200_OK)

class BoothsMainView(views.APIView): #부스 목록 페이지
    serializer_class = BoothsMainSerializer

    def get(self, request):
        category = request.GET.get('category')
        place = request.GET.get('place')
        dayofweek = request.GET.get('dayofweek')
        is_show= request.GET.get('is_show')

        # 부스 정렬 기준
        booths = Booth.objects.all()
        booths = booths.filter(is_show = False)

        if category:
                booths = booths.filter(category=category)

        if dayofweek:  # dayofweek가 요청되면
            booths = booths.filter(days__dayofweek=dayofweek)

        booths = booths.order_by("id") #오름차순 정렬
        serializer = BoothsMainSerializer(booths, many=True)
        return Response({'message': "부스 목록 불러오기 성공!",
                         'data': serializer.data},
                        status=HTTP_200_OK)
    

# 일반 사용자 방명록 작성 뷰
class GuestBookUserView(views.APIView):

    def get_object(self, pk):
        try:
            return Booth.objects.get(pk=pk)
        except Booth.DoesNotExist:
            raise NotFound("부스를 찾을 수 없습니다.")

    def post(self, request, pk, format=None):
        if request.user.is_anonymous:
            return Response({"error": "로그인 후 방명록을 작성할 수 있습니다."}, 
                            status=HTTP_401_UNAUTHORIZED)
        user = request.user
        try:
            booth = self.get_object(pk)
        except NotFound as e:
            return Response({"error": str(e)}, 
                            status=HTTP_404_NOT_FOUND)
        serializer = GuestBookSerializer(data=request.data, context={'request': request, 'booth_id': booth.id})

        if serializer.is_valid():
            guestbook_instance = serializer.save(user=user, booth=booth)
            response_serializer = GuestBookSerializer(guestbook_instance)
            return Response({"message": "방명록 작성 성공!", 
                             "data": response_serializer.data}, 
                            status=HTTP_201_CREATED)
        return Response({"error": "방명록 작성 실패"},
                         status=HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):

        if not request.user.is_authenticated:
            return Response({"error": "로그인 후 방명록을 가져올 수 있습니다."},
                             status=HTTP_401_UNAUTHORIZED)

        try:
            booth = self.get_object(pk)
        except NotFound as e:
            return Response({"error": str(e)}, 
                            status=HTTP_404_NOT_FOUND)

        guestbook= Guestbook.objects.filter(booth=booth)
        serializer = GuestBookSerializer(guestbook, many=True)
        return Response({"message": "부스 방명록 가져오기 성공!", 
                         "data": serializer.data}, 
                         status=HTTP_200_OK)

class GuestBookDeleteView(views.APIView):

    def get_object(self, pk):
        try:
            return Booth.objects.get(pk=pk)
        except Booth.DoesNotExist:
            raise NotFound("부스를 찾을 수 없습니다.")
    
    def delete(self, request, pk, guestbook_id):
        if not request.user.is_authenticated:
            return Response({"error": "로그인 후 방명록 기능을 사용할 수 있습니다."},
                             status=HTTP_401_UNAUTHORIZED)

        try:
            booth = self.get_object(pk)
        except NotFound as e:
            return Response({"error": str(e)}, 
                            status=HTTP_404_NOT_FOUND)
        
        guestbook_entry = get_object_or_404(Guestbook, booth=booth, id=guestbook_id)

        if guestbook_entry.user != request.user:
            return Response({"error": "자신이 작성한 방명록만 삭제할 수 있습니다."}, 
                            status=HTTP_403_FORBIDDEN)

        guestbook_entry.delete()
        return Response({"message": "방명록 삭제 성공!"}, 
                        status=HTTP_204_NO_CONTENT)


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


class BoothsTFView(views.APIView): #축제일정페이지 - TF 
    def get(self, request):
        booth_category = request.GET.get('booth_category')
        dayofweek = request.GET.get('dayofweek')

        boothshow = Booth.objects.all()
        shows = boothshow.filter(is_show=True)
        booths = boothshow.filter(is_show=False)

        if dayofweek:  # dayofweek가 요청되면
            shows = shows.filter(days__dayofweek=dayofweek)

        if booth_category:
            booths = booths.filter(booth_category=booth_category)

        shows = shows.order_by('id')
        booths = booths.order_by('id')

        showserializer = BoothsTFSerializer(shows, many=True)
        boothserializer = BoothsTFSerializer(booths, many=True)
        return Response({'message': "TF 축제 일정 불러오기 성공!",
                         'show': showserializer.data,
                         'booth': boothserializer.data},
                        status=HTTP_200_OK)

class BoothsTFDetailView(views.APIView): #축제일정상세페이지 - TF
    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)
    
    def get(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk)
        boothSerializer= BoothsTFDetailSerializer(booth)   

        notices = Notice.objects.all()
        noticeSerializer = NoticeListSerializer(notices, many=True)

        return Response({'message': '부스 상세 조회 성공',
                        'data': boothSerializer.data,
                        'notice': noticeSerializer.data},
                        status=HTTP_200_OK)