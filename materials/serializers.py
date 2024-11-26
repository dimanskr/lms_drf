from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import youtube_url_validator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[youtube_url_validator], required=False)
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"
