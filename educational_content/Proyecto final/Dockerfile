FROM python:3.11-slim

WORKDIR /app

# Install system deps for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps (CPU-only PyTorch to save space)
COPY requirements.txt .
RUN pip install --no-cache-dir \
    torch==2.3.1+cpu torchvision==0.18.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY api/ ./api/
COPY reports/ ./reports/
COPY models/ ./models/
COPY data/ ./data/

# Expose port
EXPOSE 8000

# Start the API
CMD ["python", "api/main.py"]
