from rest_framework import viewsets
from .models import Skill
from .serializers import SkillSerializer

# Create your views here.
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    