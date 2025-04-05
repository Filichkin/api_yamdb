from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from .constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME,
    MAX_LENGTH_ROLE,
    ROLE_CHOICES
)
from .validators import validate_username


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        blank=False,
        max_length=MAX_LENGTH_NAME,
        unique=True,
        validators=(UnicodeUsernameValidator(), validate_username,),
        verbose_name='Логин'
    )
    email = models.EmailField(
        blank=False,
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        verbose_name='e-mail'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=MAX_LENGTH_ROLE,
        default=UserRole.USER,
        verbose_name='Роль'
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
