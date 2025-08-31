from rest_framework import viewsets
from .models import Skill
from .serializers import SkillSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnlyOrMentor

# Create your views here.
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [ReadOnlyOrMentor] #view for all, modify for mentors only

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user) #logged-in mentors is auto-assigned
    