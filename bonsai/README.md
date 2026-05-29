# Bonsai LLM Setup (GTX 1060 6GB, Pascal CC 6.1)

LLM inference environment using PrismML-Eng/llama.cpp fork with CUDA acceleration on a GTX 1060 6GB.

## Hardware
- GPU: NVIDIA GeForce GTX 1060 6GB (Pascal, CC 6.1)
- CUDA Driver: 13.0, RAM: 15 GB

## Models Installed

| Model | Format | Size | VRAM | Speed (t/s) |
|-------|--------|------|------|-------------|
| Bonsai-4B-Q1_0 | GGUF Q1_0 (1-bit) | 545 MB | ~540 MB | 28.1 |
| Ternary-Bonsai-4B-Q2_0 | GGUF Q2_0 (2-bit ternary) | 1.07 GB | ~1 GB | 47.1 |

## Directory Structure

```
languagelearning/
├── .gitignore           # data/ excluded
└── bonsai/
    ├── config.sh        # shared config (sourced by scripts)
    ├── env.sh           # aliases for ~/.bashrc
    ├── README.md
    ├── scripts/
    │   ├── run.sh       # one-shot CLI inference
    │   ├── serve.sh     # HTTP API server
    │   └── query.sh     # query the API
    └── data/            # (git-ignored) binary + GGUF models
```

## Usage

### One-shot inference
```bash
./bonsai/scripts/run.sh                          # defaults: ternary, "Hello", 50 tokens
./bonsai/scripts/run.sh Bonsai-4B-Q1_0.gguf "What is 2+2?" 30
```

### Start API server
```bash
./bonsai/scripts/serve.sh                        # defaults: ternary, port 8080
./bonsai/scripts/serve.sh Bonsai-4B-Q1_0.gguf 8081
```

### Query the API
```bash
./bonsai/scripts/query.sh                        # defaults: localhost:8080
./bonsai/scripts/query.sh http://127.0.0.1:8081 "Explain quantum computing" 100 0.3
```

### Aliases (add to ~/.bashrc)
```bash
echo "source ~/languagelearning/bonsai/env.sh" >> ~/.bashrc
source ~/languagelearning/bonsai/env.sh

bonsai-run              # run with defaults
bonsai-q1               # run Bonsai-4B-Q1_0
bonsai-t2               # run Ternary-Bonsai-4B-Q2_0
bonsai-serve            # start server
bonsai-query            # query server
bonsai-models           # list available models
```

## How It Works

The PrismML fork's pre-built CUDA 12.4 binary works on Pascal GPUs via NVIDIA's CUDA 12.x driver. The ollama-provided `libcudart.so.12` bridges the binary (compiled against CUDA 12.4) with the system driver (CUDA 13.0).

## Known Limitations

- **Bonsai Image generation** is blocked on this GPU — PyTorch 2.12.0+cu130 lacks sm_61 CUDA kernels
- CUDA 12.4 pre-built binary may lack some Pascal-specific optimizations (falls through PTX JIT)
