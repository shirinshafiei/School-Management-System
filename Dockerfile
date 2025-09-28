# Use official Python runtime
FROM python:3.11-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for GIS
RUN apt-get update && \
    apt-get install -y \
    binutils \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    proj-bin \
    postgresql-client && \
    apt-get clean all

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY . .