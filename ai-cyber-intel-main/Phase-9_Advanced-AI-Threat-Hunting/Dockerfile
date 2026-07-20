FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
ENV PATH="/opt/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN groupadd --system phase9 && useradd --system --gid phase9 --home /app phase9
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=phase9:phase9 . .
USER phase9
EXPOSE 8090
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8090/health', timeout=2)"]
CMD ["uvicorn", "run_phase9:app", "--host", "0.0.0.0", "--port", "8090"]
