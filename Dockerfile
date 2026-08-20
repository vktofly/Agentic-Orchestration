FROM python:3.11-slim-bookworm

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy the application into the container.
COPY . /app

# Working directory
WORKDIR /app

# Install the application dependencies.
RUN uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Ensure we use the dummy store in Docker by default unless overridden
# (To avoid Windows/Linux onnxruntime mismatches unless properly configured)
ENV VECTOR_STORE_TYPE=dummy

EXPOSE 8000

CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
