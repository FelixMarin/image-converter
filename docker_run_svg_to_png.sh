#!/usr/bin/env bash
set -euo pipefail

# Usage: ./docker_run_svg_to_png.sh [args passed to svg_to_png]
# Example: ./docker_run_svg_to_png.sh -i output/alien_sf.svg -o dtf -d 600

IMAGE=${IMAGE:-image-converter:latest}
mkdir -p input output temp

docker run --rm -it \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  -v "$(pwd)/temp":/app/temp \
  "$IMAGE" python -m svg_to_png "$@"
