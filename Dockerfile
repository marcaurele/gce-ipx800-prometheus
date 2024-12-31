###############
# BUILD STAGE #
# Put here any build steps in order to not install building tools into the final image
###############

####################
# BACKEND BUILDER #
####################
FROM python:3.13-alpine as builder

ARG version=development
ENV VERSION=${version}

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV APP_VENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONPATH="${PYTHONPATH}:/app/metrics/"

RUN set -ex \
    && adduser -D prometheus \
    && uv sync --frozen \
    && rm -rf /var/cache/apk/*

COPY ./metrics /app/metrics/

# Switch to non-root user
USER prometheus

EXPOSE 8333

CMD ["uv", "run", "uvicorn", "metrics.main:app", "--host", "0.0.0.0", "--port", "8333"]
