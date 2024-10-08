from booths.serializers import BoothsMainSerializer
from booths.models import Booth_scrap
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from booths.models import *
from notice.models import *
from shows.models import Booth as Show
from .serializers import *
from django.shortcuts import render
from booths.serializers import BoothScrapSerializer
from django.db.models import Q


class MainPageView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        if request.user.is_authenticated:
            # 로그인한 사용자라면 스크랩한 항목을 포함해서 보여줌
            user_scraped_booths = Booth_scrap.objects.filter(
                user=request.user).values_list('booth', flat=True)
            user_scraped_menus = Menu_scrap.objects.filter(
                user=request.user).values_list('menu__booth', flat=True)
            user_scraped_shows = Booth_scrap.objects.filter(
                user=request.user, booth__is_show=True).values_list('booth', flat=True)

            booths = Booth.objects.exclude(
                id__in=user_scraped_booths).order_by('id')[:5]
            shows = Show.objects.exclude(
                id__in=user_scraped_shows).order_by('id')[:5]

            serializer = MainPageSerializer(booths, many=True)




            return Response({'booths': serializer.data}, status=200)
        else:
            # 로그인하지 않은 사용자
            booths = Booth.objects.filter(is_show=False).order_by('id')[:5]
            shows = Show.objects.filter(is_show=True).order_by('id')[:5]

            serializer = MainPageSerializer(booths, many=True)
            

            return Response({'booths': serializer.data}, status=200)


# 스크랩 조회 뷰
class ScrapListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자가 스크랩한 모든 부스와 공연을 가져옴
        all_scraps = Booth_scrap.objects.filter(user=request.user)

        # 일반 부스 (is_show=False)와 공연 (is_show=True)으로 구분
        booth_scraps = all_scraps.filter(booth__is_show=False)
        show_scraps = all_scraps.filter(booth__is_show=True)

        # 시리얼라이징
        booth_data = MainPageSerializer(
            [scrap.booth for scrap in booth_scraps], many=True).data
        show_data = MainPageSerializer(
            [scrap.booth for scrap in show_scraps], many=True).data

        return Response({
            'message': '스크랩 조회 성공',
            'booths': booth_data,
            'shows': show_data
        }, status=200)


class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')

        # Booth, Menu, Notice에 대한 검색을 각각 필터링
        booth_results = Booth.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        menu_results = Menu.objects.filter(
            Q(menu__icontains=query) | Q(booth__name__icontains=query)
        )
        notice_results = Notice.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        # 각 검색 결과에 대해 시리얼라이저 적용
        booth_data = SearchResultSerializer(booth_results, many=True).data

        for booth in booth_data:
            booth_id = booth['id']
            is_scraped = Booth_scrap.objects.filter(user=request.user, booth_id=booth_id).exists()
            booth['is_scraped'] = is_scraped


        menu_data = SearchResultSerializer(menu_results, many=True).data
        notice_data = SearchResultSerializer(notice_results, many=True).data

        return Response({
            'booths': booth_data,
            'menus': menu_data,
            'notices': notice_data
        }, status=200)
