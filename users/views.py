from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserPublicSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserPublicSerializer
    queryset = User.objects.all()

class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Выбираем сериализатор в зависимости от владельца.
        """
        if self.request.user == self.get_object():
            return UserSerializer  # Полная информация для владельца
        return UserPublicSerializer  # Общая информация для других пользователей


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        # Разрешаем редактирование только владельцу профиля
        if self.request.user != self.get_object():
            raise PermissionDenied("Вы можете редактировать только свой профиль.")
        # Сохраняем обновленные данные пользователя
        user = serializer.save()

        # Хэшируем пароль, если он передан
        if 'password' in serializer.validated_data:
            user.set_password(serializer.validated_data['password'])
            user.save()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        # Удаление разрешено только владельцу
        if self.request.user != instance:
            raise PermissionDenied("Вы можете удалять только свой профиль.")
        super().perform_destroy(instance)


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = (
        "payment_date",
        "amount",
    )
    search_fields = ("payment_method",)
    filterset_fields = (
        "payment_date",
        "course",
        "lesson",
        "payment_method",
    )


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
