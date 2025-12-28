#!/usr/bin/env bash
set -euo pipefail

# Usage: ./docker_run_convert.sh [args passed to convert_to_svg]
# Example: ./docker_run_convert.sh -i input/foto.png -o output/foto -b true

IMAGE=${IMAGE:-image-converter:latest}
mkdir -p input output temp

docker run --rm -it \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  -v "$(pwd)/temp":/app/temp \
  "$IMAGE" python -m convert_to_svg "$@"
