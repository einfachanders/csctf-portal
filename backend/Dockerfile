FROM python:3.12-slim-bookworm AS builder

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y -q && apt-get upgrade -y -q \
    && apt-get install -y -q --no-install-recommends \
    gcc \
    git \
    python3-dev \
    &&  rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /opt/csctf-portal-backend/requirements.txt
COPY ./app/ /opt/csctf-portal-backend/app/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    -r /opt/pizza/requirements.txt

FROM python:3.12-slim-bookworm AS runtime
LABEL maintainer="me@bitsheep.net"
LABEL description="csctf-portal-backend"

USER root

# Preparations and upgrading operating system
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y -q && apt-get upgrade -y -q \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --gid="10000" --system ctf \
    && adduser --uid "10000" --ingroup "ctf" --home "/home/ctf" --shell "/bin/sh" --system --disabled-password --gecos "" ctf \
    && chown -R ctf:ctf \
    /home/ctf

# Install specific operating system packages
RUN apt-get update -y -q && apt-get upgrade -y -q \
    && apt-get install -y -q --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt /opt
RUN chown -R ctf:ctf /opt/csctf-portal-backend

# Make sure we use the virtualenv:
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV SHELL=/bin/sh
ENV PYTHONUNBUFFERED=1

USER 10000

EXPOSE 8000/tcp
WORKDIR /opt/csctf-portal-backend
ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
