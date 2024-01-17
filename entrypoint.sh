#!/bin/sh
# Apply database migrations
python3 api/manage.py makemigrations
python3 api/manage.py migrate

export DJANGO_SUPERUSER_EMAIL=admin@barapp.com
export DJANGO_SUPERUSER_PASSWORD=admin@123
export DJANGO_SUPERUSER_USERNAME=admin
python3 api/manage.py createsuperuser --no-input
python3 api/manage.py makemigrations
python3 api/manage.py migrate


# Start the Django development server
python3 api/manage.py runserver 0.0.0.0:8080