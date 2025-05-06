#!/bin/bash

HOST_PORT="$1"

echo "Waiting for postgres at db:5432"

while ! nc -z db 5432; do
    sleep 1
done

echo "PostGreSQL is ready"

shift # remove "db:5432" from the argument list

exec "$@"