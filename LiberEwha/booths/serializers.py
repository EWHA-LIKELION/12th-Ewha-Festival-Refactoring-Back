from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
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

<<<<<<< HEAD

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

=======
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
>>>>>>> 6d5a67236863c53451e1f71d2154ced4dd103fcb
