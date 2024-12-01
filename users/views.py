from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.permissions import IsModer, IsOwner
from users.serializers import PaymentSerializer, UserSerializer, UserPublicSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session, get_status_payment


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
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        stripe_product_id = create_stripe_product(payment)
        price = create_stripe_price(
            stripe_product_id=stripe_product_id, amount=payment.amount
        )
        session_id, payment_link = create_stripe_session(price=price)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()


class PaymentsRetrieveAPIView(RetrieveAPIView):
    """ Проверка статуса платежа """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get(self, request, *args, **kwargs):

        payment_id = request.parser_context['kwargs'].get('pk')
        payment = Payment.objects.get(pk=payment_id)

        # Запрашиваем данные по платежу
        status = get_status_payment(payment.session_id)

        # Присваиваем статус платежа
        payment.payment_status = status.get('payment_status')
        payment.save()

        return super().get(request)