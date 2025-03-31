from rest_framework import serializers

from users.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME
)
from users.models import User
from users.validators import validate_username


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(validate_username,)
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class OwnerUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
