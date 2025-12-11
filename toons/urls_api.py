from django.urls import path
from .api_views import webtoon_list, webtoon_detail, toggle_favorite, my_favorites
from .views import RandomWebtoonView, SurveySubmitView

urlpatterns = [
    path('webtoons/', webtoon_list, name='api-webtoon-list'),
    path('webtoons/<int:webtoon_id>/', webtoon_detail, name='api-webtoon-detail'),
    path('webtoons/<int:webtoon_id>/favorite/', toggle_favorite, name='api-toggle-favorite'),
    path('me/favorites/', my_favorites, name='api-my-favorites'),
    # [신규 추가] 설문 관련 API
    # 프론트엔드 호출 경로: /api/webtoons/random/ -> config/urls.py의 'api/' + 여기 'webtoons/random/'
    path('webtoons/random/', RandomWebtoonView.as_view(), name='webtoon-random'),
    path('survey/submit/', SurveySubmitView.as_view(), name='survey-submit'),
]
