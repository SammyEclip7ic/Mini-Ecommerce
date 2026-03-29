from rest_framework.permissions import BasePermission


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vendor'


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.vendor == request.user
