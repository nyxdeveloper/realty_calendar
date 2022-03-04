import re

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from .exceptions import InvalidPhoneException


def validate_phone(value):
    if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', value) is None:
        raise InvalidPhoneException()
