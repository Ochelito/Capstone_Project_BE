from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model

class UserSerializer(serializers.ModelSerializer):
    
    """Serializer for reading user details (safe fields)."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'bio']
        

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user with password hashing."""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'role', 'bio']
        extra_kwargs = {
            'role': {'required': False},
            'bio': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # remove confirmation field
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)  # calls custom manager
        user.set_password(password)
        user.save()
        return user