# Determine repo root: .env lives at <repo_root>/bonsai/.env
BONSAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$BONSAI_DIR/.." && pwd)"

# Data paths
BIN_DIR="$BONSAI_DIR/data"
MODELS_DIR="$BONSAI_DIR/data"
CUDART_DIR="/usr/local/lib/ollama/cuda_v12"

export LD_LIBRARY_PATH="$CUDART_DIR:$BIN_DIR:$LD_LIBRARY_PATH"
