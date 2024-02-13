FROM python:3.11-alpine

LABEL maintainers="Gourish Sadhu"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app

EXPOSE 8000

ARG DEV=false

RUN python -m venv /python && \
    /python/bin/pip install --upgrade pip && \
    /python/bin/pip install -r /tmp/requirements.txt && \
    ([ $DEV == "true" ] && /python/bin/pip install -r /tmp/requirements.dev.txt) && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/python/bin:$PATH"

USER django-user