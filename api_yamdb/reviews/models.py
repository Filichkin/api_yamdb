from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import (
    MAX_LENGTH_NAME,
    MAX_LENGTH_SLUG,
    MAX_LENGTH_TEXT
)
from users.models import User
from .validators import validate_for_year, validate_slug


class CategoryGenreModel(models.Model):
    """Базовый класс для моделей Categories и Genres."""

    slug = models.SlugField(
        verbose_name='Cлаг',
        max_length=MAX_LENGTH_SLUG,
        validators=(validate_slug,),
        unique=True,
        db_index=True
    )
    name = models.TextField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f'Название - {self.name}'


class Genre(CategoryGenreModel):
    """
    Модель жанров.
    Одно произведение может быть привязано к нескольким жанрам.
    """

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(CategoryGenreModel):
    """
    Модель категорий.
    Одно произведение может быть привязано только к одной категории.
    """

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель произведений."""

    name = models.TextField(
        verbose_name='Название произведения',
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        validators=[validate_for_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=False,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'Название - {self.name}'


class ReviewCommentModel(models.Model):
    """Базовый класс для моделей Review и Comment."""

    text = models.TextField(
        verbose_name='текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class Review(ReviewCommentModel):
    """
    Модель отзывов.
    Отзыв привязан к определённому произведению.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведения',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return self.text[:MAX_LENGTH_TEXT]

    class Meta(ReviewCommentModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='author_title_connection'
            )
        ]


class Comment(ReviewCommentModel):
    """
    Модель комментариев.
    Комментарий привязан к определённому отзыву.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор',
    )

    def __str__(self):
        self.text[:MAX_LENGTH_TEXT]

    class Meta(ReviewCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
