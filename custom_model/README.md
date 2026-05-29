# Gemma4 on Limited Hardware: Optimization Guide

## The Problem

You have a **GTX 1060 6GB** GPU and want to run **Gemma4** models, but they're too slow or unusable. Here's why:

- **gemma4:e4b** = 9.6GB (42 layers)
- **gemma4:26b** = 18GB (62 layers)
- Your GPU has only **6GB VRAM**

The model can't fit fully in GPU memory, so Ollama falls back to CPU for some layers, making inference extremely slow (5-20 tokens/second instead of 50+).

---

## Core Concepts

### What is a "Layer"?

Think of a neural network like an assembly line in a factory. Each worker (layer) does one step of processing and passes the result to the next worker.

- Each layer has **weights** — numbers that define how it processes data
- These weights need to be stored somewhere (GPU VRAM or system RAM)
- Gemma4:e4b has **42 layers**, Gemma4:26b has **62 layers**

### GPU Layer Offloading

Your GPU is like a **very fast but tiny warehouse** (6GB). Your system RAM is a **big but slower warehouse** (15GB).

- **Layers in GPU VRAM** = lightning fast
- **Layers in system RAM** = 5-10x slower
- **Layers on disk (swap)** = impossibly slow

By default, Ollama tries to put as many layers on GPU as possible. But with a 6GB GPU and 9.6GB+ model, the GPU fills up and Ollama scrambles to manage layers across VRAM and RAM, causing performance issues.

### What is Context Window?

The context window is the model's **working memory** — how many tokens it can "see" at once.

- 1 token ≈ 4 characters ≈ 0.75 words
- **4096 tokens** ≈ 3,000 words
- **32768 tokens** ≈ 24,000 words
- **131072 tokens** ≈ 98,000 words

Gemma4:e4b supports up to 131,072 tokens, but each token requires KV cache memory (roughly 512 bytes per token per layer).

**Memory math for context:**
```
32K tokens × 42 layers × 512 bytes ≈ 687 MB
131K tokens × 42 layers × 512 bytes ≈ 2.8 GB  (just for context!)
```

Context also competes for GPU VRAM, so a large context window + large model = GPU OOM.

### What is a Modelfile?

A **Modelfile** is Ollama's configuration file that acts like a **recipe card** for your model:

```bash
FROM gemma4:e4b           # Which model to use
PARAMETER num_ctx 16384   # Set context window
PARAMETER num_gpu 10      # How many layers on GPU
PARAMETER temperature 0.7 # How creative/precise
```

Modelfiles let you customize any model without redownloading it.

---

## The Solution

### Parameter Breakdown (Precise Mode)

| Parameter | Default | Precise | Why |
|-----------|---------|---------|-----|
| `num_ctx` | 131072 | 16384 (e4b) / 32768 (e2b/qwen3.5) | Keeps context in RAM, not GPU VRAM |
| `num_gpu` | 42 (all) | 10 (e4b) / 20 (e2b) / 0 (qwen3.5) | Limits GPU layers to what fits in VRAM |
| `num_predict` | -1 (unlimited) | 2048 (gemma4) / 4096 (qwen3.5) | Prevents runaway memory usage |
| `temperature` | 0.8 | **0.1** | Lower = more precise, deterministic answers |
| `top_p` | 0.9 | **0.5** | Lower = focus on most likely tokens |
| `repeat_penalty` | 1.1 | **1.2-1.3** | Higher = less repetition |
| `seed` | 0 (random) | **42** | Fixed seed for reproducible output |

**Precision tuning:** Lower temperature (0.1), lower top_p (0.5), and higher repeat_penalty produce more factual, less creative responses.

### Flash Attention

Flash Attention is a memory optimization that reduces KV cache by ~50%. Enable it by running the setup script or setting environment variables:

```bash
# Option 1: Run the setup helper (sets env vars for current session)
bash ~/custom_model/setup-ollama-env.sh

# Option 2: Add to /etc/environment (requires sudo)
sudo bash -c 'echo "OLLAMA_FLASH_ATTENTION=1" >> /etc/environment'

# Option 3: Restart Ollama service with env var
sudo systemctl set-environment OLLAMA_FLASH_ATTENTION=1
sudo systemctl restart ollama
```

### Recommended Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `OLLAMA_FLASH_ATTENTION` | 1 | Reduces KV cache memory by ~50% |
| `OLLAMA_NUM_PARALLEL` | 1 | Prevents memory issues with concurrent requests |
| `OLLAMA_CONTEXT_LENGTH` | 16384 | Default context window (adjust per model) |

---

## Usage with OpenCode

OpenCode connects to Ollama as a local provider. Here's how to run it:

### Quick Start (Recommended)

```bash
OLLAMA_CONTEXT_LENGTH=32768 opencode --model ollama/qwen3.5:4b
```

This sets context to 32K and loads qwen3.5:4b model.

### Available Models

```bash
# Qwen 3.5 4B (fastest, 100% GPU)
OLLAMA_CONTEXT_LENGTH=32768 opencode --model ollama/qwen3.5:4b

# Qwen 3.5 4B Optimized (precise mode, 32K context)
ollama run custom_model/qwen3.5-4b-optimized

# Gemma 4 E4B (higher quality, slower)
OLLAMA_CONTEXT_LENGTH=16384 opencode --model ollama/gemma4:e4b

# Gemma 4 E2B (balanced)
OLLAMA_CONTEXT_LENGTH=32768 opencode --model ollama/gemma4:e2b
```

### Model Selection in OpenCode

Type `/models` in OpenCode to see all available models, then select one.

### Direct API Call

```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "qwen3.5:4b",
  "prompt": "Your question",
  "options": {
    "num_ctx": 32768,
    "temperature": 0.1
  }
}'
```

### Method 3: Create Custom Models (Modelfile)

This creates persistent named model configurations:

```bash
ollama create gemma4:e4b-opt -f ~/custom_model/gemma4-e4b-optimized
ollama create gemma4:e2b-opt -f ~/custom_model/gemma4-e2b-optimized
ollama create custom_model/qwen3.5-4b-optimized -f ~/custom_model/qwen3.5-4b-optimized
```

Then run with:
```bash
ollama run gemma4:e4b-opt "Your question here"
ollama run gemma4:e2b-opt "Your question here"
ollama run custom_model/qwen3.5-4b-optimized "Your question here"
```

**Note:** If `ollama create` fails with permission error, use Method 1 or 2 instead.

### Run Performance Test

```bash
bash ~/custom_model/test_performance.sh
```

---

## Alternative Models

If Gemma4 is still too slow, these models are better fits for 6GB GPUs:

| Model | Size | Best For |
|-------|------|----------|
| `qwen3.5:4b` | 3.4GB | Coding, fast responses |
| `granite4` | 2.1GB | General purpose, very fast |
| `llama3.2:1b` | 1.3GB | Lightweight tasks |
| `mistral` | 4.4GB | Balanced performance |

Example usage:
```bash
ollama run qwen3.5:4b "Explain recursion"
```

---

## Troubleshooting

### Problem: Out of Memory (OOM) Error

**Symptoms:** Ollama crashes or won't start model

**Solutions:**
1. Reduce `num_ctx` by half (e.g., 16384 → 8192)
2. Reduce `num_gpu` by 2-3 layers
3. Close other GPU applications

### Problem: Very Slow Response (1-5 tokens/sec)

**Symptoms:** Model is technically running but practically unusable

**Diagnosis:**
```bash
# Check what's loaded and where
ollama ps

# Check GPU usage
nvidia-smi
```

**Solutions:**
1. Verify optimized parameters are used
2. Reduce `num_gpu` to force more layers to RAM (but slower)
3. **Recommended:** Use `gemma4:e2b` — smaller model fits more layers on GPU

### Problem: Garbled or Repeated Output

**Symptoms:** Model repeats same words, produces nonsense

**Solutions:**
1. Lower `temperature` to 0.5 (less creative, more coherent)
2. Increase `repeat_penalty` to 1.2
3. Set `seed` to a fixed number for reproducible output

### Problem: Model Still Doesn't Work

**Solutions:**
1. Restart Ollama: `sudo systemctl restart ollama`
2. Check logs: `journalctl -u ollama -n 50`
3. Try the smallest variant: `ollama run gemma4:e2b` (no custom config needed)

### Problem: "ollama create" Fails with Permission Error

**Symptoms:** Error: `500 Internal Server Error: chtimes ... operation not permitted`

**Cause:** Blob files have incorrect ownership (owned by root/ollama instead of home user)

**Solutions:**
1. **Quick fix:** Use Method 1 or 2 instead of creating custom models
2. **Permanent fix:** `sudo chown -R $(whoami):$(whoami) ~/.ollama/models/blobs/`

---

## Using with OpenCode

OpenCode can use local Ollama models instead of cloud providers. Here's how to configure it:

### Method 1: Using the Helper Script (Recommended)

The script sets `OLLAMA_CONTEXT_LENGTH=32768` before launching OpenCode:

```bash
# Default (qwen3.5:4b with 32K context)
bash ~/custom_model/opencode.sh

# With gemma4:e4b
bash ~/custom_model/opencode.sh gemma4:e4b

# With gemma4:e2b
bash ~/custom_model/opencode.sh gemma4:e2b
```

**Why use this script?** OpenCode doesn't pass `num_ctx` to Ollama by default. The model's default context is only 4096 tokens, which is too small for coding tasks. The script sets `OLLAMA_CONTEXT_LENGTH=32768` so all Ollama models use 32K context.

### Method 2: Manual Configuration

Your `~/.config/opencode/opencode.jsonc` is already configured:

```json
{
  "model": "openai/qwen3.5:4b",
  "provider": {
    "openai": {
      "baseUrl": "http://localhost:11434/v1",
      "models": {
        "qwen3.5:4b": {
          "options": {
            "num_ctx": 32768,
            "temperature": 0.1,
            "top_p": 0.5
          }
        }
      }
    }
  }
}
```

Then run:
```bash
OLLAMA_CONTEXT_LENGTH=32768 opencode --model openai/qwen3.5:4b
```

### Verify Connection

```bash
opencode models openai 2>&1 | grep -E "qwen|gemma"
```

You should see: `openai/qwen3.5:4b`

### Important Notes for OpenCode + Gemma4

1. **Context Window**: OpenCode needs at least 64k context for complex tasks. With limited VRAM, use 16k-32k:
   ```bash
   # Set via environment before running opencode
   export OLLAMA_NUM_CTX=32768
   ```

2. **Performance**: Expect slower responses than cloud models due to CPU layer offloading. For best experience, use `gemma4:e2b` (smaller, faster).

3. **Thinking Mode**: Gemma4 supports thinking. OpenCode may try to use extended thinking which requires more memory. Disable if OOM errors occur.

4. **Alternative for OpenCode**: Use `qwen3.5:4b` instead of Gemma4 (see section below).

---

## Using Qwen 3.5 4B with OpenCode (Recommended)

Qwen3.5:4B is smaller (3.4GB) and **fully fits on your GPU** (100% GPU vs 89% CPU for Gemma4). Better choice for OpenCode on limited hardware.

### Why Qwen over Gemma4?

| Model | Size | GPU Usage | Speed | Context |
|-------|------|----------|-------|---------|
| `qwen3.5:4b` | 3.4GB | 100% GPU | Fast | 32K |
| `gemma4:e4b` | 9.6GB | 11% GPU | Slow | 16K |

### Configuration for OpenCode

Your `~/.config/opencode/opencode.jsonc` is already configured to use qwen3.5:4b:

```json
{
  "model": "openai/qwen3.5:4b",
  "provider": {
    "openai": {
      "baseUrl": "http://localhost:11434/v1",
      "models": {
        "qwen3.5:4b": {
          "options": {
            "num_ctx": 32768,
            "num_gpu": 0,
            "temperature": 0.1,
            "top_p": 0.5,
            "repeat_penalty": 1.2
          }
        }
      }
    }
  }
}
```

### Test Qwen Performance

```bash
# Quick API test
curl -s http://localhost:11434/api/generate -d '{
  "model": "qwen3.5:4b",
  "prompt": "Write a hello world in Python",
  "options": {"num_ctx": 32768}
}'

# Run via helper script
bash ~/custom_model/opencode.sh
```

### Benefits for OpenCode

1. **100% GPU** — All inference on GPU, no CPU bottleneck
2. **32K context** — Good for code analysis and multi-file tasks
3. **Supports thinking** — Qwen3.5 has thinking mode for complex reasoning
4. **Faster tokens** — ~30-50 tokens/sec vs ~15 tokens/sec for Gemma4

### Switch Between Models

To use qwen3.5:4b:
```bash
opencode
```

To temporarily use gemma4:e4b, change config:
```bash
# Edit ~/.config/opencode/opencode.jsonc
# Change "model": "openai/qwen3.5:4b" to "model": "openai/gemma4:e4b"
```

---

## Quick Reference

```bash
# List all available models
ollama list

# Show model details
ollama show qwen3.5:4b

# Check currently loaded models
ollama ps

# Force CPU-only mode (slow but always works)
OLLAMA_GPU_LAYERS=0 ollama run gemma4:e4b

# Quick test with API parameters
curl -s http://localhost:11434/api/generate -d '{"model":"gemma4:e4b","prompt":"Hi","options":{"num_ctx":16384,"num_gpu":10}}'

# Launch OpenCode with Ollama
ollama launch opencode
```

---

## Understanding Ollama Status

Check with `ollama ps`:

```
NAME          ID              SIZE     PROCESSOR          CONTEXT    UNTIL
gemma4:e4b    xxx             11 GB    89%/11% CPU/GPU    16384      24 hours from now
```

Higher CPU % = slower inference. With GTX 1060 6GB, expect 80-90% CPU for Gemma4.

---

## Further Optimization (If You Upgrade GPU Later)

When you have a larger GPU (12GB+), you can increase parameters:

```bash
FROM gemma4:e4b
PARAMETER num_ctx 65536    # Up from 16384
PARAMETER num_gpu 42      # All layers on GPU
PARAMETER num_predict 4096
PARAMETER temperature 0.7
```

Flash Attention (`OLLAMA_FLASH_ATTENTION=1`) becomes especially valuable with larger context windows.

---

## Benchmark Results

All tests on **GTX 1060 6GB** with `num_batch 512`, `num_thread 8`, `temp 0.1`, `top_p 0.5`, `repeat_penalty 1.2`, `seed 42`.

### 32K Context

| Model | Size | GPU Layers | Speed |
|-------|------|-----------|-------|
| `g41:3b-32k` | 3.4B | 41/41 | **43.8 tok/s** |
| `q35:2b-32k` | 2.3B | 25/25 | **52.5 tok/s** |
| `g40:tiny-32k` | 6.7B (MoE) | 41/41 | **54.1 tok/s** |
| `tg:4b-32k` | 4.3B | 35/35 | **35.6 tok/s** |
| `g4:e2b-32k` | 5.1B | 19/26 | **21.8 tok/s** |
| `q35:4b-32k` | 4.7B | 32/36 | **17.0 tok/s** |

### 64K Context

| Model | Size | GPU Layers | Speed |
|-------|------|-----------|-------|
| `g41:3b-64k` | 3.4B | 31/41 | **13.9 tok/s** |
| `q35:2b-64k` | 2.3B | 25/25 | **52.5 tok/s** |
| `g40:tiny-64k` | 6.7B (MoE) | 41/41 | **54.2 tok/s** |
| `tg:4b-64k` | 4.3B | 35/35 | **35.6 tok/s** |
| `g4:e2b-64k` | 5.1B | 17/26 | **16.9 tok/s** |
| `q35:4b-64k` | 4.7B | 26/36 | **7.5 tok/s** |

### Max Context

| Model | Context | GPU Layers | Speed | Status |
|-------|---------|-----------|-------|--------|
| `g40:tiny-128k` | 128K | 41/41 | **54.5 tok/s** | Full GPU |
| `q35:2b-262k` | 262K | 9/25 | **8.1 tok/s** | Mostly CPU |
| `g4:e2b-131k` | 131K | 3/26 | **6.8 tok/s** | Mostly CPU |
| `g41:3b-131k` | 131K | 4/41 | **7.6 tok/s** | Mostly CPU |
| `q35:4b-262k` | 262K | — | — | OOM crash |
| `g4:e4b-131k` | 131K | — | — | OOM crash |
| `tg:4b-131k` | 131K | — | — | OOM crash |
| `g40:tiny-256k` | 256K | — | — | OOM crash |

### Key Findings

- **Fastest overall:** `g40:tiny` — full GPU at 32K, 64K, and 128K (MoE sparsity keeps VRAM low)
- **Best for max context on 6GB:** `q35:2b-262k` (2.3B model fits 9 GPU layers at 262K)
- **Long-context verified:** `g40:tiny-128k` correctly recalled embedded secrets from 20K-token prompt
- **OOM limits:** models >4.7B crash at max context (131K+) due to KV cache exceeding 6GB VRAM + 11GB available RAM