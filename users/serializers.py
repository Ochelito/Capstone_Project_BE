from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

# Get the active user model
User = get_user_model()

# Serializer for reading user details safely (without sensitive info)
class UserSerializer(serializers.ModelSerializer):
    """Serializer for reading user details (safe fields)."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'bio']  # Fields exposed for read-only purposes


# Serializer for registering a new user with password handling
class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user with password hashing."""
    
    # Password fields (write-only)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}  # Rendered as password input in browsable API
    )
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}  # Confirmation field
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'role', 'bio']
        extra_kwargs = {
            'role': {'required': False},  # Optional during registration
            'bio': {'required': False},   # Optional during registration
        }

    # Ensure password and password2 match
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    # Create the user instance with hashed password
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove confirmation field
        password = validated_data.pop('password')  # Extract password
        user = User.objects.create_user(**validated_data)  # Create user using manager
        user.set_password(password)  # Hash the password
        user.save()
        return user