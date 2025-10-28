FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Slack CLI
RUN curl -fsSL https://downloads.slack-edge.com/slack-cli/install.sh | bash

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY app.py ./
COPY version.py ./

# Use uv to run the application
CMD ["uv", "run", "python", "app.py"]

