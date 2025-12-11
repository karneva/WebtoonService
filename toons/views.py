from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import requests
from .models import Webtoon

PLATFORM_API = {
    'NAVER': 'https://korea-webtoon-api.onrender.com/webtoons?provider=NAVER&page=1&perPage=100&sort=ASC',
    'KAKAO': 'https://korea-webtoon-api.onrender.com/webtoons?provider=KAKAO&page=1&perPage=100&sort=ASC',
    'KAKAO_PAGE': 'https://korea-webtoon-api.onrender.com/webtoons?provider=KAKAO_PAGE&page=1&perPage=100&sort=ASC'
}

def fetch_webtoons_all_pages(provider):
    all_webtoons = []
    for page in range(1, 51):
        url = f'https://korea-webtoon-api.onrender.com/webtoons?provider={provider}&page={page}&perPage=100&sort=ASC'
        resp = requests.get(url)
        page_items = resp.json().get('webtoons', [])
        # 빈 페이지라면 더 이상 요청하지 않음
        if not page_items:
            break
        all_webtoons.extend(page_items)
    return all_webtoons

def filter_webtoons_with_updateDays(webtoons):
    # 업데이트 요일이 하나 이상 존재하는 웹툰만 남김
    return [toon for toon in webtoons if toon.get('updateDays')]

def sync_webtoons(provider):
    all_webtoons = fetch_webtoons_all_pages(provider)
    valid_webtoons = filter_webtoons_with_updateDays(all_webtoons)
    # 이미 저장된 웹툰은 중복 저장 방지
    for toon in valid_webtoons:
        Webtoon.objects.update_or_create(
            url=toon['url'],
            defaults={
                'provider': provider,
                'title': toon['title'].strip(),
                'authors': ','.join(toon.get('authors', [])),
                'update_days': ','.join(toon['updateDays']),
                'thumbnail': toon['thumbnail'][0] if toon.get('thumbnail') else '',
                'is_end': toon['isEnd'],
            }
        )

def webtoon_list(request):
    platform = request.GET.get('platform', 'NAVER')
    query = request.GET.get('q', '')
    
    # [1] DB에 플랫폼별 웹툰이 없으면 API로 불러와서 동기화/저장
    if not Webtoon.objects.filter(provider=platform).exists():
        sync_webtoons(platform)

    # [2] DB에서 검색·필터링
    qs = Webtoon.objects.filter(provider=platform).exclude(update_days='')
    
    if platform in ['KAKAO', 'KAKAO_PAGE']:
        qs = qs.filter(is_end=False)

    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query)
        )

    webtoons = qs.all()

    context = {
        'webtoons': webtoons,
        'platform': platform,
        'query': query,
    }
    return render(request, 'toons/index.html', context)
    
@login_required
def toggle_favorite(request, webtoon_id):
    """AJAX 즐겨찾기 토글"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST 요청만 가능합니다.'}, status=405)
    
    webtoon = get_object_or_404(Webtoon, id=webtoon_id)
    
    # 즐겨찾기 토글
    if request.user in webtoon.favorited_by.all():
        webtoon.favorited_by.remove(request.user)
        is_favorited = False
        message = '즐겨찾기에서 제거되었습니다.'
    else:
        webtoon.favorited_by.add(request.user)
        is_favorited = True
        message = '즐겨찾기에 추가되었습니다.'
    
    context = {
        'success': True,
        'is_favorited': is_favorited,
        'message': message,
        'favorites_count': webtoon.favorited_by.count()
    }
    
    return JsonResponse(context)

@login_required
def my_page(request):
    """마이페이지 - 탭별 콘텐츠"""
    tab = request.GET.get('tab', 'interest')  # 기본 탭: 관심웹툰
    platform = request.GET.get('platform', 'ALL')
    query = request.GET.get('q', '')
    
    context = {
        'current_tab': tab,
        'platform': platform,
        'query': query,
    }
    
    if tab == 'interest':
        # 관심웹툰(즐겨찾기) 목록
        favorite_webtoons = request.user.favorite_webtoons.all()
        
        # 플랫폼 필터
        if platform != 'ALL':
            favorite_webtoons = favorite_webtoons.filter(provider=platform)
        
        # 검색
        if query:
            favorite_webtoons = favorite_webtoons.filter(
                Q(title__icontains=query) | Q(authors__icontains=query)
            )
        
        context['webtoons'] = favorite_webtoons
    
    # 추후 다른 탭 추가 가능
    # elif tab == 'recent':
    #     최근 본 웹툰
    # elif tab == 'comments':
    #     내가 단 댓글
    
    return render(request, 'toons/my_page.html', context)

# ---------------------------------------------------------------------------------
## 설문조사용 views 정리(start)
# ---------------------------------------------------------------------------------

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Survey_Webtoon, SurveyLog
from .serializers import SurveyWebtoonSerializer
import random

class RandomWebtoonView(APIView):
    # 설문은 로그인 직후 진행되므로 인증 필요
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        count = int(request.GET.get('count', 10))
        # 랜덤 정렬하여 요청된 개수만큼 반환
        survey_webtoons = Survey_Webtoon.objects.order_by('?')[:count]
        serializer = SurveyWebtoonSerializer(survey_webtoons, many=True)
        return Response(serializer.data)

class SurveySubmitView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data
        
        SurveyLog.objects.create(
            user=user,
            preferred_genres=data.get('genres', []),
            webtoon_ratings=data.get('ratings', {}),
            main_platform=data.get('platform', '')
        )
        
        user.birth_year = data.get('birth_year')
        user.gender = data.get('gender')
        user.is_survey_completed = True
        user.save()
        
        return Response({"message": "완료", "is_survey_completed": True})
    
# ---------------------------------------------------------------------------------
## 설문조사용 views 정리(end)
# ---------------------------------------------------------------------------------