from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

MIN_YEAR = 1900
MAX_YEAR = 2025
MIN_RATING = 1
MAX_RATING = 10
MAX_LENGTH_TITLE = 128
MAX_LENGTH_SLUG = 50


class BaseClass(models.Model):
    """Абстрактная базовая модель для категорий и жанров."""

    name = models.CharField(
        'Наименование',
        max_length=MAX_LENGTH_TITLE,
        help_text=f'Название макс. {MAX_LENGTH_TITLE} символов'
    )
    slug = models.SlugField(
        'Идентификатор',
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
        return f'Категория: {self.title}'


class Genre(BaseClass):
    """Модель жанра произведения."""

    def __str__(self):
        return f'Жанр: {self.title}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    """Модель произведения (фильма, книги и т.д.)."""

    name = models.CharField(
        'Наименование',
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
        'Год',
        validators=[
            MinValueValidator(MIN_YEAR),
            MaxValueValidator(MAX_YEAR)
        ],
        db_index=True,
        help_text=f'Год выпуска (от {MIN_YEAR} до {MAX_YEAR})'
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
        default=''
    )
    rating = models.IntegerField(
        'Рейтинг',
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING)
        ],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'Произведение: {self.name}'
