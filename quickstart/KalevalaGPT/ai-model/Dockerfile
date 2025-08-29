# Use official Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy the rest of the project
COPY . .

# Expose the API port
EXPOSE 8000

# Run Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8000", "api.app:app", "--workers=2", "--threads=4"]
