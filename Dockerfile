FROM python:3.10-slim as python-base

# Env variables
ENV ENV=staging \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.12 \
    PORT=8001

FROM python-base as builder-base
# Install gcc compiler since poetry depends on gcc
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential


WORKDIR /app
COPY . /app/


# Install deps
RUN pip install -r /app/requirements.txt

FROM python-base as runtime
COPY --from=builder-base /usr/local/bin /usr/local/bin
COPY --from=builder-base /usr/local/lib/python3.10/ /usr/local/lib/python3.10/
COPY --from=builder-base /app/ /app/

WORKDIR /app
COPY . /app

# This app run in port 8001
EXPOSE 8001

# Entry point to our app
ENTRYPOINT /usr/local/bin/uvicorn main:app --host 0.0.0.0 --port $PORT