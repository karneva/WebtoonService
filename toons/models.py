from django.db import models
from django.conf import settings

# Create your models here.
class Webtoon(models.Model):
    provider = models.CharField(max_length=15)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    update_days = models.CharField(max_length=50)
    thumbnail = models.URLField()
    url = models.URLField()
    is_end = models.BooleanField(default=False)

    # ManyToMany로 즐겨찾기 관계 설정
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_webtoons',
        blank=True
    )
    
    def __str__(self):
        return self.title
    
    
# --------------------------------------------------------------------------
# [추가됨] Taste.io 스타일 설문조사 데이터 저장용 모델
# 유저가 선택한 데이터는 User 모델에 다 넣지 말고, 별도 테이블로 분리(1:N)해야 관리가 쉽습니다.
# --------------------------------------------------------------------------


# 설문조사용 웹툰 선택지 모델
class Survey_Webtoon(models.Model):
    title = models.CharField(max_length=100)
    # genre = models.CharField(max_length=50)
    # 썸네일 URL 필드 (더미 이미지용, 필요시 ImageField로 변경)
    thumbnail_url = models.URLField(null=True, blank=True) 

    def __str__(self):
        return self.title

# 조사 결과 저장용 모델
class SurveyLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_logs')
    # 설문 2: 선호 장르 (JSON 리스트)
    preferred_genres = models.JSONField(default=list)
    # 설문 3: 작품별 선호도 (JSON 객체)
    webtoon_ratings = models.JSONField(default=dict)
    # 설문 4: 주 사용 플랫폼
    main_platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Survey Log"
    
    
