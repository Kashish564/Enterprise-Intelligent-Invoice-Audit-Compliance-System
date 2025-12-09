# Use lightweight Python Linux image
FROM python:3.12-slim

# 1. Install System Dependencies (Tesseract OCR & PDF Tools)
# This installs the Linux version of Tesseract automatically
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the Application Code
# We copy everything into /app/backend to match your folder logic
COPY app /app/backend/app

# 5. Set Environment Variable so Python knows where to find modules
ENV PYTHONPATH=/app/backend

# 6. Run the Server
# We start Uvicorn on 0.0.0.0 so Docker can see it
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]