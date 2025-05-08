#!/bin/bash

HOST={$1:-localhost}
PORT={$2:-5432}

echo "Waiting for postgres at $HOST:$PORT"

while ! nc -z "$HOST" at "$PORT"; do
    sleep 2
done

echo "PostGreSQL is ready"

