from rest_framework import serializers

from reviews.models import Categories, Genres, Reviews, Titles
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
        validators=(validate_username,)
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL
    )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для отправки токена зарегистрированному пользователю."""

    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели класса User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class OwnerUserSerializer(UserSerializer):
    """Сериализатор для запросов по категориям."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по категориям."""

    class Meta:
        model = Categories
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов по жанрам."""

    class Meta:
        model = Genres
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
        model = Titles


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для записи данных.
    Возвращает JSON-данные всех полей модели Title
    для эндпоинта api/v1/titles/.
    """

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
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
        model = Titles


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
        model = Reviews

    def validate(self, data):
        """Проверка невозможности дважды оставить отзыв на произведение."""

        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context['request'].user
        if Reviews.objects.filter(
            author=author,
            title_id=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение.'
            )
        return data
