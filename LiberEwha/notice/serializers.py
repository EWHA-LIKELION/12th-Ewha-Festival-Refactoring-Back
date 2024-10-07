from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'notice_type',
                  'event_type', 'is_important', 'created_at', 'author']


class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'notice_type',
                  'event_type', 'created_at', 'is_important']
