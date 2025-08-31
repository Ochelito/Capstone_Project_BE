from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsLearnerForReviews(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_Authenticated and request.user.role == 'learner'

class IsReviewOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.learner == request.user
    
    
    