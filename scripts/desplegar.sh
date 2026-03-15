#!/usr/bin/env bash
set -e

if [ ! -f .env ]; then
  echo "Falta el archivo .env"
  exit 1
fi

docker compose up --build
