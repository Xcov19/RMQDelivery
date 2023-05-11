# Starts core package
FROM python:3.10.2
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install -y --no-install-recommends libsqlite3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -U pip && python3 -m pip install --no-cache-dir poetry

WORKDIR /app

COPY core /app/core
COPY infrastructure /app/infrastructure
COPY utils /app/utils

COPY *.toml /app/
COPY poetry.lock /app

ENV PYTHONPATH /app
RUN poetry install -vvv
