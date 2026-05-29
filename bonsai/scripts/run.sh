#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config.sh"

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
