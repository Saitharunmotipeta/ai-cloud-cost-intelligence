FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY services/storage-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/storage-service/app ./app

COPY shared ./shared

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]