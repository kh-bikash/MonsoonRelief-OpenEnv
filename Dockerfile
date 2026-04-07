FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

# Enable bytecode compilation for optimal performance
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies optimally with uv
COPY pyproject.toml uv.lock requirements.txt ./
RUN uv sync --frozen --no-install-project --no-dev
RUN uv pip install --system -r requirements.txt

# Copy the actual project code
COPY . .
RUN uv sync --frozen --no-dev

# Expose exactly port 7860 standard for Hugging Face Spaces
EXPOSE 7860

# Command to launch the API server seamlessly 
CMD ["uv", "run", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
