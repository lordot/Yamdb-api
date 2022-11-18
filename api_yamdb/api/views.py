from rest_framework import viewsets

from serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # добавить определение ID произведения
        pass

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # добавить передачу ID title и review
        pass

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
