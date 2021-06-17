import random
import string

from django.utils.text import slugify
from unidecode import unidecode


def random_string(length = 10, charset = string.ascii_letters + string.digits):
    return "".join(random.choices(charset, k=length))


def generate_slug(value, max_length=64, count = 10, sufix_generator=random_string()):
    sufix = ""
    for _ in range(count):
        slug = slugify(unidecode(value))
        yield slug[:max_length] if not sufix else "-".join([slug[: max_length - (len(sufix) + 1)], sufix])
        sufix = sufix_generator()
