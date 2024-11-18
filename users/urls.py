from django.urls import path

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentListAPIView,
                         UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="user-register"),
    path("", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-delete"),
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payments-create"),
]