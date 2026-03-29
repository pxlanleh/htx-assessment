# Task 2e: Dockerfile to containerise the ASR API service

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY asr_api.py .

EXPOSE 8001

CMD ["uvicorn", "asr_api:app", "--host", "0.0.0.0", "--port", "8001"]
