###############################################
############ VSCode DEV Environment ###########
###############################################
FROM python:3.12.9-slim

# System update.
RUN apt-get update && apt-get -y dist-upgrade && apt-get -y autoremove && apt-get -y autoclean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y git && \
    apt-get -y autoremove && \
    apt-get -y autoclean && \
    rm -rf /var/lib/apt/lists/*

# Set Workdir
WORKDIR /var/app

ENV PROJECT_ROOT='/var/app' \
    DEBIAN_FRONTEND='noninteractive' \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV PYTHON_PATH="${PROJECT_ROOT}"

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN /usr/local/bin/pip3 --no-cache-dir install -r /tmp/requirements.txt
