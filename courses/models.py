from django.db import models
from users.models import User
from django.db.models import ForeignKey, SET_NULL


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='photos/', verbose_name='превью курса', null=True, blank=True)
    description = models.TextField(verbose_name='описание курса')
    price = models.IntegerField(default=1, verbose_name='Цена курса в рублях')
    owner = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='courses')

    def __str__(self):
        return f"Название курса: {self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    preview = models.ImageField(upload_to='photos/', verbose_name='превью урока', null=True, blank=True)
    video_url = models.URLField(verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    price = models.IntegerField(default=1, verbose_name='Цена урока в рублях')
    owner = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='lessons')

    def __str__(self):
        return f"Название урока: {self.name}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    CARD = 'card'
    CASH = 'cash'

    PAYMENT_METHODS = [
        (CARD, 'Карта'),
        (CASH, 'Наличные'),
    ]

    PAID = 'paid'
    UNPAID = 'unpaid'

    PAYMENT_STATUS = [
        (PAID, 'Оплачено'),
        (UNPAID, 'Неоплачено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_payments', null=True,
                                    blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_payments', null=True,
                                    blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default=CARD,
                                      verbose_name='способ оплаты')

    stripe_product_id = models.CharField(max_length=300, blank=True, null=True, verbose_name='id продукта в stripe')
    stipe_price_id = models.CharField(max_length=300, blank=True, null=True, verbose_name='id цены в stripe')
    stripe_checkout_session_id = models.CharField(max_length=300, blank=True, null=True,
                                                  verbose_name='id сессии оплаты в stripe')
    stripe_payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default=UNPAID,
                                             verbose_name='Статус оплаты в stripe')
    stripe_payment_url = models.TextField(blank=True, null=True, verbose_name='Ссылка для оплаты')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        unique_together = ['user', 'course']
