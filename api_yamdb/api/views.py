from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filtersets import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly)

from reviews.models import Review, Category, Genre, Title
from .serializers import (
    ReviewSerializer, CommentSerializer, CategorySerializer,
    TitleSerializer, GenreSerializer, CreateTitleSerializer
)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).prefetch_related('genre').select_related('category')
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return CreateTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAdminOrReadOnly | IsAuthorOrReadOnly | IsModeratorOrReadOnly
    ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ReviewViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAdminOrReadOnly | IsAuthorOrReadOnly | IsModeratorOrReadOnly
    ]

    def get_review(self):
        return get_object_or_404(
            Review, title=self.get_title(), pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
