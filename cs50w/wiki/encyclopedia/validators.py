from django.core.exceptions import ValidationError

from . import util


def validate_title(value):
    content = util.get_entry(value)

    if content:
        raise ValidationError(
            f"A page with title of {value} already exists.",
        )