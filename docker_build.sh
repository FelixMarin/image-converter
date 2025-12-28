#!/usr/bin/env bash
set -euo pipefail

# Build helper for the docker image
IMAGE=${IMAGE:-image-converter:latest}
docker build -t "$IMAGE" .
