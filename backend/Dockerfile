# this dockerfile was optimized for prod according to the reqs
# stage 1: build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app

# install build dependencies - only needed for compiling packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# install python packages to user directory
# why? lets us copy just the packages to final image without build tools
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# stage 2: runtime (smaller final image)
FROM python:3.11-slim
WORKDIR /app

# install only runtime dependencies - curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# create non-root user for security
RUN useradd -m -u 1000 appuser

# copy installed packages to appuser's home
COPY --from=builder /root/.local /home/appuser/.local

# copy application code
COPY . .

# fix permissions for app and installed packages
RUN chown -R appuser:appuser /app /home/appuser/.local

USER appuser

# make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

# expose non-privileged port
EXPOSE 8000

# health check for kubernetes
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# run with gunicorn - 4 workers, 2 threads each = 8 concurrent requests per pod
CMD ["gunicorn", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "4", \
    "--threads", "2", \
    "--timeout", "60", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "--log-level", "info", \
    "app:app"]