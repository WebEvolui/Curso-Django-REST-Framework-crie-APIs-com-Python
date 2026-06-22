# Use a lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Copy requirements first (leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install gunicorn && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Run entrypoint
ENTRYPOINT ["/entrypoint.sh"]