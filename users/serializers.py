from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, required=False)

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # извлекаем данные о платежах и пароль
        payments = validated_data.pop("payments", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Добаляем платежи
        if payments:
            user.payments.set(payments)

        return user

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "password", "payments",)
