from rest_framework import viewsets
from .models import Lesson
from .serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsMentorForLessons

# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer 
    permission_classes = [IsMentorForLessons]

    def perform_create(self, serializer):
        #mentor creates lesson under their own skill
        serializer.save(skill__mentor=self.request.user)
