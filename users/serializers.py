from django.contrib.auth import get_user_model
from rest_framework import serializers, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )
        return value


class UserRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "detail": "User created successfully",
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "detail": "Invalid data",
                "errors": serializer.errors,
                "message":
                    "Ensure that all required fields are "
                    "filled out and meet validation requirements.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
