FROM python:3.13-alpine3.21

ARG version=development
ENV VERSION=${version}

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    APP_VENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONPATH="${PYTHONPATH}:/app/metrics/"

WORKDIR /app

RUN adduser -D prometheus

COPY --from=ghcr.io/astral-sh/uv:0.5.29 /uv /bin/

COPY pyproject.toml uv.lock ./

RUN --mount=type=tmpfs,target=/tmp uv sync --frozen

COPY ./metrics /app/metrics/

USER prometheus

EXPOSE 8333

CMD ["uv", "run", "--no-cache", "--offline", "uvicorn", "metrics.main:app", "--host", "0.0.0.0", "--port", "8333"]
