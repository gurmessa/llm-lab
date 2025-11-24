FROM python:3.11-slim

# Install system dependencies for numpy, scikit-learn, SQLAlchemy
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libgomp1 \
    libffi-dev \
    libssl-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . /app

# Pre-download NLTK punkt
RUN python -m nltk.downloader -d /app/nltk_data punkt
ENV NLTK_DATA=/app/nltk_data

EXPOSE 8083
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8083"]
