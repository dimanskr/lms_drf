from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import youtube_url_validator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(
        validators=[youtube_url_validator], required=False
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        request = self.context.get("request")
        if not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=course).exists()

    class Meta:
        model = Course
        fields = "__all__"
