from django.contrib import admin
from .models import Notice

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'notice_type', 'is_important', 'created_at', 'author']
    search_fields = ['title', 'content']
    list_filter = ['notice_type', 'is_important', 'created_at']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        
        # 새 공지를 추가할 때
        if obj is None:
            # 'event_type' 필드를 활성화
            form.base_fields['event_type'].disabled = False
        elif obj.notice_type == 'operational':
            # 수정 시 운영 공지인 경우 'event_type' 필드를 비활성화
            form.base_fields['event_type'].disabled = True
        else:
            # 수정 시 행사 공지인 경우 'event_type' 필드를 활성화
            form.base_fields['event_type'].disabled = False
            
        return form

admin.site.register(Notice, NoticeAdmin)
