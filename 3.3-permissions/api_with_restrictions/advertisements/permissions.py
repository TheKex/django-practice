from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user == obj.creator


class IsAuthenticatedUpdate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS \
               or super(IsAuthenticatedUpdate, self).has_permission(request, view)
