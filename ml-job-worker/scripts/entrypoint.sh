#!/bin/sh

# Exit immediately if any command fails
set -e

# Launch the Celery worker:
#   -A: module:attribute pointing to the Celery app instance
#   --concurrency=2: number of worker processes
#   --loglevel=info: set logging verbosity
exec celery -A "src.main:app" worker \
    --concurrency=2 \
    --loglevel=info
