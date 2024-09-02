import os

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerShop.settings')

import django

# Инициализация Django
django.setup()

from django.contrib.auth.models import User

# Создание миграций
os.system('python manage.py makemigrations')

# Выполнение миграций
os.system('python manage.py migrate')

# Сборка статических файлов
os.system('python manage.py collectstatic')

# Создание суперпользователя
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.py', 'admin@pass')
    print("Суперпользователь создан успешно.")
else:
    print("Суперпользователь уже существует.")