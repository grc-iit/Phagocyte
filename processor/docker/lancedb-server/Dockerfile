FROM python:3.12-slim-bookworm

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    lancedb>=0.10.0 \
    fastapi>=0.104.0 \
    uvicorn>=0.24.0 \
    pydantic>=2.0.0 \
    pyarrow>=14.0.0

# Copy server code
COPY server.py /app/server.py

# Environment
ENV LANCEDB_PATH=/data
ENV PORT=8000

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

CMD ["python", "server.py"]
