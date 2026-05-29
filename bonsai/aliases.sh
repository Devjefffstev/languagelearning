# Source this file in ~/.bashrc to use the aliases:
#   echo "source ~/Home/languagelearning/custom_model/aliases.sh" >> ~/.bashrc

export CUSTOM_MODEL_DIR="$HOME/Home/languagelearning/custom_model"
export LLAMA_BIN="$HOME/Home/custom_models/llama.cpp/build-cuda12.4/llama-prism-b8846-d104cf1"
export LLAMA_MODELS="$HOME/Home/custom_models/llama.cpp/models"
export LD_LIBRARY_PATH="/usr/local/lib/ollama/cuda_v12:$LLAMA_BIN:$LD_LIBRARY_PATH"

alias bonsai='$CUSTOM_MODEL_DIR/run-bonsai.sh'
alias bonsai-server='$CUSTOM_MODEL_DIR/serve-bonsai.sh'
alias bonsai-q='$CUSTOM_MODEL_DIR/query-bonsai.sh'

# Quick completions
alias bonsai-q1='bonsai Bonsai-4B-Q1_0.gguf'
alias bonsai-t2='bonsai Ternary-Bonsai-4B-Q2_0.gguf'

# List available models
alias bonsai-models='ls -lh $LLAMA_MODELS/*.gguf'

echo "Bonsai aliases loaded. Available: bonsai, bonsai-server, bonsai-q, bonsai-q1, bonsai-t2, bonsai-models"
