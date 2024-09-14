from django import forms
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Branch  # 확장된 사용자 모델 사용

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일')
    name = forms.CharField(max_length=100, required=True, label='이름')
    phone_number = forms.CharField(max_length=15, required=True, label='전화번호')
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True, label='지부 선택')
    verification_code = forms.CharField(max_length=100, required=True, label='인증 코드')  # 인증 코드 필드 추가

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'phone_number', 'branch', 'password1', 'password2')
        labels = {
            'username': '아이디',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code')
        
        # 인증 코드 확인 (예: 'SECRET1234'이 실제 인증 코드)
        if verification_code != 'SECRET1234':
            raise forms.ValidationError('유효하지 않은 인증 코드입니다.')
        
        return verification_code
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'business_number', 'store_id', 'store_name', 'region', 'store_type', 'min_order_amount', 
            'employee_number', 'notes', 'store_category', 'sticker_status', 'transfer_status', 
            'packaging', 'food_tech', 'multiple_pos', 'store_phone', 'owner_contact', 'email', 
            'competitor_status', 'bm', 'bm1', 'menu_board', 'origin_info', 'business_hours', 
            'images', 'account_id', 'password', 'open_date', 'special_notes',
            'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'image10', 'image11'
        ]
        widgets = {
            'open_date': forms.DateInput(attrs={'type': 'date'}),
            'image1': forms.ClearableFileInput(attrs={'multiple': False}),
            'image2': forms.ClearableFileInput(attrs={'multiple': False}),
            'image3': forms.ClearableFileInput(attrs={'multiple': False}),
            'image4': forms.ClearableFileInput(attrs={'multiple': False}),
            'image5': forms.ClearableFileInput(attrs={'multiple': False}),
            'image6': forms.ClearableFileInput(attrs={'multiple': False}),
            'image7': forms.ClearableFileInput(attrs={'multiple': False}),
            'image8': forms.ClearableFileInput(attrs={'multiple': False}),
            'image9': forms.ClearableFileInput(attrs={'multiple': False}),
            'image10': forms.ClearableFileInput(attrs={'multiple': False}),
            'image11': forms.ClearableFileInput(attrs={'multiple': False})
        }

class PostSearchForm(forms.Form):
    store_name = forms.CharField(required=False, label='매장명', widget=forms.TextInput(attrs={'placeholder': '매장명 검색'}))
    author = forms.CharField(required=False, label='작성자', widget=forms.TextInput(attrs={'placeholder': '작성자 검색'}))
    branch = forms.CharField(required=False, label='지부', widget=forms.TextInput(attrs={'placeholder': '지부 검색'}))