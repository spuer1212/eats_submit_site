"""
URL configuration for bulletin_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from board import views
from django.contrib.auth import views as auth_views
from board.views import CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')),  # board 앱의 URL 포함
    path('', views.post_list, name='post_list'),  # 기본 페이지를 게시판 리스트로 설정
    path('post/new/', views.post_create, name='post_create'),
    path('accounts/signup/', views.signup, name='signup'),   # 회원가입 URL 추가
    path('accounts/', include('django.contrib.auth.urls')),  # Django의 기본 인증 URL 포함
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # 게시글 상세
    path('post/new/', views.post_create, name='post_create'),  # 새 게시글 작성
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', include('board.urls')),  # 게시판 관련 URL
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),  # 커스텀 로그아웃 뷰 연결
    path('accounts/', include('django.contrib.auth.urls')),  # Django 기본 인증 URL 포함
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)