# Stage 1: Build stage
FROM python:3.10-alpine AS builder

# Install build dependencies
RUN apk add --no-cache build-base gcc libffi-dev musl-dev

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final stage
FROM python:3.10-alpine

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Install runtime dependencies
RUN apk add --no-cache libffi

# Set working directory
WORKDIR /app

# Copy the application code
COPY . .

# Default port, can be overridden by environment variable
ENV PORT=8000

# Expose the default port
EXPOSE $PORT

# Command to run the application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
