from rest_framework.exceptions import ValidationError


def validate_score(value):
    if not 1 <= value <= 10:
        raise ValidationError('Оценка должна быть от 1 до 10!')
