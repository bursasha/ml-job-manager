#!/bin/sh

# Exit immediately if any command fails
set -e

# Run all pending database migrations
alembic upgrade head

# Launch the FastAPI application via Gunicorn with Uvicorn workers
exec gunicorn "src.main:app" \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --workers 1
