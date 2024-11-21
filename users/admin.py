from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone' ,'city', 'avatar', 'is_staff', 'display_groups',)

    def display_groups(self, obj):
        # Возвращаем список групп пользователя через запятую
        return ", ".join([group.name for group in obj.groups.all()])

    display_groups.short_description = "Группы"  # Настройка названия колонки
