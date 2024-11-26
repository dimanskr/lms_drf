from django.db import models

NULLABLE = {"null": True, "blank": True}

class Course(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/",
        verbose_name="Фото курса",
        **NULLABLE,
        help_text="Загрузите фото курса"
    )
    description = models.TextField(
        verbose_name="Описание курса", **NULLABLE, help_text="Введите описание курса"
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Владелец",
        related_name="course"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = (
            "name",
        )


class Lesson(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", **NULLABLE, help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="lessons/",
        verbose_name="Фото урока",
        **NULLABLE,
        help_text="Загрузите фото урока"
    )
    video_url = models.URLField(verbose_name="Видеоурок", **NULLABLE)
    course = models.ForeignKey(
        "materials.Course", on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Владелец",
        related_name="lessons"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = (
            "name",
            "course",
        )


class Subscription(models.Model):
    """
    Модель подписки
    """
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        verbose_name="курс",
        related_name="subscriptions",
    )

    def __str__(self):
        return f"Подписка пользователя {self.user} на курс {self.course}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
