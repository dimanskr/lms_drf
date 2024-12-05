from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import User


@shared_task
def block_inactive_users():
    month_ago = now() - timedelta(days=31)
    passive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    for user in passive_users:
        user.is_active = False
        user.save()