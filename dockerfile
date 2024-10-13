# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Collect static files
RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Use gunicorn to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "TurfBooking.wsgi:application"]
