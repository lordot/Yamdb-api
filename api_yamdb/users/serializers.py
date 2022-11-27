from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator


from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Изменение полей модели юзера."""
    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]
        model = User
        lookup_field = 'username'


class SimpleUserSerializer(serializers.ModelSerializer):
    """Поля для редактирования простым пользователем."""
    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',

        ]
        read_only_fields = ('username', 'email')
        model = User


class AuthSerializer(serializers.ModelSerializer):
    """Регистрация нового юзера.
    Полечение кода подьверждения."""
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = [
            'username',
            'email'
        ]
        model = User

    def validate_username(self, value):
        username = value.lower()
        if username == "me":
            raise serializers.ValidationError("Имя me недоступно")
        return value


class TokenSerializer(serializers.Serializer):
    """Получение токена.
    Зарезервированное имя "me" использовать нельзя."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if value == settings.RESERVED_NAME:
            raise serializers.ValidationError(
                settings.MESSAGE_FOR_RESERVED_NAME
            )
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(settings.MESSAGE_FOR_USER_NOT_FOUND)
        return value

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
                user, data['confirmation_code']
        ):
            raise exceptions.ParseError
        return data
