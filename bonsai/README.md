# Custom LLM Setup (GTX 1060 6GB, Pascal CC 6.1)

## Overview

LLM inference environment using PrismML-Eng/llama.cpp fork with CUDA acceleration on a GTX 1060 6GB.

### Hardware
- GPU: NVIDIA GeForce GTX 1060 6GB (Pascal, CC 6.1)
- CUDA Driver: 13.0, RAM: 15 GB

### Models Installed

| Model | Format | Size | VRAM | Speed (t/s) |
|-------|--------|------|------|-------------|
| Bonsai-4B-Q1_0 | GGUF Q1_0 (1-bit) | 545 MB | ~540 MB | 28.1 |
| Ternary-Bonsai-4B-Q2_0 | GGUF Q2_0 (2-bit ternary) | 1.07 GB | ~1 GB | 47.1 |

### How It Works

The PrismML fork's pre-built CUDA 12.4 binary works on Pascal GPUs via NVIDIA's CUDA 12.x driver. The ollama-provided `libcudart.so.12` bridges the binary (compiled against CUDA 12.4) with the system driver (CUDA 13.0).

## File Locations

- **llama.cpp binary**: `~/Home/custom_models/llama.cpp/build-cuda12.4/llama-prism-b8846-d104cf1/`
- **GGUF models**: `~/Home/custom_models/llama.cpp/models/`
- **CPU-only build**: `~/Home/custom_models/llama.cpp/build/`

## Scripts

| Script | Purpose |
|--------|---------|
| `run-bonsai.sh [model] [prompt] [tokens]` | Run one-shot inference |
| `serve-bonsai.sh [model] [port] [host]` | Start HTTP API server |
| `query-bonsai.sh [url] [prompt] [tokens] [temp]` | Query the API server |
| `aliases.sh` | Source this for convenient aliases |

### Aliases (from aliases.sh)

```bash
source ~/Home/languagelearning/custom_model/aliases.sh

bonsai                    # run-bonsai.sh with defaults
bonsai-q1                 # run with Bonsai-4B-Q1_0.gguf
bonsai-t2                 # run with Ternary-Bonsai-4B-Q2_0.gguf
bonsai-server             # start API server
bonsai-q                  # query API server
bonsai-models             # list available models
```

Add `source ~/Home/languagelearning/custom_model/aliases.sh` to your `~/.bashrc`.

### Usage Examples

```bash
# Run one-shot
./run-bonsai.sh Ternary-Bonsai-4B-Q2_0.gguf "What is 2+2?" 30

# Start server on port 8080
./serve-bonsai.sh Bonsai-4B-Q1_0.gguf 8080

# Query server (in another terminal)
./query-bonsai.sh http://127.0.0.1:8080 "Explain quantum computing" 100 0.3
```

## Setup Process

### 1. Clone PrismML llama.cpp fork
```bash
git clone https://github.com/PrismML-Eng/llama.cpp.git \
  ~/Home/custom_models/llama.cpp
```

### 2. Download pre-built CUDA 12.4 binary
```bash
cd ~/Home/custom_models/llama.cpp
mkdir -p build-cuda12.4
wget https://github.com/PrismML-Eng/llama.cpp/releases/download/prism-b8846-d104cf1/llama-prism-b8846-d104cf1-bin-linux-cuda-12.4-x64.tar.gz -O /tmp/llama-cuda12.4.tar.gz
tar xzf /tmp/llama-cuda12.4.tar.gz -C build-cuda12.4/
```

### 3. Download models
```bash
wget https://huggingface.co/prism-ml/Bonsai-4B-gguf/resolve/main/Bonsai-4B-Q1_0.gguf \
  -O ~/Home/custom_models/llama.cpp/models/Bonsai-4B-Q1_0.gguf
wget https://huggingface.co/prism-ml/Ternary-Bonsai-4B-gguf/resolve/main/Ternary-Bonsai-4B-Q2_0.gguf \
  -O ~/Home/custom_models/llama.cpp/models/Ternary-Bonsai-4B-Q2_0.gguf
```

The binary needs `libcudart.so.12` — use ollama's copy:
```
export LD_LIBRARY_PATH="/usr/local/lib/ollama/cuda_v12:$HOME/Home/custom_models/llama.cpp/build-cuda12.4/llama-prism-b8846-d104cf1:$LD_LIBRARY_PATH"
```

## Known Limitations

- **Bonsai Image generation** is blocked on this GPU — PyTorch 2.12.0+cu130 lacks sm_61 CUDA kernels, and conda CUDA 11.8 nvcc conflicts with conda GCC 15 headers
- CUDA 12.4 pre-built binary may lack some Pascal-specific optimizations (falls through PTX JIT)
