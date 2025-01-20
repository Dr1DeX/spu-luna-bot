FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ../pyproject.toml /app/pyproject.toml
COPY ../uv.lock /app/uv.lock
COPY ../boto /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["uv", "run", "main.py"]
