from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class BoothsMainSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booths
        fields = ['id', 'name', 'category', 'thumnail', 'is_open', 'place'] 

class BoothsDetailSerializer(serializers.ModelSerializer):
    booth_id = serializers.IntegerField(source='booths.id', read_only=True)
    phonenum = serializers.IntegerField(source='booths.phonenum', read_only=True)
    
    
    class Meta:
        model = Menus
        fields = ['menu', 'price', 'img', 'is_vegan',  ]

class MenuMainSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Menus
        fields = ['id', 'name', 'booth_id', 'tuhmnail', 'menu', 'price', 'img', 'is_soldout', 'is_vegan']

class MenuDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Menus
        fields = ['id', 'menu', 'price', 'img', 'is_soldout', 'is_vegan']