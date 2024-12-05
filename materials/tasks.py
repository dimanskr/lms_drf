from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course, Subscription


@shared_task
def course_update_notification(course_pk):
    course = Course.objects.filter(pk=course_pk).first()
    subscribers = Subscription.objects.filter(course=course).select_related("user")
    emails = [sub.user.email for sub in subscribers if sub.user.email]
    if emails:
        send_mail(
            subject=f'Обновление курса "{course.name}"',
            message=f'Здравствуйте! Курс "{course.name}" обновился!',
            from_email=EMAIL_HOST_USER,
            recipient_list=emails,
        )