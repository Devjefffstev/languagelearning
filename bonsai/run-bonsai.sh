#!/usr/bin/env bash
set -e

BIN_DIR="$HOME/Home/custom_models/llama.cpp/build-cuda12.4/llama-prism-b8846-d104cf1"
MODELS_DIR="$HOME/Home/custom_models/llama.cpp/models"
CUDART_DIR="/usr/local/lib/ollama/cuda_v12"

export LD_LIBRARY_PATH="$CUDART_DIR:$BIN_DIR:$LD_LIBRARY_PATH"

model="${1:-Ternary-Bonsai-4B-Q2_0.gguf}"
prompt="${2:-Hello}"
tokens="${3:-50}"

if [ ! -f "$MODELS_DIR/$model" ]; then
  echo "Model not found: $MODELS_DIR/$model"
  echo "Available models:"
  ls "$MODELS_DIR"/*.gguf 2>/dev/null | xargs -n1 basename
  exit 1
fi

echo "Model: $model ($(du -h "$MODELS_DIR/$model" | cut -f1))"
echo "---"

exec "$BIN_DIR/llama-cli" \
  -m "$MODELS_DIR/$model" \
  -ngl 99 \
  --temp 0.7 \
  -n "$tokens" \
  -p "$prompt"
