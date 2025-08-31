from rest_framework import serializers
from .models import Skill

# Serializer for the Skill model
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill  # Specifies the model to serialize
        # Fields to include in the API representation
        fields = ['id', 'name', 'description', 'mentor']
        # 'id' - unique identifier for the skill
        # 'name' - name of the skill
        # 'description' - optional description of the skill
        # 'mentor' - the mentor associated with the skill