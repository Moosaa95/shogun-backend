from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User's email address")
    password = serializers.CharField(help_text="User's password", write_only=True)
    first_name = serializers.CharField(help_text="User's first name")
    last_name = serializers.CharField(help_text="User's last name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
