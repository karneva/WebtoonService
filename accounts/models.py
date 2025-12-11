from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 기본적 정보
    email = models.EmailField(unique=True)
    
    # 설문 완료 여부 (핵심 필드)
    is_survey_completed = models.BooleanField(default=False)
    
    # 설문 1: 인적 사항 저장용
    birth_year = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', '남성'), ('F', '여성')], null=True, blank=True)

    # 자기 참조??
    def __str__(self):
        return self.username


# --------------------------------------------------------------------------
# [추가됨] Taste.io 스타일 설문조사 데이터 저장용 모델
# 유저가 선택한 데이터는 User 모델에 다 넣지 말고, 별도 테이블로 분리(1:N)해야 관리가 쉽습니다.
# --------------------------------------------------------------------------

