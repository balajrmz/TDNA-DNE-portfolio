# Lightweight Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list and install first (better Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the image
COPY . .

# Train the model at build time so the container ships with a ready-to-use model.
# In a real system this might be done in a separate training pipeline,
# but for a portfolio demo this keeps everything self-contained.
RUN python -m sentinelflow.pipeline

# Expose FastAPI's default port
EXPOSE 8000

# Start the FastAPI app when the container runs
CMD ["uvicorn", "sentinelflow.api:app", "--host", "0.0.0.0", "--port", "8000"]

