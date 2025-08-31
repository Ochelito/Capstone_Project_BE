from rest_framework.permissions import BasePermission, SAFE_METHODS

# Permission class that allows safe methods (GET, HEAD, OPTIONS) to anyone,
# but restricts modification actions (POST, PUT, PATCH, DELETE) to learners only.
class IsLearnerForBookings(BasePermission):
    def has_permission(self, request, view):
        # Allow safe methods without restrictions
        if request.method in SAFE_METHODS:
            return True
        
        # Only authenticated users with role 'learner' can modify bookings
        return request.user.is_authenticated and request.user.role == 'learner'


# Permission class that allows safe methods to anyone,
# but restricts modifications to the owner of the booking
class IsBookingOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view, obj):
        # Allow safe methods without restrictions
        if request.method in SAFE_METHODS:
            return True
        
        # Only the learner who owns this booking can modify it
        return obj.learner == request.user