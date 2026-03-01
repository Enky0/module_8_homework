from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from courses.models import Course, Subscription
from django.conf import settings
from django.utils import timezone

from users.models import User


@shared_task
def send_course_update_info(course_id):
    course = Course.objects.get(id=course_id)

    subscriptions = Subscription.objects.filter(course=course)

    for subscription in subscriptions:
        user = subscription.user
        send_mail(
            subject="Обновление курса",
            message=f"Доброго времени суток! Курс {course.name} был обновлен!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    return

@shared_task
def check_user_last_login():
    month_ago = timezone.now() - timedelta(days=30)
    User.objects.filter(last_login__lt=month_ago).update(is_active=False)
