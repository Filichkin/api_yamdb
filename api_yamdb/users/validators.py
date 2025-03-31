import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError(
            'В логине нельзя использовать символы, отличные от букв'
            'в верхнем и нижнем регистрах, цифр, знаков подчеркивания,'
            'точки, знаков плюса, минуса и знака (@)'
        )
    return username
