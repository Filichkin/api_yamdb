from rest_framework import serializers

from users.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME
)
from users.models import User
from reviews.models import Category, Genre, Titles
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ('id',)


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = '__all__'
        read_only_fields = ('id',)
