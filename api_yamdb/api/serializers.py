import datetime as dt
from rest_framework import serializers


from reviews.models import (
    Review, Comment,
    Category, Genre, Title
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title


class CreateTitleSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    def validate_year(self, value):
        now = dt.date.today().year
        if value > now:
            raise serializers.ValidationError("Wrong year")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', required=False)

    def create(self, validated_data):
        author = self.context.get('request').user
        context = self.context.get('view').kwargs
        title = context['title_id']
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                "Only one review per title for author"
            )
        return Review.objects.create(**validated_data)

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
