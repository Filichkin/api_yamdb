from django.core.exceptions import ValidationError

from .constants import NOT_ALLOWED_NAMES


def validate_username(username):
    if username.lower() in NOT_ALLOWED_NAMES:
        raise ValidationError(
            f'Зарезервированный логин {username}, нельзя использолвать'
        )
    return username
