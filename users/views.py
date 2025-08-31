from rest_framework import viewsets, generics, status
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

# ViewSet for standard user CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Assign permissions based on action:
        - list/retrieve: public access (anyone can view user profiles)
        - update/destroy: only the user themselves (owner) can modify/delete
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # public read-only access
        return [IsAuthenticated(), IsOwnerOrReadOnly()]  # owner-only for edits


# API endpoint for user registration
class RegisterView(generics.CreateAPIView):
    """API endpoint for registering a new user."""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # anyone can register

    def create(self, request, *args, **kwargs):
        """
        Handle registration request:
        1. Validate input data using serializer
        2. Save new user
        3. Return a response with the created user's info
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # raise error if validation fails
        user = serializer.save()  # create user

        # Return successful registration response
        return Response(
            {
                "message": "User registered successfully",
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "bio": user.bio,
            },
            status=status.HTTP_201_CREATED,
        )