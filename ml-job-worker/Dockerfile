# Use official slim Python 3.11 base image for minimal footprint
FROM python:3.11-slim

# Prevent generation of .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

# Install build dependencies (GCC, Python headers) then clean up apt cache
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for the Celery Worker application
WORKDIR /ml-job-worker

# Copy only requirements first to leverage cache
COPY requirements.txt ./

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Worker source code into the container
COPY . .

# Ensure any shell scripts in ./scripts are executable
RUN chmod +x ./scripts/*.sh
