from rest_framework import serializers
from .models import Booth_scrap, Menu_scrap, Booth
from .serializers import BoothsMainSerializer, MenuMainSerializer, ShowsMainSerializer


# 부스/공연/메뉴 구분하기 위해 type도 리턴하게 함

class UserBoothScrapSerializer(serializers.ModelSerializer):
    booth = BoothsMainSerializer(read_only=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = Booth_scrap
        fields = ['booth', 'type']

    def get_type(self, obj):
        return 'booth'

class UserMenuScrapSerializer(serializers.ModelSerializer):
    menu = MenuMainSerializer(read_only=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = Menu_scrap
        fields = ['menu', 'type']

    def get_type(self, obj):
        return 'menu'

class UserShowScrapSerializer(serializers.ModelSerializer):
    booth = ShowsMainSerializer(read_only=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = Booth_scrap
        fields = ['booth', 'type']

    def get_type(self, obj):
        return 'show'
