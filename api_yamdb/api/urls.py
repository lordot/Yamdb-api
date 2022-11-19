from django.urls  import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet,
                       TitleViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet)
router.register(r'users/<slug:username>', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]

