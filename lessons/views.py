from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Lesson
from .serializers import LessonSerializer
from .permissions import IsMentorForLessons
from rest_framework.exceptions import PermissionDenied

class LessonViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Lesson model.
    Only mentors can create or modify lessons.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsMentorForLessons]

    def perform_create(self, serializer):
        """
        Associates the lesson with a skill that belongs to the logged-in mentor.
        Ensures a mentor cannot create lessons under another mentor's skill.
        """
        skill = serializer.validated_data.get('skill')
        
        # Check if the skill belongs to the logged-in mentor
        if skill.mentor != self.request.user:
            raise PermissionDenied("You can only create lessons for your own skills.")

        # Save the lesson with the mentor-restricted skill
        serializer.save()