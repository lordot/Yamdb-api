from django.urls  import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (CategoryViewSet, GenreViewSet,
                       TitleViewSet, UserViewSet, ReviewViewSet, CommentViewSet,
                       SignupViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet)
router.register(r'users/<slug:username>', UserViewSet)
router.register(r'auth/signup', SignupViewSet, basename='auth')
router.register(r'auth/token', SignupViewSet, basename='auth')
router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)

jwt_urls = [
    path(
        'jwt/create/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'jwt/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(jwt_urls)),
]

