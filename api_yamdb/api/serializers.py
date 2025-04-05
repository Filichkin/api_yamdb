from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME
)
from users.models import User
from users.validators import validate_username


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя и отправки кода."""

    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(UnicodeUsernameValidator(), validate_username,)
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL
    )

    def create(self, validated_data):
        try:
            user, _ = User.objects.get_or_create(**validated_data)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Confirmation code',
                f'Code: {confirmation_code}',
                settings.EMAIL_HOST,
                [validated_data.get('email')]
            )
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({'detail': str(e)})


class TokenSerializer(serializers.Serializer):
    """Сериализатор для отправки токена зарегистрированному пользователю."""

    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Неверный код подтверждения')
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели класса User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по категориям."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по жанрам."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для чтения данных.
    Возвращает JSON-данные всех полей модели Title
    для эндпоинта api/v1/titles/.
    Добавляет новое поле rating.
    """

    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для записи данных.
    Возвращает JSON-данные всех полей модели Title
    для эндпоинта api/v1/titles/.
    """

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Возвращает JSON-данные всех полей модели Reviews
    для эндпоинта api/v1/titles/{title_id}/reviews/.
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = Review

    def validate(self, data):
        """Проверка невозможности дважды оставить отзыв на произведение."""

        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context['request'].user
        if Review.objects.filter(
            author=author,
            title_id=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Возаращает JSON-данные всех полей модели Comment
    для эндпоинта api/v1/titles/{title_id}/reviews/{review_id}/comments.
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'pub_date'
        )
        model = Comment
