from rest_framework import serializers
from .models import Lesson

# Serializer for the Lesson model
class LessonSerializer(serializers.ModelSerializer):
    """
    Serializes Lesson instances for API responses and handles
    validation for creating/updating lessons.
    """

    class Meta:
        model = Lesson
        # Fields to expose via API
        fields = [
            'id',        # Unique identifier for the lesson
            'skill',     # Related skill (foreign key)
            'title',     # Lesson title
            'description',  # Lesson description/content
            'order',     # Display order in the skill's lesson list
            'price',     # Price for the lesson
        ]