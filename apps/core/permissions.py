from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.role == 'admin':
            return True
        
        # Check if object has user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to everyone,
    but write access only to the owner.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role == 'admin':
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsVendorOwner(permissions.BasePermission):
    """
    Permission to check if user is the vendor who owns the resource.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        
        if hasattr(obj, 'vendor'):
            return obj.vendor.user == request.user
        
        return False
