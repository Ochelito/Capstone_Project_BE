from rest_framework import viewsets, generics, status
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()] #anyone can view profiles
        return [IsAuthenticated(), IsOwnerOrReadOnly()] #only owner can update/delete


class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration."""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

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