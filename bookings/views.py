from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLearnerForBookings, IsBookingOwnerOrReadOnly

# ViewSet for the Booking model
# Handles CRUD operations: list, retrieve, create, update, delete
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()              # Base queryset for this viewset
    serializer_class = BookingSerializer          # Serializer to convert model instances to JSON

    # Define custom permissions based on action
    def get_permissions(self):
        if self.action in ['create']:
            # Only authenticated learners can create bookings
            return [IsAuthenticated(), IsLearnerForBookings()]
        # For other actions (retrieve, update, delete), enforce ownership or read-only
        return [IsAuthenticated(), IsBookingOwnerOrReadOnly()]

    # Automatically assign the logged-in user as the learner when creating a booking
    def perform_create(self, serializer):
        serializer.save(learner=self.request.user)