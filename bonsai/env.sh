# Source this in ~/.bashrc:
#   echo "source ~/languagelearning/bonsai/env.sh" >> ~/.bashrc

BONSAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$BONSAI_DIR/config.sh"

alias bonsai-run='$BONSAI_DIR/scripts/run.sh'
alias bonsai-serve='$BONSAI_DIR/scripts/serve.sh'
alias bonsai-query='$BONSAI_DIR/scripts/query.sh'

alias bonsai-q1='bonsai-run Bonsai-4B-Q1_0.gguf'
alias bonsai-t2='bonsai-run Ternary-Bonsai-4B-Q2_0.gguf'
alias bonsai-models='ls -lh $MODELS_DIR/*.gguf'

echo "Bonsai aliases loaded. Commands: bonsai-run, bonsai-serve, bonsai-query, bonsai-q1, bonsai-t2, bonsai-models"
