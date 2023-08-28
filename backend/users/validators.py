import re

from django.conf import settings
from django.core.exceptions import ValidationError

ERROR_MESSAGE = 'Имя пользователя содержит недопустимые символы: {}'


def validate_username(value):
    if (settings.MIN_USERNAME > len(value)
       or settings.MAX_USERNAME < len(value)):
        raise ValidationError(
            f'допустимая длина от {settings.MIN_USERNAME} до'
            f' {settings.MAX_USERNAME} символов.'
        )
    invalid_chars = set(re.findall(settings.EXCEPTION_CHARACTERS, value))
    if invalid_chars:
        raise ValidationError(
            ERROR_MESSAGE.format(''.join(invalid_chars))
        )
    return value
