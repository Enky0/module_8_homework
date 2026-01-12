from rest_framework import serializers
from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'preview', 'description')

    preview = serializers.ImageField(required=False, allow_null=True)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name', 'description', 'preview', 'video_url', 'course')

    preview = serializers.ImageField(required=False, allow_null=True)
