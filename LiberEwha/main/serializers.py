from rest_framework import serializers
from booths.models import Booth, Menu
from notice.models import Notice
from booths.serializers import BoothsMainSerializer, MenuMainSerializer
from shows.serializers import ShowsMainSerializer


class ScrapSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.CharField()
    type = serializers.CharField()  # 부스, 공연, 메뉴 타입 구분


class MainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth
        fields = ['id', 'name', 'thumbnail', 'category',
                  'booth_place', 'is_opened', 'scrap_count']


class SearchResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.CharField()
    description = serializers.CharField()
    type = serializers.CharField()  # 검색 타입 구분 (부스, 공연, 메뉴, 공지)
