FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# -------------------------
# Install dependencies (cache friendly)
# -------------------------
COPY services/analytics-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------------------------
# Copy full service code
# -------------------------
COPY services/analytics-service /app

# -------------------------
# Copy shared module
# -------------------------
COPY shared /app/shared

# -------------------------
# Run service
# -------------------------
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]