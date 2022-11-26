from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (UserViewSet,
                    SignupViewSet, TokenJWTView)

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'users/<slug:username>', UserViewSet)
router.register(r'auth/signup', SignupViewSet, basename='auth')


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
    path(
        'auth/token/', TokenJWTView.as_view(),
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(jwt_urls)),
]
