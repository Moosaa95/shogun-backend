from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from .serializers import UserCreateSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    """

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]  # Anyone can register

    @extend_schema(
        request=UserCreateSerializer,
        tags=["User"],
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "user_id": {"type": "integer"},
                    "status": {"type": "boolean"},
                    "user_email": {"type": "string"},
                },
                "example": {
                    "message": "User registered successfully!",
                    "user_id": 1,
                    "status": True,
                    "user_email": "john@gmail.com",
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": "array", "items": {"type": "string"}},
                },
                "example": {
                    "status": "error",
                    "message": [
                        "email: This field is required.",
                        "password: This field is required.",
                        "first_name: This field is required.",
                        "last_name: This field is required.",
                    ],
                },
            },
        },
    )
    def create(self, request):
        """
        Handle user registration.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully!",
                "user_id": user.id,
                "status": True,
                "user_email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )
