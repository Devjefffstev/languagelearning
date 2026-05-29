#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config.sh"

model="${1:-Ternary-Bonsai-4B-Q2_0.gguf}"
port="${2:-8080}"
host="${3:-127.0.0.1}"

if [ ! -f "$MODELS_DIR/$model" ]; then
  echo "Model not found: $MODELS_DIR/$model"
  echo "Available models:"
  ls "$MODELS_DIR"/*.gguf 2>/dev/null | xargs -n1 basename
  exit 1
fi

echo "Starting server on $host:$port with model $model..."
exec "$BIN_DIR/llama-server" \
  -m "$MODELS_DIR/$model" \
  -ngl 99 \
  --port "$port" \
  --host "$host"
