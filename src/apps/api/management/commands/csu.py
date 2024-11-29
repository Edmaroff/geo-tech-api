from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает суперпользователя с логином и паролем admin/admin"

    def handle(self, *args, **kwargs):
        username = "admin"
        password = "admin"
        email = "admin@localhost"

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING("Суперпользователь с логином 'admin' уже существует")
            )
            return

        try:
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email,
            )
            self.stdout.write(self.style.SUCCESS("Суперпользователь успешно создан"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при создании суперпользователя: {str(e)}")
            )
