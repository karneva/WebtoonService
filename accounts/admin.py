from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # 커스텀 유저 모델 import

# 커스텀 유저 모델 등록
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 관리자 목록에 보여줄 필드들 (필요에 따라 수정 가능)
    list_display = ('username', 'email', 'is_survey_completed', 'is_staff')
    
    # 상세 페이지에서 수정할 필드 섹션 추가
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('is_survey_completed', 'birth_year', 'gender')}),
    )