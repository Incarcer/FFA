# File: FFA/App/backend/Dockerfile

# Use a Python 3.10+ base image as required by yfpy
FROM python:3.10-slim-buster

# Set the working directory inside the container for the backend code.
# This path should match the target path of the volume mount in docker-compose.yml
# (i.e., `/app/backend`) for consistent live reloading during development.
WORKDIR /app/backend

# Copy requirements.txt from the root of the build context (FFA/)
# to a temporary location inside the container, then install dependencies.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the backend application code from its source directory (App/backend)
# relative to the build context (FFA/) into the container's WORKDIR (/app/backend).
COPY App/backend/ .

# Keep the container running indefinitely.
# This ensures the backend service remains "Up" and its mounted volumes are accessible
# for the api_server to import data and modules.
CMD ["tail", "-f", "/dev/null"]
