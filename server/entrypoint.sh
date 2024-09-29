#!/bin/bash

# Wait for the database to be ready
echo "Create migrations"

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Создание суперпользователя, если его нет
echo "Creating superuser if it doesn't exist"

python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(email=email, password=password)
EOF

# Start Gunicorn processes
echo "Starting Gunicorn."
python manage.py runserver 0.0.0.0:8000
