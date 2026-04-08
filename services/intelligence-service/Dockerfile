FROM python:3.11-slim

WORKDIR /app

# 🔥 System optimizations
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 🔥 Install only essential system deps (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 🔥 Copy only requirements first (cache layer)
COPY services/intelligence-service/requirements.txt .

# 🔥 Install dependencies (cached unless requirements change)
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 Copy app code (separate layer → faster rebuilds)
COPY services/intelligence-service/app ./app
COPY shared ./shared

# 🔥 Use non-root user (production best practice)
RUN useradd -m appuser
USER appuser

EXPOSE 8000

# 🔥 Faster startup + better performance tuning
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]