import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_for_year(value):
    """Дата выхода не может быть позднее текущего года."""
    if value > timezone.now().year:
        raise ValidationError(
            (f'Год {value} позднее текущего года {timezone.now().year}!')
        )


def validate_slug(slug):
    if not re.match(r'[-a-zA-Z0-9_]+$', slug):
        raise ValidationError(
            'В slug нельзя использовать символы оличные от букв и цифр'
        )
    return slug
