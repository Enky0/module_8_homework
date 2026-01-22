from django.core.management.base import BaseCommand
from courses.models import Course, Lesson, Payment
from users.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'add test payment data to database'

    def handle(self, *args, **options):
        # удаление существующих данных
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.all().delete()
        Payment.objects.all().delete()

        # создание курсов
        test_courses = [
            {'name': 'Питон-разработчик', 'description': 'Курс разработки на питоне'},
            {'name': 'Тестировщик', 'description': 'Курс тестировщика'},
        ]

        for courses_data in test_courses:
            course, created = Course.objects.get_or_create(**courses_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Course successfully added: {course.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Course already exists: {course.name}'))

        # запись курсов в переменную для использования в коде создании продуктов
        python_course = Course.objects.get(name='Питон-разработчик')
        testing_course = Course.objects.get(name='Тестировщик')

        # создание уроков
        test_lessons = [
            {'name': 'Как написать свой первый Hello World', 'description': 'Пишем', 'course': python_course},
            {'name': 'Как протестировать чей-то первый Hello World', 'description': 'Тестируем',
             'course': testing_course},
        ]

        for lessons_data in test_lessons:
            lesson, created = Lesson.objects.get_or_create(**lessons_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Lesson successfully added: {lesson.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Lesson already exists: {lesson.name}'))

        # создание тестовых пользователей
        test_users = [
            {
                'email': 'coder1@coder.com',
                'password': 'coder123',
                'phone': '+79991112233',
                'city': 'Coder-City',
            },
            {
                'email': 'coder2@coder.com',
                'password': 'coder123',
                'phone': '+78881112233',
                'city': 'Coder-City',
            },
            {
                'email': 'tester1@tester.com',
                'password': 'tester123',
                'phone': '+79992223344',
                'city': 'Tester-City',
            },
            {
                'email': 'tester2@tester.com',
                'password': 'tester123',
                'phone': '+78882223344',
                'city': 'Tester-City',
            },
            {
                'email': 'admin@admin.com',
                'password': 'admin123',
                'phone': '+79993334455',
                'city': 'Admin-City',
                'is_staff': True,
                'is_superuser': True
            }
        ]

        # уроки
        python_lesson = Lesson.objects.get(name='Как написать свой первый Hello World')
        testing_lesson = Lesson.objects.get(name='Как протестировать чей-то первый Hello World')

        for users_data in test_users:
            password = users_data.pop('password')

            user, created = User.objects.get_or_create(**users_data)

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'User successfully added: {user.email}')
            else:
                self.stdout.write(f'User already exists: {user.email}')

        # пользователи
        coder_user_1 = User.objects.get(email='coder1@coder.com')
        coder_user_2 = User.objects.get(email='coder2@coder.com')
        tester_user_1 = User.objects.get(email='tester1@tester.com')
        tester_user_2 = User.objects.get(email='tester2@tester.com')

        # создание оплаты

        test_payment = [
            {
                'user': coder_user_1,
                'payment_date': timezone.now(),
                'paid_course': python_course,
                'paid_lesson': None,
                'payment_method': Payment.CARD
            },
            {
                'user': coder_user_2,
                'payment_date': timezone.now(),
                'paid_course': None,
                'paid_lesson': python_lesson,
                'payment_method': Payment.CASH
            },
            {
                'user': tester_user_1,
                'payment_date': timezone.now(),
                'paid_course': testing_course,
                'paid_lesson': None,
                'payment_method': Payment.CARD
            },
            {
                'user': tester_user_2,
                'payment_date': timezone.now(),
                'paid_course': None,
                'paid_lesson': testing_lesson,
                'payment_method': Payment.CASH
            },
        ]

        for payment_data in test_payment:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Payment successfully added: {payment.user.email}, {payment.payment_date}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment already exists: {payment.user.email}, {payment.payment_date}'))
