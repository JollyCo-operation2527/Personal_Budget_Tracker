#!/bin/bash

HOST_PORT="$1"

echo "Waiting for postgres at localhost:5432"

while ! nc -z localhost 5432; do
    sleep 1
done

echo "PostGreSQL is ready"

shift # remove "db:5432" from the argument list

echo "Running migrate"
python manage.py migrate

exec "$@"

