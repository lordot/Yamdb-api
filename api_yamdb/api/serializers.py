from api_yamdb.settings import RESERVED_NAME, MESSAGE_FOR_RESERVED_NAME
from api_yamdb.settings import MESSAGE_FOR_USER_NOT_FOUND
import datetime as dt
from django.db.models import Avg
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator



from reviews.models import Review, User, Comment, Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']

    def validate_year(self, value):
        now = dt.date.today().year
        if value > now:
            raise serializers.ValidationError("Wrong year")
        return value

    class Meta:
        fields = 'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        model = Title


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
            raise serializers.ValidationError("Only one review per title fon author")
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
