from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from booths.models import *


class ShowsMainSerializer(serializers.ModelSerializer):
    booth_place = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'category', 
                  'thumbnail', 'is_opened', 
                  'booth_place'] 
        
    def get_booth_place(self, obj):
        return obj.booth_place() 


class ShowsDetailSerializer(serializers.ModelSerializer):
    #booth_id = serializers.IntegerField(source='booth.id', read_only=True)
    booth_place = serializers.SerializerMethodField()
    booth_hours = serializers.SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'booth_place', 'category', 
                  'thumbnail', 'phonenum', 'is_opened', 
                  'booth_hours', 'description']
    
    def get_booth_place(self, obj):
        return obj.booth_place() 

    def get_booth_hours(self, obj):
        return [obj.booth_hours()] #여러개 받기