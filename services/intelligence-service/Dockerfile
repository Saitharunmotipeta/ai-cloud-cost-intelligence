FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Copy dependency file first (for caching)
COPY services/intelligence-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY services/intelligence-service/app ./app

# Copy shared module
COPY shared ./shared

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]