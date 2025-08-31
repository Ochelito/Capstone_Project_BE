from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLearnerForBookings, IsBookingOwnerOrReadOnly


# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsLearnerForBookings()]
        return[IsAuthenticated(), IsBookingOwnerOrReadOnly()]
    
    def perform_create(self, serializer):
        serializer.save(learner=self.request.user) #logged-in learner auto-assigned
        