from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLearnerForReviews, IsReviewOwnerOrReadOnly

# ViewSet for managing Review objects via REST API
class ReviewViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Review model.
    - Learners can create reviews for completed bookings.
    - Learners can only edit or delete their own reviews.
    """
    queryset = Review.objects.all()          # Base queryset for the ViewSet
    serializer_class = ReviewSerializer     # Serializer to convert Review objects to/from JSON

    def get_permissions(self):
        """
        Assign permissions dynamically based on action:
        - For 'create', user must be authenticated and a learner.
        - For other actions (retrieve, update, delete), user must be the review owner.
        """
        if self.action in ['create']:
            return [IsAuthenticated(), IsLearnerForReviews()]
        return [IsAuthenticated(), IsReviewOwnerOrReadOnly()]
    
    def perform_create(self, serializer):
        """
        Automatically assign the logged-in learner as the reviewer when creating a review.
        """
        serializer.save(learner=self.request.user)