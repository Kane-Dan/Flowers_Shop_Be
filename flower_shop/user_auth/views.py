from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Token
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer
)
from django.core.cache import cache

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({"message": "Регистрация пройдена успешно"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Авторизация пользователя",
        description="Логин через телефон и пароль, возвращает JWT токены.",
        request=UserLoginSerializer,
        responses={
            200: OpenApiParameter(
                name="tokens",
                type="object",
                description="Access и Refresh токены",
                examples=[
                    {
                        "refresh": "<refresh_token>",
                        "access": "<access_token>",
                    }
                ],
            )
        },
    )
    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Получаем пользователя из сериализатора
            
            # Создаем новый refresh и access токены для пользователя
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Сохраняем access токен в таблице Token
            Token.objects.update_or_create(
                users=user,
                defaults={'a_token': access_token}
            )

            # Сохраняем refresh-токен в Redis (или в кэше Django)
            cache.set(f'refresh_token_{user.id}', str(refresh), timeout=60*60*24)  # 1 день

            return Response({
                "access": access_token,
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Обновление access-токена",
        description="Обновляет access-токен с использованием refresh-токена.",
        request={
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "example": "<refresh_token>"},
            },
        },
        responses={
            200: {"type": "object", "properties": {"access": {"type": "string"}}},
            400: {"type": "string", "example": "Invalid token"},
        },
    )
    @action(methods=['post'], detail=False, url_path='refresh')
    def refresh(self, request):
        refresh_token = request.data.get('refresh', None)
        if not refresh_token:
            return Response({"detail": "Токен не прошел проверку"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли refresh-токен в Redis
        user_id = self.get_user_id_from_refresh_token(refresh_token)  # реализуйте этот метод
        if user_id is None:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Создаем новый access-токен
            user = User.objects.get(id=user_id)
            new_access_token = str(RefreshToken.for_user(user).access_token)

            return Response({"access": new_access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_id_from_refresh_token(self, refresh_token):
        # Здесь вы можете добавить логику для извлечения user_id из refresh-токена или проверить его в Redis.
        for user_id in cache.keys('refresh_token_*'):
            if cache.get(user_id) == refresh_token:
                return user_id.split('_')[-1]  # Извлекаем id пользователя из ключа
        return None