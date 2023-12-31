FROM python:3.11.5-slim-bookworm

# poetry version argument
ARG POETRY_VERSION=1.6.1

# env variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# system dependencies
RUN apt update \
    && apt install --no-install-recommends -y \
    git \
    build-essential \
    libpq-dev


# app setup
WORKDIR /app
COPY ./poetry.lock ./pyproject.toml ./

# project dependencies
RUN --mount=type=cache,target=/root/.cache pip install -U pip setuptools
RUN --mount=type=cache,target=/root/.cache pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false
RUN --mount=type=cache,target=/root/.cache poetry install --only main --compile --no-root --no-interaction

# cleanup
RUN apt purge -y \
    git \
    build-essential

# listen port
EXPOSE 8000

# copy main project
COPY . .

# Run project
CMD python manage.py runserver 0.0.0.0:8000