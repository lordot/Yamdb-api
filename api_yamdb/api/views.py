

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Review, User
from serializers import ReviewSerializer, UserSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
