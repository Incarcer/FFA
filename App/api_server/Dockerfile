# File: FFA/App/api_server/Dockerfile

FROM python:3.10-slim-buster

# Set the working directory to the root of your application in the container.
# This makes /app the "parent" directory for the 'api_server' package.
WORKDIR /app

# Copy requirements.txt from the build context root (FFA/)
# to a temporary location inside the container, then install dependencies.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the entire 'api_server' application directory from the build context (FFA/App/api_server)
# into a subdirectory named 'api_server' within the container's WORKDIR (/app/api_server).
# This creates the correct Python package structure.
COPY App/api_server/ ./api_server/

EXPOSE 8000

# Default command to run the FastAPI application using Uvicorn.
# Now, specify the full module path 'api_server.main:app' relative to the WORKDIR (/app).
CMD ["uvicorn", "api_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
