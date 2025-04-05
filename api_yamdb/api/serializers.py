from rest_framework import serializers

from users.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME
)
from users.models import User
from reviews.models import Category, Genre, Title
from users.validators import validate_username
from reviews.models import Comment, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'comments')

    def validate(self, data):
        """Проверка уникальности отзыва пользователя на произведение."""
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user

        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data
=======
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        read_only_fields = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        read_only_fields = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )


class TitlesWriteSerializer(serializers.ModelSerializer):
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
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

