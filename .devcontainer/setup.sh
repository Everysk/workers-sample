#!/usr/bin/env bash

# Host-side setup for the dev container. The "initializeCommand" in
# devcontainer.json runs this on your machine, before the container exists.
# It creates the commit signing key files when they are missing. VS Code passes
# every "mounts" entry as `docker --mount type=bind`, which refuses to start the
# container when the source path does not exist.

set -eo pipefail

# A bind mount needs an existing source, or the container does not start at all.
mkdir -p "$HOME/.ssh"
for signing_key in "$HOME/.ssh/git-signing" "$HOME/.ssh/git-signing.pub"; do
    [ -e "$signing_key" ] || touch "$signing_key"
done

if [ ! -s "$HOME/.ssh/git-signing.pub" ]; then
    echo "⚠️  No commit signing key found. Protected branches will reject your commits."
    echo "    Create one: ssh-keygen -t ed25519 -f ~/.ssh/git-signing -C \"you@everysk.com\""
    echo "    Then run:   gh auth refresh -h github.com -s admin:ssh_signing_key"
    echo "                gh ssh-key add ~/.ssh/git-signing.pub --type signing --title \"git-signing \$(hostname)\""
fi
