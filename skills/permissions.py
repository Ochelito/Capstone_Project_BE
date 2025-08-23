from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_Authenticated and request.user.role == 'mentor'
    
class ReadOnlyOrMentor(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_Authenticated and request.user.role == 'mentor'
    