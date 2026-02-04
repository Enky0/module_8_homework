from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123', )
        self.course = Course.objects.create(
            name='test_course',
            description='test_description', )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            'name': 'test_lesson_1',
            'description': 'test_description_1',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'course': self.course.id
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lesson(self):
        """Тестирование списка данных урока"""

        Lesson.objects.create(
            name='test_lesson_1',
            description='test_description_1',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course
        )
        Lesson.objects.create(
            name='test_lesson_2',
            description='test_description_1',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course
        )

        response = self.client.get(
            '/lesson/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_detail_lesson(self):
        """Тестирование данных одного урока"""

        test_lesson = Lesson.objects.create(
            name='test_lesson_1',
            description='test_description_1',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course,
            owner=self.user
        )

        response = self.client.get(
            f'/lesson/{test_lesson.id}/'
        )

        # проверка успешного статус-кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка данных
        self.assertEqual(response.data['name'], 'test_lesson_1')
        self.assertEqual(response.data['description'], 'test_description_1')
        self.assertEqual(response.data['video_url'], 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.assertEqual(response.data['course'], self.course.id)

    def test_update_lesson(self):
        """Тестирование обновления данных урока"""

        test_lesson = Lesson.objects.create(
            name='test_lesson_1',
            description='test_description_1',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course,
            owner=self.user
        )

        response = self.client.get(f'/lesson/{test_lesson.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_lesson_1')

        update_data = {
            'name': 'new_test_lesson_1',
            'description': 'new_test_description_1'
        }
        updated_response = self.client.patch(f'/lesson/update/{test_lesson.id}/', data=update_data, format='json')

        self.assertEqual(updated_response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_response.data['name'], 'new_test_lesson_1')
        self.assertEqual(updated_response.data['description'], 'new_test_description_1')

    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        test_lesson = Lesson.objects.create(
            name='test_lesson_1',
            description='test_description_1',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course,
            owner=self.user
        )

        # проверка что успешно создалось
        response = self.client.get(f'/lesson/{test_lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # удаление и проверка что контента нет
        response = self.client.delete(f'/lesson/delete/{test_lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # проверка что данные точно удалены
        response = self.client.get(f'/lesson/{test_lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123', )
        self.course = Course.objects.create(
            name='test_course',
            description='test_description', )
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        """Тестирование создания подписки"""

        # проверка что изначально подписки нет
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # создание подписки и проверка ее успешности
        response = self.client.post('/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('подписка добавлена', response.data['message'])

        # проверка что подписка создалась в БД
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # повторное создание подписки и проверка ее удаления
        response = self.client.post('/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('подписка удалена', response.data['message'])

        # проверка что подписка удалилась из БД
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
