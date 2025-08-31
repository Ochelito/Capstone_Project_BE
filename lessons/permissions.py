from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom permission to allow only mentors to create/update lessons
class IsMentorForLessons(BasePermission):
    """
    Permission class that allows safe methods (GET, HEAD, OPTIONS) for everyone,
    but restricts modification actions (POST, PUT, PATCH, DELETE) to authenticated users
    with the role of 'mentor'.
    """

    def has_permission(self, request, view):
        # Allow read-only requests for anyone
        if request.method in SAFE_METHODS:
            return True
        
        # Only authenticated users with role 'mentor' can modify lessons
        return request.user.is_authenticated and request.user.role == 'mentor'