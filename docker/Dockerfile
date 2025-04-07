############ Base image ############
FROM everyskpackages/everysk_worker_development:latest AS everysk_worker_base

WORKDIR ${PROJECT_ROOT}

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN /usr/local/bin/pip3 --no-cache-dir install -r /tmp/requirements.txt

FROM everysk_worker_base AS everysk_worker_remote

COPY . ${PROJECT_ROOT}

ENTRYPOINT [ "/bin/bash", "--login", "-c", "${PROJECT_ROOT}/run.sh deploy all" ]

FROM everysk_worker_base AS everysk_worker_tests

ENTRYPOINT [ "/bin/bash", "--login", "-c", "${PROJECT_ROOT}/run.sh tests" ]
