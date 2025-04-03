from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ScoreChoices(models.IntegerChoices):
    ONE = 1, '1 (Минимальный)'
    TWO = 2, '2'
    THREE = 3, '3'
    FOUR = 4, '4'
    FIVE = 5, '5 (Средний)'
    SIX = 6, '6'
    SEVEN = 7, '7'
    EIGHT = 8, '8'
    NINE = 9, '9'
    TEN = 10, '10 (Максимальный)'


class Titles(models.Model):
    """Заглушка для модели Titles (временное решение)"""
    title = models.CharField(max_length=256)

    class Meta:
        managed = False  # Не создавать таблицу в БД

    def __str__(self):
        return self.title


class Response(models.Model):
    """Модель отзыва.  """

    title = models.ForeignKey(
        Titles,
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
        choices=ScoreChoices.choices,
        default=ScoreChoices.FIVE
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария.  """

    review = models.ForeignKey(
        Response, on_delete=models.CASCADE,
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
