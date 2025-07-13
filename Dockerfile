# Use Python 3.10 slim as base
FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libgbm-dev libgtk-3-0 \
    chromium chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome/Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copy rest of your project files
COPY . .

# Expose Flask default port
EXPOSE 5000

# Start your Flask app (App_V2.py)
CMD ["python", "App_V2.py"]
