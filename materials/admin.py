from django.contrib import admin
from materials.models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "description", "preview")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course", "owner", "video_url", "preview")
