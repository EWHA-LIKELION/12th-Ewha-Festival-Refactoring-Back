from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import *
from main.serializers import MainPageMenuSerializer

class BoothsMainSerializer(serializers.ModelSerializer):
    booth_place = serializers.SerializerMethodField()
    dayofweek = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField(allow_null=True)
    scrap_count = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'category', 'thumbnail',
                  'is_opened', 'booth_place', 'scrap_count', 'dayofweek']

    def get_booth_place(self, obj):
        return obj.booth_place()

    def get_thumbnail(self, obj):
        if obj.thumbnail and obj.thumbnail.name:
            return obj.thumbnail.url

    def get_dayofweek(self, obj):
        days = obj.days.all()
        return [day.dayofweek for day in days]

    def get_scrap_count(self, obj):
        return obj.scrap_count

class MenuMainSerializer(serializers.ModelSerializer):
    booth_id = serializers.IntegerField(source='booth.id', read_only=True)  # booth_id 추가
    menu_price = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id','booth_id', 'menu',
                'img', 'menu_price',
                'is_vegan', 'is_soldout']

    def get_menu_price(self, obj):
        return obj.menu_price()

class BoothsDetailSerializer(serializers.ModelSerializer):
    #booth_id = serializers.IntegerField(source='booth.id', read_only=True)
    menus = serializers.SerializerMethodField()
    booth_place = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Booth
        fields = ['id', 'name', 'booth_place', 'category', 'scrap_count',
                  'thumbnail', 'admin_contact', 'is_opened',
                  'description', 'menus', 'days' , 'notice_count']

    def get_booth_place(self, obj):
        return obj.booth_place()

    def get_thumbnail(self, obj):
        if obj.thumbnail and obj.thumbnail.name:
            return obj.thumbnail.url

    def get_days(self, obj):
        days = [f"{day.day}일 {day.dayofweek}요일 {day.opening_time} ~ {day.closing_time}"
                 for day in obj.days.all()]
        return days

    def get_menus(self, obj):
        menu_results = Menu.objects.filter(booth=obj)
        return MainPageMenuSerializer(menu_results, many=True).data

class ReplySerializer(serializers.ModelSerializer):
    reply_id = serializers.IntegerField(source='id', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    guestbook_id = serializers.IntegerField(source='guestbook.id', read_only=True)
    class Meta:
        model = Reply
        fields = ['guestbook_id','reply_id','user_nickname','content','created_at']

    def create(self,validated_data):
        request = self.context.get('request')
        guestbook_id = self.context.get('guestbook_id')
        validated_data['guestbook'] = get_object_or_404(Guestbook, id=guestbook_id)
        validated_data['user'] = request.user
        return super().create(validated_data)

class GuestBookSerializer(serializers.ModelSerializer):
    guestbook_id = serializers.IntegerField(source='id', read_only=True)
    reply = ReplySerializer(many=True, read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    booth_id = serializers.IntegerField(source='booth.id', read_only=True)
    class Meta:
        model = Guestbook
        fields = ['booth_id','guestbook_id', 'user_nickname','content','created_at','reply']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class BoothScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth_scrap
        fields = '__all__'

class MenuScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_scrap
        fields = '__all__'


class BoothsTFSerializer(serializers.ModelSerializer):
    booth_place = serializers.SerializerMethodField()
    dayofweek = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Booth
        fields = ['id', 'name', 'booth_category', 'thumbnail', 'is_opened',
                  'is_show', 'booth_place', 'dayofweek', 'days']

    def get_booth_place(self, obj):
        return obj.booth_place()

    def get_dayofweek(self, obj):
        days = obj.days.all()
        return [day.dayofweek for day in days]

    def get_thumbnail(self, obj):
        if obj.thumbnail and obj.thumbnail.name:
            return obj.thumbnail.url

    def get_days(self, obj):
        days = [f"{day.opening_time} ~ {day.closing_time}" for day in obj.days.all()]
        return days

class BoothsTFDetailSerializer(serializers.ModelSerializer):
    booth_place = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Booth
        fields = ['id', 'name', 'booth_place', 'category',
                  'thumbnail', 'admin_contact', 'is_opened',
                  'description', 'days']

    def get_booth_place(self, obj):
        return obj.booth_place()

    def get_thumbnail(self, obj):
        if obj.thumbnail and obj.thumbnail.name:
            return obj.thumbnail.url

    def get_days(self, obj):
        days = [f"{day.opening_time} ~ {day.closing_time}" for day in obj.days.all()]
        return days