FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY backend/ /app/backend/
RUN python -c "import backend.database; import backend.models; import backend.scripts.init_db"
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8100"]
