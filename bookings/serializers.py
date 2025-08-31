from rest_framework import serializers
from .models import Booking

# Serializer for the Booking model
# Responsible for converting Booking instances to JSON and validating input data
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking  # The model this serializer is based on
        # Fields to include in the serialized representation
        fields = [
            'id',            # Booking ID
            'learner',       # User who made the booking
            'content_type',  # Generic content type (e.g., Lesson)
            'object_id',     # ID of the booked object (e.g., lesson ID)
            'booked_at'      # Timestamp when the booking was created
        ]