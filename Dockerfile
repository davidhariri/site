# Use the specified image as the base
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /usr/src/app

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev \
    && pip install --no-cache-dir uvicorn

# Copy application code
COPY . .

# Create final slim image
FROM python:3.12-slim

WORKDIR /usr/src/app

# Copy only the installed packages and application code
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/src/app/ ./
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/

# Expose the application's port
EXPOSE 8000

# Set the entry point of the application
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app:app", "--workers", "1"]
