# # Use official Python image with CUDA support if using GPU

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENV CHROMA_TELEMETRY_ENABLED=false


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
