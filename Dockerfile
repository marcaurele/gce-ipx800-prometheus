###############
# BUILD STAGE #
# Put here any build steps in order to not install building tools into the final image
###############

####################
# BACKEND BUILDER #
####################
FROM python:3.11-alpine as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # poetry
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV=/opt/poetry-venv


RUN set -ex \
    && python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install poetry

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Generate requirements.txt file from poetry lock and create wheels packages
RUN set -ex \
    && poetry export \
        --output requirements.txt \
    && pip wheel \
        --wheel-dir ./wheels/ \
        --requirement requirements.txt \
    && poetry export \
        --with dev \
        --output requirements-dev.txt \
    && cp -r ./wheels/ ./wheels-dev/ \
    && pip wheel \
        --wheel-dir ./wheels-dev/ \
        --requirement requirements-dev.txt

#################
# Runtime stage #
#################
FROM python:3.11-alpine as production

ARG version=development
ENV VERSION=${version}

ENV APP_VENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONPATH="${PYTHONPATH}:/app/metrics/"

# Copy python wheels packages
COPY --from=builder /app/wheels/ /wheels/

WORKDIR /app

RUN set -ex \
    && adduser -D prometheus \
    && python -m venv $APP_VENV \
    && "$APP_VENV"/bin/pip install \
        --no-cache-dir \
        --no-index \
        /wheels/* \
    && rm -rf /var/cache/apk/*

WORKDIR /app/metrics

COPY ./metrics /app/metrics/

# Switch to non-root user
USER prometheus

EXPOSE 8333

CMD ["uvicorn", "metrics.main:app", "--host", "0.0.0.0", "--port", "8333"]
