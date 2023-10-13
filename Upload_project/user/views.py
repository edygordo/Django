"""
Views for user API
"""
from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(generics.CreateAPIView):
    """Create a token upon successfull validation"""
    serializer_class = AuthTokenSerializer
    rendered_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage and authenticate user"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes =[authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return user"""
        return self.request.user 