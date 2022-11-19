from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers

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
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


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
