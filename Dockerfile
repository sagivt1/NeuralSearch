# Use a slim Python image to keep the final image size down.
FROM python:3.12-slim

WORKDIR /app

# Install build-time dependencies for Python packages with C extensions (e.g., psycopg2).
# Clean up apt cache in the same layer to reduce image size.
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Use a multi-stage build to copy the `uv` binary directly.
# This is faster and cleaner than installing it via pip.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

# Install dependencies from the lock file, excluding development packages.
# `--frozen` ensures reproducibility.
RUN uv sync --frozen --no-dev

COPY . .

# Add the virtual environment's bin directory to the PATH.
# Allows running installed Python packages like `uvicorn` directly.
ENV PATH="/app/.venv/bin:$PATH"

# Run the application using `uv run` to ensure it uses the correct environment.
# Bind to 0.0.0.0 to make the server accessible from outside the container.
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
