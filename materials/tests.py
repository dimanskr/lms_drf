from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class BaseAPITestCase(APITestCase):
    """
    Базовый тестовый класс для API, предоставляющий общие данные.
    """

    def setUp(self):
        """
        Подготовка общих тестовых данных.
        """
        # Создаем группу модераторов
        self.moder_group = Group.objects.create(name="moders")

        # Создаем пользователей
        self.user = User.objects.create_user(email="user1@mail.ru", password="pass")
        self.owner = User.objects.create_user(email="owner@mail.ru", password="pass")
        self.moderator = User.objects.create_user(
            email="moderator@mail.ru", password="pass"
        )
        self.moderator.groups.add(self.moder_group)

        # Создаем курс
        self.course = Course.objects.create(
            name="Test Course", description="Test Description", owner=self.owner
        )


class CoursesAPITestCase(BaseAPITestCase):
    """
    Тесты для работы с курсами.
    """

    def test_create_course(self):
        """
        Проверяем создание курса владельцем и запрет для модератора.
        """
        self.client.force_authenticate(user=self.owner)
        data = {"name": "New Course", "description": "Course Description"}
        response = self.client.post(reverse("materials:courses-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Course.objects.filter(name="New Course").exists())
        self.assertEqual(Course.objects.all().count(), 2)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(reverse("materials:courses-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_course(self):
        """
        Проверяем получение курса владельцем.
        """
        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:courses-detail", args=[self.course.pk])
        response = self.client.get(url)
        resp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_data.get("name"), self.course.name)

    def test_update_course(self):
        """
        Проверяем обновление курса владельцем и модератором.
        """
        self.client.force_authenticate(user=self.owner)
        data = {"name": "Updated Course"}
        url = reverse("materials:courses-detail", args=[self.course.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data.get("name"), "Updated Course")

        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data.get("name"), "Updated Course")

    def test_delete_course(self):
        """
        Проверяем удаление курса владельцем и запрет удаления модератором.
        """
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:courses-detail", args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:courses-detail", args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.pk).exists())
        self.assertEqual(Course.objects.all().count(), 0)

    def test_list_courses(self):
        """
        Проверяем отображение списка курсов для любого пользователя.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("materials:courses-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Course.objects.count())


class LessonsAPITestCase(BaseAPITestCase):
    """
    Тесты для работы с уроками.
    """

    def setUp(self):
        super().setUp()
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test Description",
            course=self.course,
            owner=self.owner,
        )

    def test_create_lesson(self):
        """
        Проверяем создание урока владельцем и запрет для модератора.
        """
        self.client.force_authenticate(user=self.owner)
        data = {
            "name": "New Lesson",
            "description": "New Description",
            "course": self.course.pk,
        }
        response = self.client.post(reverse("materials:lesson_create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name="New Lesson").exists())
        self.assertEqual(Lesson.objects.all().count(), 2)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(reverse("materials:lesson_create"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson(self):
        """
        Проверяем получение урока.
        """
        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:lesson_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        resp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_data.get("name"), self.lesson.name)

    def test_update_lesson(self):
        """
        Проверяем обновление урока владельцем.
        """
        self.client.force_authenticate(user=self.owner)
        data = {"name": "Updated Lesson"}
        url = reverse("materials:lesson_update", args=[self.lesson.pk])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data.get("name"), "Updated Lesson")

        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data.get("name"), "Updated Lesson")

    def test_delete_lesson(self):
        """
        Проверяем удаление урока владельцем и запрет удаления модератором.
        """
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.pk).exists())
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_list_lessons(self):
        """
        Проверяем отображение списка уроков.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("materials:lesson_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), Lesson.objects.count())


class SubscriptionsAPITestCase(BaseAPITestCase):
    """
    Тесты для работы с подписками.
    """

    def test_subscription_toggle(self):
        """
        Проверяем подписку и отписку на курс.
        """
        self.client.force_authenticate(user=self.user)

        # Подписка
        url = reverse("materials:subscribe-course", args=[self.course.pk])
        response = self.client.post(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Отписка
        response = self.client.post(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
