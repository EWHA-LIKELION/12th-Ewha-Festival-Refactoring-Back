from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from booths.models import *

class BoothNoticeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booth_notice
        fields = ['notice_type', 'content', 'booth']