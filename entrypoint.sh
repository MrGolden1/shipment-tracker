#!/bin/sh

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z 172.23.0.2 5432; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi
sleep 2

pip install -r requirements.txt
python manage.py makemigrations shipments --noinput
python manage.py migrate --noinput

exec "$@"
