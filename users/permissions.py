from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom permission: Only the owner of the object can edit; others have read-only access
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only requests for any user
        if request.method in SAFE_METHODS:
            return True
        
        # For write requests, allow only if the object is the logged-in user
        return obj == request.user  # Only the owner can edit