from django.db import models
from django.conf import settings
from accounts.models import User
from .models import *

# Create your models here.
class Booth(models.Model):
    PLACE_CHOICES = [ #부스 지도 참고... 
        ('교육관', '교육관'),
        ('학문관', '학문관'),
        ('생활관', '생활관'),
        ('대강당', '대강당'),
        ('휴웃길', '휴웃길'),
        ('포스코관', '포스코관'),
        ('신세계관', '신세계관'),
        ('잔디광장', '잔디광장'),
        ('학관', '학관'),
        #공연
        ('학문관광장', '학문관광장'),
        ('스포츠트랙', '스포츠트랙')]
    
    CATEGORY_CHOICES = [
        ('음식', '음식'),
        ('굿즈', '굿즈'),
        ('체험', '체험'),
        #공연
        ('밴드', '밴드'),
        ('댄스', '댄스')]

    DAYOFWEEK_CHOICES =[
        ('수', '수'),
        ('목', '목'),
        ('금', '금')
    ]
    DAY_CHOICES=[
        ('10','10'),
        ('11','11'),
        ('12','12')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='booths')
    name = models.CharField(max_length=20, unique=True)
    thumbnail = models.ImageField(upload_to='thumbnail', null=False) #upload_to: 업로드된 이미지 모아둘 경로
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, null=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True)
    admin_contact = models.CharField(max_length=50, unique=True, null=False) #오픈채팅
    is_opened = models.BooleanField(default=True) #default: 부스 운영중
    description = models.TextField(null=True) #소개글 
    is_show = models.BooleanField(default=False) #default: 부스
    scrap_count = models.IntegerField(default=0) #스크랩 수
    notice_count = models.IntegerField(default=0)
    
    def booth_place(self):
        return f"{self.place} {self.id}"
    
    def increaseScrapCount(self):
        self.scrap_count += 1
        self.save()

    def decreaseScrapCount(self):
        if self.scrap_count > 0:
            self.scrap_count -= 1
            self.save()

    def increaseNoticeCount(self):
        self.notice_count += 1
        self.save()

    def decreaseNoticeCount(self):
        if self.scrap_count > 0:
            self.notice_count -= 1
            self.save()

    notice_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def increaseScrapCount(self):
        self.scrap_count += 1
        self.save()

    def decreaseScrapCount(self):
        if self.scrap_count > 0:
            self.scrap_count -= 1
            self.save()

    def increaseNoticeCount(self):
        self.notice_count += 1
        self.save()

    def decreaseNoticeCount(self):
        if self.scrap_count > 0:
            self.notice_count -= 1
            self.save()

class Menu(models.Model):

    VEGAN_CHOICES = [
        ('페스코', '페스코'),
        ('비건', '비건'),
        ('논비건','논비건'),
        ('해당없음', '해당없음')]
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='menus')
    menu= models.CharField(max_length=14, unique=False)
    price = models.IntegerField(blank=False,null= False, unique=False)
    img = models.ImageField(upload_to='menu_img', null=False)
    is_vegan = models.CharField(max_length=10, choices=VEGAN_CHOICES, default='None', null=False)
    is_soldout = models.BooleanField(default=False)
    scrap_count = models.IntegerField(default=0) #메뉴 스크랩 수
    
    def menu_price(self):
        return f"{self.price}원"
    
    def __str__(self):
        return self.menu
    
    def increaseScrapCount(self):
        self.scrap_count += 1
        self.save()

    def decreaseScrapCount(self):
        if self.scrap_count > 0:
            self.scrap_count -= 1
            self.save()
    #여기서 related_name은 Booth 모델에서 해당 부스에 연결된 모든 메뉴를 참조할 때 사용할 수 있는 이름을 지정한 것

    def increaseScrapCount(self):
        self.scrap_count += 1
        self.save()

    def decreaseScrapCount(self):
        if self.scrap_count > 0:
            self.scrap_count -= 1
            self.save()

# 부스 공지 모델
class Booth_notice(models.Model):
    NOTICE_TYPE = [
        ('판매공지', '판매공지'),
        ('운영공지', '운영공지')
    ]
    # 공지 타입
    notice_type = models.CharField(max_length=10, choices=NOTICE_TYPE)

    # 공지 내용
    content = models.CharField(max_length=500, null=False)

    # 공지 생성 시간(자동)
    created_at = models.DateTimeField(auto_now_add=True)

    # 부스(외래키)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='notice')

    def __str__(self):
        return self.content

#방명록 모델
class Guestbook(models.Model):
    # 작성자(외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'guestbook')
    # 부스(외래키)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='guestbook')
    # 내용
    content = models.CharField(max_length=200, null=False)
    # 작성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.content
    
#답글 모델
class Reply(models.Model):
    # 작성자(외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply')
    # 방명록(외래키)
    guestbook = models.ForeignKey(Guestbook, on_delete=models.CASCADE, related_name='reply')
    # 내용
    content = models.CharField(max_length=200, null=False)
    # 작성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.content

# 부스 스크랩 모델
class Booth_scrap(models.Model):
    # 부스 (외래키)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name="booth_scrap")

    # 유저 (외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booth_scrap")

    

# 메뉴 스크랩 모델
class Menu_scrap(models.Model):
    # 메뉴 (외래키)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_scrap")

    # 유저 (외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="menu_scrap")

class Day(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='days')
    day = models.CharField(max_length=5, choices=[
        ('10', '10'),
        ('11', '11'),
        ('12', '12')
    ])
    dayofweek = models.CharField(max_length=5, choices=[
        ('수', '수'),
        ('목', '목'),
        ('금', '금')
    ])
    opening_time= models.CharField(max_length=5, null=False)
    closing_time= models.CharField(max_length=5, null=False)
    
    def __str__(self):
        return self.day
