from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLearnerForReviews, IsReviewOwnerOrReadOnly


# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsLearnerForReviews()]
        return[IsAuthenticated(), IsReviewOwnerOrReadOnly()]
    
    def perform_create(self, serializer):
        serializer.save(learner=self.request.user)