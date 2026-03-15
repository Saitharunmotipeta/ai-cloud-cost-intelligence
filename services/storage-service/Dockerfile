FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# install dependencies
COPY services/storage-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy service code
COPY services/storage-service/app ./app

# copy shared modules
COPY shared ./shared

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]