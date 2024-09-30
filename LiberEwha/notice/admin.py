from django.contrib import admin
from .models import Notice

admin.site.register(Notice)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'notice_type',
                    'is_important', 'created_at', 'author']
    search_fields = ['title', 'content']
    list_filter = ['notice_type', 'is_important', 'created_at']

# Register your models here.
