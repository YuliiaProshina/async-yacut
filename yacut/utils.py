import random
import string

from .constants import SHORT_LINK_LENGTH
from .models import URLMap


def get_unique_short_id(length=SHORT_LINK_LENGTH):
    VALID_CHARS = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(VALID_CHARS) for _ in range(length))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id