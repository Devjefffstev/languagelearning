#!/usr/bin/env bash
set -e

BIN_DIR="$HOME/Home/custom_models/llama.cpp/build-cuda12.4/llama-prism-b8846-d104cf1"
MODELS_DIR="$HOME/Home/custom_models/llama.cpp/models"
CUDART_DIR="/usr/local/lib/ollama/cuda_v12"

export LD_LIBRARY_PATH="$CUDART_DIR:$BIN_DIR:$LD_LIBRARY_PATH"

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
