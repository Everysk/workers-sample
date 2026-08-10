#!/usr/bin/env bash

set -euo pipefail

if [[ -z ${EVERYSK_ENVIRONMENT} ]]; then
    export EVERYSK_ENVIRONMENT=local
fi

# The deploy workspace may be bind-mounted from a CI runner, so the repo can be
# owned by a different user than the container. Mark it safe so the git commands
# in the deploy (changed-folder detection) don't fail with "dubious ownership".
git config --global --add safe.directory "${PROJECT_ROOT}" 2>/dev/null || true

case $1 in
    deploy)
        python "${PROJECT_ROOT}"/run.py deploy all
        ;;
    *)
        echo "Invalid command."
        exit 1
        ;;
esac
