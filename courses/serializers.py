from rest_framework import serializers
from courses.models import Course, Lesson, Payment, Subscription
from courses.validators import YouTubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[YouTubeURLValidator('video_url')])

    class Meta:
        model = Lesson
        fields = ('name', 'description', 'preview', 'video_url', 'course', 'owner')

    preview = serializers.ImageField(required=False, allow_null=True)


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'lesson_count', 'lessons', 'owner')

    preview = serializers.ImageField(required=False, allow_null=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
