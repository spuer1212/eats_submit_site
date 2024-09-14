from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import os
import uuid
from django.utils import timezone

# 파일 이름을 UUID로 변경하고 날짜별로 폴더에 저장하는 함수
def unique_file_path(instance, filename):
    # 파일 확장자 추출
    ext = filename.split('.')[-1]
    
    # UUID를 기반으로 한 고유 파일 이름 생성
    unique_filename = f"{uuid.uuid4()}.{ext}"

    # 파일이 저장될 폴더 구조 정의 (날짜 기반 폴더 구조)
    today = timezone.now().strftime('%Y/%m/%d')

    # 최종 파일 경로 반환 (예: uploads/2024/09/13/유니크이름.jpg)
    return os.path.join('uploads', today, unique_filename)

class Branch(models.Model):
    name = models.CharField(max_length=100)  # 지부 이름

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)  # 사용자 지부 정보
    is_manager = models.BooleanField(default=False)  # 중간관리자 권한 추가

    def __str__(self):
        return self.username
    
class Post(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True,)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 작성자와 연결
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)  # 지부 정보 추가
    
    # 새로운 필드 추가
    is_published = models.BooleanField(default=False)

     # 텍스트 필드
    business_number = models.CharField(max_length=100, verbose_name="사업자등록번호")
    store_id = models.CharField(max_length=100, verbose_name="스토어아이디")
    store_name = models.CharField(max_length=100, verbose_name="스토어명")
    region = models.CharField(max_length=100, verbose_name="지역")
    store_type = models.CharField(max_length=100, verbose_name="타입")
    min_order_amount = models.CharField(max_length=100, verbose_name="최소주문금액")
    employee_number = models.CharField(max_length=100, verbose_name="사번(대행사코드)")
    notes = models.TextField(blank=True, verbose_name="비고")
    
    # 추가 항목
    store_category = models.CharField(max_length=100, verbose_name="스토어 유형")
    sticker_status = models.CharField(max_length=100, verbose_name="스티커 부착 유무")
    transfer_status = models.CharField(max_length=100, verbose_name="양도양수")
    packaging = models.CharField(max_length=100, verbose_name="포장")
    food_tech = models.CharField(max_length=100, verbose_name="푸드테크")
    multiple_pos = models.CharField(max_length=100, verbose_name="다중포스")
    store_phone = models.CharField(max_length=100, verbose_name="매장전화번호")
    owner_contact = models.CharField(max_length=100, verbose_name="점주 연락처")
    email = models.EmailField(verbose_name="이메일")
    competitor_status = models.CharField(max_length=100, verbose_name="경쟁사 운영여부")
    bm = models.CharField(max_length=100, verbose_name="BM")
    bm1 = models.CharField(max_length=100, verbose_name="BM1")
    menu_board = models.CharField(max_length=100, verbose_name="메뉴판")
    origin_info = models.CharField(max_length=100, verbose_name="원산지")
    business_hours = models.CharField(max_length=100, verbose_name="영업시간")
    images = models.CharField(max_length=100, verbose_name="이미지")
    account_id = models.CharField(max_length=100, verbose_name="계정 아이디")
    password = models.CharField(max_length=100, verbose_name="비번")
    open_date = models.DateField(verbose_name="오픈희망일")
    special_notes = models.TextField(blank=True, verbose_name="특이사항")

    # 다중 사진 업로드를 위한 11개의 이미지 필드
    image1 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='사업자등록증 사진')
    image2 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='영업신고증 사진')
    image3 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='통장사본 사진')
    image4 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='식품안전나라 영업신고 상세페이지')
    image5 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='배민 앱 캡쳐본(메인)')
    image6 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='배민 앱 캡쳐본(상세정보)')
    image7 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='포스기 설치 사진')
    image8 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='쿠팡이츠 스티커')
    image9 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='스토어 앱 설치 사진')
    image10 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='설문조사 안내 캡쳐본')
    image11 = models.ImageField(upload_to=unique_file_path, blank=True, null=True, verbose_name='이미지 사용 정책 확인')


    def __str__(self):
        return self.store_name

    # def __str__(self):
    #     return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 작성자와 연결
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
    
