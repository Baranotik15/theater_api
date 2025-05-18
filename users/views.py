from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    pagination_class = None
