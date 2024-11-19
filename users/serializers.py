from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, required=False)

    def create(self, validated_data):
        # извлекаем данные о платежах
        payments = validated_data.pop("payments", None)
        user = User(**validated_data)
        user.save()

        # Добаляем платежи
        if payments:
            user.payments.set(payments)

        return user

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "password", "payments",)
