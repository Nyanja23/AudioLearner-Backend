FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini .

# Health check. Uses urllib from the standard library (`requests` is not a
# dependency of this service) and honours $PORT so the check follows the port
# the app is actually listening on.
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import os,urllib.request; urllib.request.urlopen('http://localhost:'+os.getenv('PORT','8000')+'/health')"

# Run the application.
# SHELL form on purpose: Railway (and most PaaS) inject the port to bind as
# $PORT at runtime, and a JSON/exec-form CMD would pass the literal string
# "$PORT" to uvicorn. Falls back to 8000 for local docker-compose.
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
