# FROM continuumio/miniconda3 AS builder

# COPY  conda.yaml .
# RUN conda env create --file conda.yaml

# RUN conda install -c conda-forge conda-pack

# RUN /bin/bash -c "conda-pack -n dev.mnist.env -o /tmp/env.tar && mkdir venv && cd venv && tar xf /tmp/env.tar && rm /tmp/env.tar"

# RUN venv/bin/conda-unpack
FROM python:3.9-alpine AS compile-image

RUN apk add --no-cache py-pip openssl ca-certificates python3-dev build-base wget

WORKDIR "$APP_HOME"/app

COPY requirements.txt .
RUN python3 -m venv .
RUN ./bin/pip install -r requirements.txt

FROM python:3.9-alpine AS runtime-image

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 APP_USER=app APP_HOME=/home/app

RUN apk update && \
    apk add --no-cache py-pip openssl ca-certificates python3-dev build-base wget \
    && rm -rf /var/lib/apt/lists/*

RUN adduser -D -g '' -s /bin/sh "$APP_USER"

# COPY --from=builder --chown="$APP_USER":"$APP_USER" venv "$APP_HOME"/dev.mnist.env
COPY --chown="$APP_USER":"$APP_USER" ./ "$APP_HOME"/app
WORKDIR "$APP_HOME"/app

COPY --from=compile-image "$APP_HOME"/app ./
USER "$APP_USER"


# ENV PATH="$APP_HOME/dev.mnist.env/bin:$PATH"

CMD uvicorn api.predict:app --reload --workers 1 --host 0.0.0.0 --port 3000