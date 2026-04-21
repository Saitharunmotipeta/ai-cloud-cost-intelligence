FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# -------------------------
# Install dependencies first (cache optimization)
# -------------------------
COPY services/ingestion-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------------------------
# Copy service code
# -------------------------
COPY services/ingestion-service /app

# -------------------------
# Copy shared module (CRITICAL)
# -------------------------
COPY shared /app/shared

# -------------------------
# Run service
# -------------------------
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]