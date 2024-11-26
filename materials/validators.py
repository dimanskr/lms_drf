import re
from rest_framework.exceptions import ValidationError


def youtube_url_validator(value):
    """
    Валидатор для проверки, является ли значение ссылкой на YouTube.
    """
    youtube_regex = re.compile(
        r'^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/'
        r'(?:watch\?v=|embed\/|v\/|shorts\/|playlist\?list=)|youtu\.be\/)([\w\-]{11})(?:[&?=\w\-]*)?$'
    )
    if not youtube_regex.match(value):
        raise ValidationError("Ссылка должна вести на YouTube.")