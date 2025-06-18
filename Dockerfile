# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy source code and requirements
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r app/requirements.txt

# Optional: Download NLTK + spaCy models during build
RUN python -m nltk.downloader punkt stopwords && \
    python -m spacy download en_core_web_sm

# Expose port for FastAPI app
EXPOSE 8000

# Launch the API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
