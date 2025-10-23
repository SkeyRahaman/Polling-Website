# Use an official Python runtime as a parent image
# python:3.11-slim-bookworm is a good choice for a smaller image
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (optional, but sometimes needed, e.g., if using postgres-related packages)
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#        # build-essential \ # Uncomment if you need to compile C extensions
#        # libpq-dev \     # Uncomment if using psycopg2 (for PostgreSQL)
#     && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
# Use a two-step process to leverage Docker's caching:
# 1. Only copy requirements.txt
COPY requirements.txt .

# 2. Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# expose port used by uvicorn
EXPOSE 8000

# runtime entrypoint (runs wait, migrations, then app)
ENTRYPOINT ["/entrypoint.sh"]