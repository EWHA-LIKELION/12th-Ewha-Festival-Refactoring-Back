from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'notice_type',
                  'event_type', 'is_important', 'author', 'created_at']
        #read_only_fields = ['author', 'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'notice_type',
                  'event_type', 'created_at', 'is_important']
