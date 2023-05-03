from rest_framework import permissions


class AuthOrOwner(permissions.BasePermission):
    message = 'Нельзя изменить чужой контент!'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.author == request.user
        return False


class ReadOrOwner(permissions.BasePermission):
    message = 'Изменять можно только свой контент!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
