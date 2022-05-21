#!/bin/bash

# Add these for easier development
#  -v $(dirname ${CURRENT_DIR}):/home/user/signalblast/ \
#  --interactive=true \
#  --tty=true \
#  --entrypoint bash \

SIGNALBLAST_BASE="${SIGNALBLAST_BASE:-$(pwd)}"

CURRENT_DIR=$(dirname $(realpath $0))
docker container run \
  -v "${SIGNALBLAST_BASE}/data/signalblast:/home/user/signalblast/signalblast/data" \
  -v "${SIGNALBLAST_BASE}/data/signald:/home/user/.config/signald" \
  eraxama/signalblast:latest
