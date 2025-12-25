from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User's email address")
    password = serializers.CharField(help_text="User's password", write_only=True)
    first_name = serializers.CharField(help_text="User's first name")
    last_name = serializers.CharField(help_text="User's last name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data in responses"""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that includes user data in the response"""

    def validate(self, attrs):
        # Get the default token data
        data = super().validate(attrs)

        # Add custom user data to the response
        data['user'] = UserSerializer(self.user).data
        data['status'] = True

        return data
