# Use Python base image
FROM python:3.9.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI server using python api.py
CMD ["python", "API/api.py"]
