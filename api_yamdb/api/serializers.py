from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'is_moderator',
        )
        model = User
        lookup_field = 'username'


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email'
        )
        model = User

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код подтверждения для получения токена',
            message=f'confirmation_code:{confirmation_code}',
            from_email='Mainsuperuser27@gmail.com',
            recipient_list=[f'{user.email}'],
            fail_silently=False,
        )
        return user

