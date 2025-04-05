from django.core.exceptions import ValidationError
from django.utils import timezone


def validations_year(data_year):
    """Проверяем дату выхода, не позднее текущего года"""
    if timezone.now().year < data_year:
        raise ValidationError(
            (f'{data_year} год из будущего !')
        )
