# Use official Python image with CUDA support if using GPU
FROM python:3.10-slim

# Set working dir
WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0


# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app ./app
copy ./.env ./.env

# Expose port FastAPI listens on
EXPOSE 8000

# Run uvicorn server with reload disabled for prod
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

