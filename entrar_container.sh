#!/bin/bash

docker run --rm -it \
  -v "$PWD":/workspace \
  -w /workspace \
  --entrypoint bash \
  agente-devops-python

