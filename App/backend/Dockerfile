# File: FFA/App/backend/Dockerfile

# Use a Python 3.10+ base image as required by yfpy
FROM python:3.10-slim-buster

# Set the working directory inside the container for the backend code.
WORKDIR /app/backend

# Copy requirements.txt from the root of the build context (FFA/)
# to a temporary location inside the container, then install dependencies.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the backend application code from its source directory (App/backend)
# relative to the build context (FFA/) into the container's WORKDIR (/app/backend).
COPY App/backend/ .

# Define the default command to run the backend service.
# Replace with the actual command to start your backend logic.
# CMD ["python", "run_backend.py"]
