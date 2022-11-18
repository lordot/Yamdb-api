from .views import UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet)
v1_router.register(r'users/<slug:username>', UserViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
