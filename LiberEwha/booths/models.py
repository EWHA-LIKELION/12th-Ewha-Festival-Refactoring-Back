from django.db import models
from django.conf import settings
from accounts.models import User

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
        ('학관', '학관')]
    
    CATEGORY_CHOICES = [
        ('음식', '음식'),
        ('굿즈', '굿즈'),
        ('체험', '체험'),
        #공연
        ('학문관광장', '학문관광장'),
        ('스포츠트랙', '스포츠트랙')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='booths')
    name = models.CharField(max_length=20, unique=True)
    thumbnail = models.ImageField(upload_to='thumbnail', null=False) #upload_to: 업로드된 이미지 모아둘 경로
    place = models.CharField(max_length=20, choices=PLACE_CHOICES, null=False)
    #date = models.CharField(max_length=20, choices=DATE_CHOICES, null=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=False)
    phonenum = models.IntegerField(null= False, unique=True)
    is_opened = models.BooleanField(default=True) #default: 부스 운영중
    Field = models.TextField(null=True) #소개글 
    is_show = models.BooleanField(default=False) #default: 부스

    #스크랩 수
    scrap_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

#운영시간 : 10일 수요일 10시~15시/ 11일 목요일 10시~15시

class Menu(models.Model):

    VEGAN_CHOICES = [
        ('페스코', '페스코'),
        ('비건', '비건'),
        ('None', 'None')]
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='menus')
    menu= models.CharField(max_length=20, unique=False)
    price = models.IntegerField(null= False, unique=False)
    img = models.ImageField(upload_to='menu_img', null=False)
    is_vegan = models.CharField(max_length=10, choices=VEGAN_CHOICES, default='None', null=False)

    # 메뉴 스크랩 수
    scrap_count = models.IntegerField(default=0)

    def __str__(self):
        return self.menu
    #여기서 related_name은 Booth 모델에서 해당 부스에 연결된 모든 메뉴를 참조할 때 사용할 수 있는 이름을 지정한 것

# 부스 공지 모델
class Booth_notice(models.Model):
    NOTICE_TYPE = [
        ('판매공지', '판매공지'),
        ('운영공지', '운영공지')
    ]
    # 공지 타입
    notice_type = models.CharField(choices=NOTICE_TYPE)

    # 공지 내용
    content = models.CharField(null=False)

    # 공지 생성 시간(자동)
    created_at = models.DateTimeField(auto_now_add=True)

    # 부스(외래키)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='booth')

    def __str__(self):
        return self.content

#방명록 모델
class Guestbook(models.Model):
    # 작성자(외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'guestbook')
    # 부스(외래키)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='guestbook')
    # 내용
    content = models.CharField(max_length=200)
    # 작성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.content
    
# 답글 모델
class Reply(models.Model):
    # 작성자(외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply')
    # 방명록(외래키)
    guestbook = models.ForeignKey(Guestbook, on_delete=models.CASCADE, related_name='reply')
    # 내용
    content = models.CharField(max_length=200)
    # 작성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.content

# 부스 스크랩 모델
class Booth_scrap(models.Model):
    # 부스 (외래키)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name="booth")

    # 유저 (외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

# 메뉴 스크랩 모델
class Menu_scrap(models.Model):
    # 메뉴 (외래키)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")

    # 유저 (외래키)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
