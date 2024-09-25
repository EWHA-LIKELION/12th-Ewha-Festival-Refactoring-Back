from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import *


class BoothsMainSerializer(serializers.ModelSerializer):
    booth_place = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'category', 
                  'thumbnail', 'is_opened', 
                  'booth_place'] 
        
    def get_booth_place(self, obj):
        return obj.booth_place() 

class MenuMainSerializer(serializers.ModelSerializer):
    booth_id = serializers.IntegerField(source='booth.id', read_only=True)  # booth_id 추가
    menu_price = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id','booth_id','menu', 
                'img', 'menu_price',
                'is_vegan', 'is_soldout']
        
    def get_menu_price(self, obj):
        return obj.menu_price() 


class BoothsDetailSerializer(serializers.ModelSerializer):
    #booth_id = serializers.IntegerField(source='booth.id', read_only=True)
    menus = MenuMainSerializer(many=True, read_only=True)
    booth_place = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'booth_place', 'category', 
                  'thumbnail', 'admin_contact', 'is_opened', 
                  'description', 'menus','days']
    
    def get_booth_place(self, obj):
        return obj.booth_place() 

    def get_days(self, obj):
        days = [f"{day.day}일 {day.dayofweek}요일 {day.opening_time} ~ {day.closing_time}"
                 for day in obj.days.all()]
        return days
    
class ReplySerializer(serializers.ModelSerializer):
    reply_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Reply
        fields = ['reply_id','content']

    def create(self,validated_data):
        request = self.context.get('request')
        guestbook_id = self.context.get('guestbook_id')
        validated_data['user'] = request.user
        validated_data['guestbook'] = get_object_or_404(Guestbook, id=guestbook_id)
        return super().create(validated_data)
    
class GuestBookSerializer(serializers.ModelSerializer):
    guestbook_id = serializers.IntegerField(source='id', read_only=True)
    reply = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Guestbook
        fields = ['guestbook_id','content', 'reply']

    def create(self, validated_data):
        request = self.context.get('request')
        booth_id = self.context.get('booth_id')
        validated_data['user'] = request.user
        validated_data['booth'] = get_object_or_404(Booth, id=booth_id)
        return super().create(validated_data)

class BoothScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth_scrap
        fields = '__all__'

class BoothScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth_scrap
        fields = '__all__'

class MenuScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_scrap
        fields = '__all__'
    
