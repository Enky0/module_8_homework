from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonDestroyAPIView, LessonUpdateAPIView, PaymentListAPIView, SubscriptionAPIView, StripeCoursePaymentAPIView, \
    StripeLessonPaymentAPIView, PaymentSuccessView, PaymentCancelView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscription'),

    path('stripe/payment/course/', StripeCoursePaymentAPIView.as_view(), name='stripe_course_payment'),
    path('stripe/payment/lesson/', StripeLessonPaymentAPIView.as_view(), name='stripe_lesson_payment'),
    path('stripe/payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('stripe/payment/cancel/', PaymentCancelView.as_view(), name='payment_cancel'),


] + router.urls
