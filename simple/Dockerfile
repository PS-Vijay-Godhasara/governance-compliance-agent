FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY simple/requirements.txt /app/requirements.txt
COPY simple/ui/requirements.txt /app/ui-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r ui-requirements.txt

# Copy application code
COPY simple/ /app/

# Create necessary directories
RUN mkdir -p /app/ui/uploads
RUN mkdir -p /app/policies
RUN mkdir -p /app/knowledge

# Copy policies and knowledge base
COPY simple/policies/ /app/policies/
COPY simple/knowledge/ /app/knowledge/

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=ui/app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Run the application
CMD ["python", "ui/app.py"]