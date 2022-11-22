from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated:
            return True
        return bool(request.user.is_admin or request.user.is_moderator)


class SpecialForStuffAndAuthor(permissions.BasePermission):
    ''' разрешение на редактирование и удаление отзыва'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return bool(request.user.is_authenticated)
        if request.method == 'PATCH' or request.method == 'DELETE':
            return bool(request.user.is_moderator
                        or request.user.is_admin
                        or obj.author == request.user)
        else:
            return False
