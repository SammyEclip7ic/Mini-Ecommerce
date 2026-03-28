from rest_framework.permissions import BasePermission

class BaseRolePermission(BasePermission):
    """
    Base permission class to check for specific user roles.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        # 1. Check authentication
        if not (request.user and request.user.is_authenticated):
            return False
        
        # 2. Admin/Staff/Superuser check (Always allowed)
        if (request.user.role == 'admin' or 
            request.user.is_staff or 
            request.user.is_superuser):
            return True

        # 3. Check specific role
        return request.user.role in self.allowed_roles

class IsCustomer(BaseRolePermission):
    """
    Allows access only to customers and administrators.
    """
    allowed_roles = ['customer']

class IsVendor(BaseRolePermission):
    """
    Allows access only to vendors and administrators.
    """
    allowed_roles = ['vendor']

class IsAdmin(BaseRolePermission):
    """
    Allows access only to administrators (role='admin', staff, or superusers).
    """
    allowed_roles = ['admin']
