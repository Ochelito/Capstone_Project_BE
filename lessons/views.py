from rest_framework import viewsets
from .models import Lesson
from .serializers import LessonSerializer

# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer 