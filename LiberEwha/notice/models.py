from django.db import models
from django.conf import settings

class Notice(models.Model):
    NOTICE_TYPE_CHOICES = [
        ('operational', '운영공지'),
        ('event', '행사공지')
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPE_CHOICES)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) #어차피 축준위지만 혹시 모르니 일단 만들어놓겠습니당

    def __str__(self):
        return self.title