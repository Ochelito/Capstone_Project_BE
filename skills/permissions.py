from rest_framework.permissions import BasePermission, SAFE_METHODS

# Permission to allow only mentors to access a view
class IsMentor(BasePermission):
    def has_permission(self, request, view):
        """
        Grant access only if the user is authenticated and has the 'mentor' role.
        """
        return request.user.is_Authenticated and request.user.role == 'mentor'
    

# Permission to allow read-only access to anyone, but restrict write actions to mentors
class ReadOnlyOrMentor(BasePermission):
    def has_permission(self, request, view):
        """
        Allow safe HTTP methods (GET, HEAD, OPTIONS) to anyone.
        Require the user to be authenticated and a mentor for unsafe methods (POST, PUT, DELETE, PATCH).
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_Authenticated and request.user.role == 'mentor'