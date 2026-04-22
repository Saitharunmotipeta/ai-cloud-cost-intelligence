FROM public.ecr.aws/lambda/python:3.11

# Set working directory (Lambda standard)
WORKDIR /var/task

# 🔥 Env optimizations (keep these)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="/var/task"

# 🔥 Copy requirements
COPY requirements.txt .

# 🔥 Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 Copy application code
COPY app ./app
COPY lambda_function.py .

# 🔥 CRITICAL: shared module
COPY shared ./shared

# 🔥 Lambda entry point (THIS replaces uvicorn)
CMD ["lambda_function.lambda_handler"]