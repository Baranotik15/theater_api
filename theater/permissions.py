from rest_framework.permissions import BasePermission, IsAdminUser, AllowAny

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Grants read access (GET) to all users.
    - Grants access for creation, update, and partial update only to administrators.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return IsAdminUser().has_permission(request, view)
