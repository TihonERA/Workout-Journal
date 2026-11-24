FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY . /app/
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.12-slim
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser
WORKDIR /app
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

USER appuser
COPY --chown=appuser:appgroup ./src ./src
COPY --chown=appuser:appgroup ./alembic ./alembic
COPY --chown=appuser:appgroup ./alembic.ini ./alembic.ini

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
