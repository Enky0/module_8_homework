from datetime import datetime

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from courses.paginators import StandardPagination
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from courses.models import Course, Lesson, Payment, Subscription
from courses.services import create_product, create_price, create_checkout_session
from users.permissions import IsModerator, IsOwner


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "delete":
            self.permission_classes = (~IsModerator, IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = StandardPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    pagination_class = StandardPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

    ordering_fields = ['payment_date', ]


class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'

        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})


class PaymentSuccessView(APIView):
    def get(self, request):
        payment_id = request.GET.get('payment_id')

        return Response({
            'status': 'success',
            'message': 'Оплата прошла',
            'payment_id': payment_id,
        })


class PaymentCancelView(APIView):
    def get(self, request):
        payment_id = request.GET.get('payment_id')

        return Response({
            'status': 'cancel',
            'message': 'Оплата отменена',
            'payment_id': payment_id,
        })


class StripeCoursePaymentAPIView(APIView):
    def post(self, request):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        stripe_product = create_product(product_name=course.name, description=course.description)
        stripe_price = create_price(stripe_product.id, course.price)
        stripe_checkout_session = create_checkout_session(stripe_price.id)

        payment = Payment.objects.create(
            user=request.user,
            payment_date=datetime.now(),
            paid_course=course,
            paid_lesson=None,
            payment_method=Payment.CARD,
            stripe_product_id=stripe_product.id,
            stipe_price_id=stripe_price.id,
            stripe_checkout_session_id=stripe_checkout_session.id,
            stripe_payment_status=Payment.UNPAID,
            stripe_payment_url=stripe_checkout_session.url
        )

        return Response({'payment_id': payment.id, 'checkout_url': stripe_checkout_session.url, },
                        status=status.HTTP_201_CREATED)


class StripeLessonPaymentAPIView(APIView):
    def post(self, request):
        lesson_id = request.data.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)

        stripe_product = create_product(product_name=lesson.name, description=lesson.description)
        stripe_price = create_price(stripe_product.id, lesson.price)
        stripe_checkout_session = create_checkout_session(stripe_price.id)

        payment = Payment.objects.create(
            user=request.user,
            payment_date=datetime.now(),
            paid_course=None,
            paid_lesson=lesson,
            payment_method=Payment.CARD,
            stripe_product_id=stripe_product.id,
            stipe_price_id=stripe_price.id,
            stripe_checkout_session_id=stripe_checkout_session.id,
            stripe_payment_status=Payment.UNPAID,
            stripe_payment_url=stripe_checkout_session.url
        )

        return Response({'payment_id': payment.id,'checkout_url': stripe_checkout_session.url,},
                        status=status.HTTP_201_CREATED)
