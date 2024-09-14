from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # 기본 게시글 리스트 뷰
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
]
