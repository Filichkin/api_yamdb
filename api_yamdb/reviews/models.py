from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Title(models.Model):
    """Заглушка для модели Titles (временное решение)"""
    title = models.CharField(max_length=256)

    class Meta:
        managed = False

    def __str__(self):
        return self.title


class Review(models.Model):
    """Модель отзыва.  """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария.  """

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text
