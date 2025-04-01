from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import (
    MAX_LENGTH_NAME,
    MAX_LENGTH_SLUG,
    MAX_LENGTH_TEXT
)
from users.models import User
from .validators import validate_for_year


class BaseModel(models.Model):
    """Абстрактная модель для наследования"""
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME
    )
    slug = models.SlugField(
        verbose_name='Уникальный id',
        max_length=MAX_LENGTH_SLUG,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Categories(BaseModel):
    """
    Категории (типы) произведений.
    Одно произведение может быть привязано только к одной категории.
    """
    class Meta(BaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(BaseModel):
    """
    Жанры произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    """
    class Meta(BaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    """Произведения, к которым пишут отзывы."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=MAX_LENGTH_NAME
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр',
        related_name='titles',
        through='TitleGenre'
    )
    year = models.PositiveIntegerField(
        verbose_name='Дата выхода',
        validators=[validate_for_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    rating = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель, необходимая для связи жанра и произведения."""

    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Reviews(models.Model):
    """
    Отзывы на произведения.
    Отзыв привязан к определённому произведению.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1,
                'Максимально низкая оценка %(limit_value)s!'
            ),
            MaxValueValidator(
                10,
                'Максимально высокая оценка %(limit_value)s!'
            )
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:MAX_LENGTH_TEXT]


class Comments(models.Model):
    """"
    Комментарии к отзывам.
    Комментарий привязан к определённому отзыву.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text[:MAX_LENGTH_TEXT]
