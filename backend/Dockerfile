FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set environment variables for optimization
ENV CONTAINER_HOME=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_LINK_MODE=copy

WORKDIR $CONTAINER_HOME


# Install only essential system dependencies for web API
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/*

# Copy pyproject.toml first for better layer caching
COPY pyproject.toml uv.lock ./
# Install Python if not present and sync dependencies
RUN --mount=type=cache,target=/tmp/uv-cache \
    uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

EXPOSE 8000

# Use the pre-built virtual environment directly
CMD [".venv/bin/python", "server.py"]
