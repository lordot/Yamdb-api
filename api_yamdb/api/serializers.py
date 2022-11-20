from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import exceptions, serializers

from reviews.models import Review, User, Comment, Category, Genre, Title

RESERVED_NAME = 'me'
MESSAGE_FOR_RESERVED_NAME = 'Имя пользователя "me" использовать нельзя!'
MESSAGE_FOR_USER_NOT_FOUND = 'Пользователя с таким именем нет!'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):
    """Изменение полей модели юзера."""
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
    """Регистрация нового юзера.
    Полечение кода подьверждения."""
    class Meta:
        fields = (
            'username',
            'email'
        )
        model = User

    def validate_username(self, value):
        username = value.lower()
        if username == "me":
            raise serializers.ValidationError("Имя me недоступно")
        return value

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


class TokenSerializer(serializers.Serializer):
    """Получение токена.
    Зарезервированное имя "me" использовать нельзя."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(MESSAGE_FOR_USER_NOT_FOUND)
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', required=False)

    def validate(self, data):
        author = self.context.get('request').user
        context = self.context.get('view').kwargs
        title = context['title_id']
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError("Only one review per title")
        return data

    class Meta:
        model = Review
        exclude = ('title', )
        read_only_fields = ('author', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', required=False)

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('author', 'pub_date')
