import random
import re
import string

from .constants import (SHORT_LINK_LENGTH, MAX_CUSTOM_ID_LENGTH,
                        CUSTOM_ID_PATTERN)
from .models import URLMap


def is_valid_short_id(short_id):
    return (
        isinstance(short_id, str)
        and len(short_id) <= MAX_CUSTOM_ID_LENGTH
        and re.fullmatch(CUSTOM_ID_PATTERN, short_id) is not None
    )


def get_unique_short_id(length=SHORT_LINK_LENGTH):
    VALID_CHARS = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(VALID_CHARS) for _ in range(length))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id