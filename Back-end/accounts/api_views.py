from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

# [내 정보 조회]
# JWT 토큰이 헤더에 있으면 request.user가 자동으로 식별됩니다.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """내 정보 조회"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# [회원가입]
# login() 함수를 제거하고 순수하게 DB 생성만 담당합니다.
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """회원가입"""
    # 앞서 만든 UserSerializer를 재사용합니다.
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # [중요] JWT에서는 여기서 login(request, user)를 하지 않습니다.
        return Response({
            'message': '회원가입 성공',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
