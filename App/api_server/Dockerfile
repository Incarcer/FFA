# File: FFA/App/api_server/Dockerfile

# Use a Python 3.10+ base image as required by yfpy
FROM python:3.10-slim-buster

# Set the working directory inside the container for the API server code.
WORKDIR /app/api_server

# Copy requirements.txt from the root of the build context (FFA/)
# to a temporary location inside the container, then install dependencies.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the api_server application code from its source directory (App/api_server)
# relative to the build context (FFA/) into the container's WORKDIR (/app/api_server).
COPY App/api_server/ .

# Expose the port on which FastAPI will run.
EXPOSE 8000

# Default command to run the FastAPI application using Uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
