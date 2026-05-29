# llama.cpp + Qwen3.6-27B-MTP Setup on macOS

> Local LLM server with speculative decoding (MTP + ngram) for Qwen3.6-27B-MTP on Apple Silicon Mac.
> Supports both Q8_0 (max quality, ~30 GB) and Q4_K_M (balanced, ~16.5 GB) variants.
> Last updated: May 2026

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Build llama.cpp](#2-build-llamacpp)
3. [Install HuggingFace CLI](#3-install-huggingface-cli)
4. [Download Models](#4-download-models)
5. [Create `models.ini`](#5-create-modelsin)
6. [Run llama-server](#6-run-llama-server)
7. [Test the API](#7-test-the-api)
8. [Quick Reference](#8-quick-reference)

---

## 1. Prerequisites

- macOS (Apple Silicon)
- Homebrew
- HuggingFace account + access token
- ~35 GB free disk space (for both model variants)

Install build tools:

```bash
brew install make cmake
```

---

## 2. Build llama.cpp

```bash
# Clone
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Configure build
cmake -B build

# Build with all CPU cores
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

The server binary will be at `./build/bin/llama-server`.

---

## 3. Install HuggingFace CLI

```bash
brew install hf

# Authenticate (opens browser or prompts for token)
hf auth login
```

> Get your token at: https://huggingface.co/settings/tokens

---

## 4. Download Models

Create the models directory:

```bash
mkdir -p ~/llama.cpp/models
cd ~/llama.cpp/models
```

### Option A: Q8_0 (Maximum Quality, ~30 GB)

```bash
hf download Radamanthys11/Qwen3.6-27B-MTP-Q8_0-GGUF   Qwen3.6-27B-MTP-Q8_0.gguf   --local-dir .
```

### Option B: Q4_K_M (Faster & Lighter, ~16.5 GB)

```bash
hf download RDson/Qwen3.6-27B-MTP-Q4_K_M-GGUF   Qwen3.6-27B-MTP-Q4_K_M.gguf   --local-dir .
```

### Download Both (Recommended)

```bash
# Q8_0
hf download Radamanthys11/Qwen3.6-27B-MTP-Q8_0-GGUF   Qwen3.6-27B-MTP-Q8_0.gguf   --local-dir .

# Q4_K_M
hf download RDson/Qwen3.6-27B-MTP-Q4_K_M-GGUF   Qwen3.6-27B-MTP-Q4_K_M.gguf   --local-dir .
```

---

## 5. Create `models.ini`

Create the preset configuration file:

```bash
micro ~/llama.cpp/models/models.ini
```

Paste the following:

```ini
version = 1

[*]
threads = 12
ctx-size = 8192
n = -1
flash-attn = on
no-mmap = true

[Qwen3.6-27B-MTP-Q8_0]
ctx-size = 16384
n-gpu-layers = 999
temperature = 0.6
top-p = 0.95
top-k = 20
min-p = 0.0
repeat-penalty = 1.0
cache-type-k = q8_0
cache-type-v = q8_0
batch-size = 2048
ubatch-size = 512
spec-type = ngram-mod,draft-mtp
spec-draft-n-max = 2
spec-ngram-mod-n-match = 24
spec-ngram-mod-n-min = 48
spec-ngram-mod-n-max = 64

[Qwen3.6-27B-MTP-Q4_K_M]
ctx-size = 16384
n-gpu-layers = 999
temperature = 0.6
top-p = 0.95
top-k = 20
min-p = 0.0
repeat-penalty = 1.0
cache-type-k = q4_0
cache-type-v = q4_0
batch-size = 2048
ubatch-size = 512
spec-type = ngram-mod,draft-mtp
spec-draft-n-max = 2
spec-ngram-mod-n-match = 24
spec-ngram-mod-n-min = 48
spec-ngram-mod-n-max = 64
```

---

## 6. Run llama-server

### 6.1 Q8_0 — Maximum Quality (MTP + ngram, ~30 GB VRAM/RAM)

```bash
cd ~/llama.cpp

./build/bin/llama-server   --host 0.0.0.0   --port 9000   --threads 12   --models-dir ~/llama.cpp/models/   --models-autoload   --models-max 1   --models-preset ~/llama.cpp/models/models.ini   -m ~/llama.cpp/models/Qwen3.6-27B-MTP-Q8_0.gguf
```

### 6.2 Q4_K_M — Balanced Speed/Quality (MTP + ngram, ~16.5 GB)

```bash
cd ~/llama.cpp

./build/bin/llama-server   --host 0.0.0.0   --port 9000   --threads 12   --models-dir ~/llama.cpp/models/   --models-autoload   --models-max 1   --models-preset ~/llama.cpp/models/models.ini   -m ~/llama.cpp/models/Qwen3.6-27B-MTP-Q4_K_M.gguf
```

### 6.3 Legacy: MTP Only (Q4_K_M, ~16.5 GB)

```bash
./build/bin/llama-server   -m ~/llama.cpp/models/Qwen3.6-27B-MTP-Q4_K_M.gguf   -ngl 999   -c 4096   --spec-type draft-mtp   --spec-draft-n-max 2   --port 9000
```

### 6.4 Legacy: MTP Only (Q8_0, ~30 GB)

```bash
./build/bin/llama-server   -m ~/llama.cpp/models/Qwen3.6-27B-MTP-Q8_0.gguf   -ngl 999   -c 16384   --flash-attn on   --spec-type draft-mtp   --spec-draft-n-max 2   --host 0.0.0.0   --port 9000
```

### 6.5 Legacy: MTP + ngram (Q4_K_M, ~16.5 GB)

```bash
./build/bin/llama-server   -m ~/llama.cpp/models/Qwen3.6-27B-MTP-Q4_K_M.gguf   -ngl 999   -c 16384   --flash-attn on   --spec-type ngram-mod,draft-mtp   --spec-draft-n-max 2   --spec-ngram-mod-n-match 24   --spec-ngram-mod-n-min 48   --spec-ngram-mod-n-max 64   --host 0.0.0.0   --port 9000
```

### 6.6 Legacy: MTP + ngram (Q8_0, ~30 GB)

```bash
./build/bin/llama-server   -m ~/llama.cpp/models/Qwen3.6-27B-MTP-Q8_0.gguf   -ngl 999   -c 16384   --flash-attn on   --spec-type ngram-mod,draft-mtp   --spec-draft-n-max 2   --spec-ngram-mod-n-match 24   --spec-ngram-mod-n-min 48   --spec-ngram-mod-n-max 64   --host 0.0.0.0   --port 9000
```

---

## 7. Test the API

Once the server is running, test with curl:

```bash
curl http://localhost:9000/v1/chat/completions   -H "Content-Type: application/json"   -d '{"model":"qwen3","messages":[{"role":"user","content":"Hello"}]}'
```

Or open the built-in web UI at: `http://localhost:9000`

---

## 8. Quick Reference

### Model Sizes

| Variant | Size | Quality | Best For |
|---------|------|---------|----------|
| Q8_0 | ~30 GB | Maximum | High-quality reasoning, coding |
| Q4_K_M | ~16.5 GB | Balanced | Faster inference, lower memory |

### Speculative Decoding Modes

| Mode | Flags | Speedup | Use Case |
|------|-------|---------|----------|
| MTP only | `--spec-type draft-mtp` | Moderate | Baseline speculative decoding |
| MTP + ngram | `--spec-type ngram-mod,draft-mtp` | Higher | Best speed with local context repetition |

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `-ngl 999` | Offload all layers to GPU (Metal on Mac) |
| `-c 16384` | Context size (16K tokens) |
| `--flash-attn on` | Enable Flash Attention for faster inference |
| `--spec-type ngram-mod,draft-mtp` | Enable both ngram and MTP speculative decoding |
| `--spec-draft-n-max 2` | Draft up to 2 tokens per step |
| `--host 0.0.0.0` | Bind to all interfaces (accessible from network) |
| `--port 9000` | Server port |

### Directory Structure

```
~/llama.cpp/
├── build/
│   └── bin/
│       └── llama-server
├── models/
│   ├── models.ini
│   ├── Qwen3.6-27B-MTP-Q8_0.gguf
│   └── Qwen3.6-27B-MTP-Q4_K_M.gguf
└── llama.cpp/          # source repo
```

---

## Notes

- **Apple Silicon**: `-ngl 999` pushes all layers to Metal GPU. On Mac Studio / Mac Mini with high unified memory, this runs entirely on GPU.
- **Memory pressure**: Q8_0 needs ~30 GB free unified memory. Q4_K_M needs ~16.5 GB. Close other apps before loading.
- **MTP (Multi-Token Prediction)**: Qwen3.6-27B-MTP includes built-in draft heads for speculative decoding — no separate draft model needed.
- **ngram**: Adds local n-gram-based speculation on top of MTP for additional speedup on repetitive patterns.
- **Recommended**: Use the `models.ini` + `--models-preset` approach (sections 6.1 and 6.2) for cleaner management.
