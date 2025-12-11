from rest_framework import serializers
from .models import Webtoon, Survey_Webtoon

class WebtoonSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Webtoon
        fields = [
            'id',
            'provider',
            'title',
            'authors',
            'update_days',
            'thumbnail',
            'url',
            'is_end',
            'is_favorited',
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(id=request.user.id).exists()
        return False

## 설문조사용 더미 웹툰 시리얼라이저
class SurveyWebtoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey_Webtoon
        fields = ['id', 'title', 'thumbnail_url']