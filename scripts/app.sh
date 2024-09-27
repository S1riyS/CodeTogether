#!/bin/bash

# Applying migrations
echo "Running migrations..."
alembic upgrade head


# Starting gunicorn
cd src
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000