from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets, mixins, status
from rest_framework.pagination import LimitOffsetPagination
from .mixins import ListCreateDestroyViewSet


from reviews.models import Review, User, Category, Genre, Title, Comment
from .serializers import (
    ReviewSerializer, UserSerializer, CommentSerializer, CategorySerializer,
    TitleSerializer, GenreSerializer, AuthSerializer, UserSerializer
)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title

    def get_queryset(self):
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ReviewViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        title = self.get_title().reviews.select_related('author')
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"), title=title)
        return review

    def get_queryset(self):
        return self.get_review().comments.select_related('author')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [permissions.AllowAny, ]
    

