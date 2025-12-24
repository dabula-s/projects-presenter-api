#!/bin/bash

alembic -n postgres upgrade head

ENVIRONMENT="${ENVIRONMENT:-dev}"

if [ "$ENVIRONMENT" = "dev" ]; then
    exec python -m flask --app presentation.api.main:create_app run --host=0.0.0.0 --port=8000 --debug
elif [ "$ENVIRONMENT" = "prod" ]; then
    exec gunicorn --bind 0.0.0.0:8000 presentation.api.main:app
else
    echo "Error: ENVIRONMENT variable is not set correctly. Use 'dev' or 'prod'."
    exit 1
fi