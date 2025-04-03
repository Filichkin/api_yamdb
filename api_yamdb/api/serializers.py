from rest_framework import serializers

from users.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME
)
from users.models import User
from users.validators import validate_username
from reviews.models import Comment, Response


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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ResponseSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Response
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'comments')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')
