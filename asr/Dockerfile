# Task 2e: Dockerfile to containerise the ASR API service

# Use official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required by librosa for MP3 decoding
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code into the container
COPY asr_api.py .

# Expose the port the API runs on
EXPOSE 8001

# Start the API server
CMD ["uvicorn", "asr_api:app", "--host", "0.0.0.0", "--port", "8001"]
