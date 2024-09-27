from django.db import models
from django.conf import settings

class Notice(models.Model):
    NOTICE_TYPE_CHOICES = [
        ('operational', '운영공지'),
        ('event', '행사공지')
    ]

    #이거 이렇게 내가 해놓는 게 맞나? 
    EVENT_TYPE_CHOICES = [
        ('ewhagreenFe', '다시 돌아온 네가 그린 그린은 이화그린'),
        ('artistShow', '아티스트 공연'),
        ('movie_fe', '야간 영화제'),
        ('nightMarket', '야시장'),
        ('tugOfWar', '영산 줄다리기'),
        ('riceFe', '이화인 한솥밥 배부')
    ]


    title = models.CharField(max_length=40)
    content = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPE_CHOICES)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, blank=True, null=True)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) #어차피 축준위지만 혹시 모르니 일단 만들어놓겠습니당

    def save(self, *args, **kwargs):
        if self.notice_type == 'operational':
            self.event_type = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title