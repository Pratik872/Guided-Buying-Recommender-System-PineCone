FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download models during build
RUN python -c "import sentence_transformers; sentence_transformers.SentenceTransformer('all-mpnet-base-v2', cache_folder='/tmp/.cache')"
RUN python -c "from transformers import pipeline; pipeline('ner', model='Babelscape/wikineural-multilingual-ner', cache_dir='/tmp/.cache')"

# Copy application files
COPY src/ ./src/
COPY config/ ./config/
COPY app.py .
COPY .env* ./

# Create directories
RUN mkdir -p logs temp && chmod 755 logs temp
RUN mkdir -p /tmp/.cache && chmod 777 /tmp/.cache
ENV SENTENCE_TRANSFORMERS_HOME=/tmp/.cache

# Expose port for HuggingFaces
EXPOSE 7860

# Expose port for HuggingFaces
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/_stcore/health || exit 1

# Environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]