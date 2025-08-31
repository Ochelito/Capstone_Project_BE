from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsLearnerForReviews(BasePermission):
    """
    Permission to allow only learners to create or modify reviews.
    Read-only methods (GET, HEAD, OPTIONS) are allowed for everyone.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        # Only authenticated users with role 'learner' can create or modify
        return request.user.is_authenticated and request.user.role == 'learner'


class IsReviewOwnerOrReadOnly(BasePermission):
    """
    Permission to allow a user to update/delete only their own reviews.
    Read-only methods are allowed for everyone.
    """
    def has_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # Allow read-only methods for all users
            return True
        # Only the owner (learner who wrote the review) can modify it
        return obj.learner == request.user