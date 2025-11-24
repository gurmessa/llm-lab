# Use a Python base image
FROM python:3.11-slim


# Install system libraries required for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code
COPY . /app

# Expose the port
EXPOSE 8083

# Pre-download NLTK punkt tokenizer
RUN python -m nltk.downloader -d /app/nltk_data punkt

# Set environment variable so NLTK uses pre-downloaded data
ENV NLTK_DATA=/app/nltk_data

# Start the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8083"]