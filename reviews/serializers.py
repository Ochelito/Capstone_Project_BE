from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    Converts Review model instances to JSON and validates input for API requests.
    """
    class Meta:
        model = Review
        # Fields to include in API responses and for creating/updating reviews
        fields = [
            'id',           # Review ID
            'content_type', # Generic relation type (e.g., lesson)
            'object_id',    # ID of the related object
            'learner',      # The learner who wrote the review
            'rating',       # Rating given (1-5)
            'comment',      # Optional text comment
            'created_at'    # Timestamp of review creation
        ]