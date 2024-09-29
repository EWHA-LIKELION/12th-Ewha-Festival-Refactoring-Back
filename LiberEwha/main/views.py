from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from booths.models import *
from notice.models import *
from shows.models import Booth as Show
from .serializers import *


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


class ScrapListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        booth_scraps = Booth_scrap.objects.filter(user=request.user)
        menu_scraps = Menu_scrap.objects.filter(user=request.user)
        show_scraps = Booth_scrap.objects.filter(
            user=request.user, booth__is_show=True)

        booth_data = ScrapSerializer(
            booth_scraps, many=True, context={'type': 'booth'}).data
        menu_data = ScrapSerializer(
            menu_scraps, many=True, context={'type': 'menu'}).data
        show_data = ScrapSerializer(
            show_scraps, many=True, context={'type': 'show'}).data

        return Response({
            'booths': booth_data,
            'menus': menu_data,
            'shows': show_data,
        }, status=200)


class SearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q')
        booth_results = Booth.objects.filter(
            name__icontains=query) | Booth.objects.filter(description__icontains=query)
        menu_results = Menu.objects.filter(menu__icontains=query)
        notice_results = Notice.objects.filter(
            title__icontains=query) | Notice.objects.filter(content__icontains=query)

        booth_data = SearchResultSerializer(
            booth_results, many=True, context={'type': 'booth'}).data
        menu_data = SearchResultSerializer(
            menu_results, many=True, context={'type': 'menu'}).data
        notice_data = SearchResultSerializer(
            notice_results, many=True, context={'type': 'notice'}).data

        return Response({
            'booths': booth_data,
            'menus': menu_data,
            'notices': notice_data
        }, status=200)
