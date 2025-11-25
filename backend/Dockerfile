# Use a Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK resources
RUN python -m nltk.downloader punkt punkt_tab

# Copy the entire application source code
COPY . /app

# Expose the port
EXPOSE 8083

# Start the application using Gunicorn with Uvicorn workers 
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8083", "app.main:app"]

# Start the application using Uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8083"]
