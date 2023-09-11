from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class CurrentUserOrAdminOrReadOnly(permissions.IsAuthenticated):
    """
    Права только для текущего пользователя, администратора
    или только на GET запросы
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj.author) == type(user) and obj.author == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff
