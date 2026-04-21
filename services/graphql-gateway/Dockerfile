FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# -------------------------
# Install dependencies
# -------------------------
COPY services/graphql-gateway/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------------------------
# Copy full service code
# -------------------------
COPY services/graphql-gateway /app

# -------------------------
# Copy shared module
# -------------------------
COPY shared /app/shared

# -------------------------
# Run service
# -------------------------
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]