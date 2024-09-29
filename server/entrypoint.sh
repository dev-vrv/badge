#!/bin/bash

# Wait for the database to be ready
echo "Create migrations"

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Start Gunicorn processes
echo Starting Gunicorn.
python manage.py runserver 0.0.0.0:8000