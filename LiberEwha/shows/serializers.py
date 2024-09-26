from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from booths.models import *


class ShowsMainSerializer(serializers.ModelSerializer):
    booth_place = serializers.SerializerMethodField()
    dayofweek = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'category', 
                  'thumbnail', 'is_opened', 
                  'booth_place', 'dayofweek'] 
        
    def get_booth_place(self, obj):
        return obj.booth_place()

    def get_dayofweek(self, obj):
        days = obj.days.all()
        return [day.dayofweek for day in days] 


class ShowsDetailSerializer(serializers.ModelSerializer):
    #booth_id = serializers.IntegerField(source='booth.id', read_only=True)
    booth_place = serializers.SerializerMethodField()
    days = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'booth_place', 'category', 
                  'thumbnail', 'admin_contact', 'is_opened', 
                  'description',
                  'days']
    
    def get_booth_place(self, obj):
        return obj.booth_place() 

    def get_days(self, obj):
        days = [f"{day.day}일 {day.dayofweek}요일 {day.opening_time} ~ {day.closing_time}"
                 for day in obj.days.all()]
        return days
    