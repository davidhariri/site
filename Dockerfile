# Use the specified image as the base
FROM python:3.12-slim

# Set the working directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock /usr/src/app/

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-dev

# Copy only necessary files
COPY . /usr/src/app/

# Remove cache to reduce image size
RUN rm -rf /root/.cache/pip

# Expose the application's port
EXPOSE 8000

# Set the entry point of the application
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app", "--timeout", "10"]
