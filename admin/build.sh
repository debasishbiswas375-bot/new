#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations 
python manage.py migrate

# Admin Credentials: admin | admin123
export DJANGO_SUPERUSER_PASSWORD="admin123"
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true
