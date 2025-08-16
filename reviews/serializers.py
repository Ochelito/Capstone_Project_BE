from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'content_type', 'object_id', 'learner', 'rating', 'comment', 'created_at']