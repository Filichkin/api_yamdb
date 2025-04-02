from .validations import validations_year
from django.db import models

from .constants import MAX_LENGTH_SLUG, MAX_LENGTH_TITLE


class BaseClass(models.Model):
    """Абстрактная базовая модель для категорий и жанров."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=MAX_LENGTH_TITLE,
        help_text=f'Название макс. {MAX_LENGTH_TITLE} символов'
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
        'цифры, дефис и подчёркивание, значение должно быть уникальным.'
    )

    class Meta:
        abstract = True


class Category(BaseClass):
    """Модель категории произведения."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория: {self.name}'


class Genre(BaseClass):
    """Модель жанра произведения."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'Жанр: {self.name}'


class Titles(models.Model):
    """Модель произведения (фильма, книги и т.д.)."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=MAX_LENGTH_TITLE,
        help_text=f'Название произведения (макс. {MAX_LENGTH_TITLE} символов)'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        related_name='titles',
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[
            validations_year
        ],
        help_text='Год выпуска не позднее текущего'
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'Произведение: {self.name}'
