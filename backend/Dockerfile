ARG ENVIRONMENT=development
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.8.2

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies (optimized for caching)
COPY requirements.txt /app/

# Create a virtual environment
RUN python -m venv /venv && \
    . /venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Set permissions for non-root user
RUN chown -R django:django /app && \
    chmod -R 755 /app

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && \
    chown django:django /app/logs

# Set non-root user
USER django

# Expose port
EXPOSE 8000

# Set environment
ENV PATH="/venv/bin:$PATH"

# For development, use runserver
# For production, use gunicorn
CMD ["sh", "-c", "if [ \"$ENVIRONMENT\" = \"production\" ]; then \
        gunicorn -c gunicorn.conf.py fusionforms.wsgi:application; \
    else \
        python manage.py migrate --noinput && \
        python manage.py runserver 0.0.0.0:8000; \
    fi"]