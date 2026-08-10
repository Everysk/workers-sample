############ Base image ############
FROM python:3.12.13-slim AS everysk_worker_base

ENV PROJECT_ROOT=/var/app

WORKDIR ${PROJECT_ROOT}

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN /usr/local/bin/pip3 --no-cache-dir install -r /tmp/requirements.txt

FROM everysk_worker_base AS everysk_worker_remote

COPY . ${PROJECT_ROOT}

ENTRYPOINT [ "/bin/bash", "--login", "-c", "python ${PROJECT_ROOT}/run.py deploy all" ]

FROM everysk_worker_base AS everysk_worker_tests

ENTRYPOINT [ "/bin/bash", "--login", "-c", "python ${PROJECT_ROOT}/run.py tests" ]
