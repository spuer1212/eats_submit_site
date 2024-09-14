from django.contrib import admin
from .models import Post, Comment, Branch
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

admin.site.register(Post)
admin.site.register(Comment)

class CustomUserAdmin(UserAdmin):
    # Django의 기본 UserAdmin을 확장하여 사용자 필드 정의
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'name', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'phone_number', 'password1', 'password2'),
        }),
    )

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(CustomUser, CustomUserAdmin)