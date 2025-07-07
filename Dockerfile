# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget curl unzip gnupg && \
    apt-get install -y chromium chromium-driver && \
    pip install --upgrade pip

# Install Python dependencies
RUN pip install flask flask-socketio eventlet selenium

# Set environment variable for headless Chrome
ENV CHROME_BIN=/usr/bin/chromium

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "App_V2.py"]
