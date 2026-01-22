from rest_framework import serializers
from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name', 'description', 'preview', 'video_url', 'course')

    preview = serializers.ImageField(required=False, allow_null=True)


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'lesson_count', 'lessons')

    preview = serializers.ImageField(required=False, allow_null=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
