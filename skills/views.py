from rest_framework import viewsets
from .models import Skill
from .serializers import SkillSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnlyOrMentor

# ViewSet for managing skills
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()  # Retrieve all Skill instances
    serializer_class = SkillSerializer  # Use the SkillSerializer for input/output
    permission_classes = [ReadOnlyOrMentor]  
    # Permission:
    # - Read-only access for everyone
    # - Create/Update/Delete only allowed for authenticated mentors

    def perform_create(self, serializer):
        # Automatically assign the logged-in mentor as the creator of the skill
        serializer.save(mentor=self.request.user)