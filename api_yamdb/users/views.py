from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken

from users.permissions import IsAdmin
from users.models import User
from users.serializers import AuthSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Модель юзеров"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdmin, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def user_info(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username
        )
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_admin or self.request.user.is_superuser:
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Регистрация нового юзера"""

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(
                username=username,
                email=email
            )
        except User.DoesNotExist:
            if User.objects.filter(username=username).exists():
                return Response(
                    'Пользователь с таким "username" уже зарегистрирован',
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    'Пользователь с таким "email" уже зарегистрирован',
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create_user(username=username, email=email)
        if serializer.is_valid(raise_exception=True):
            user.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Ваш код подтверждения для получения токена',
                message=f'confirmation_code:{confirmation_code}',
                from_email='Mainsuperuser27@gmail.com',
                recipient_list=[serializer.validated_data.get('email')],
                fail_silently=False,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenJWTView(APIView):
    """Выдача токена"""
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = User.objects.get(username=username)
        token = AccessToken.for_user(user)
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)
