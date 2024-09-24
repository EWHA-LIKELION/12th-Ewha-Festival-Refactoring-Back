from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class BoothsMainSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booth
        fields = ['id', 'name', 'category', 'thumbnail', 'is_opened', 'place'] 

class MenuMainSerializer(serializers.ModelSerializer):
    booth_id = serializers.IntegerField(source='booth.id', read_only=True)  # booth_id 추가

    class Meta:
        model = Menu
        fields = ['id', 'menu', 'booth_id', 'img', 'price', 'is_vegan']

class BoothsDetailSerializer(serializers.ModelSerializer):
    #booth_id = serializers.IntegerField(source='booth.id', read_only=True)
    menus = MenuMainSerializer(many=True, read_only=True)

    class Meta:
        model = Booth
        fields = ['id', 'name', 'category', 'thumbnail', 'is_opened', 'place', 'menus']

class MenuDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Menu
        fields = ['id', 'menu', 'price', 'img', 'is_soldout', 'is_vegan']