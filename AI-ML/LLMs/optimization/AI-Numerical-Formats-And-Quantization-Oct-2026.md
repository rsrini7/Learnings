# AI Numerical Formats and Quantization: From FP32 and BF16 to INT4 and NVFP4

**Daily learning · 22 October 2026 · Formats, scaling schemes and hardware support checked against primary sources on 22 October 2026**

> **Core idea:** An AI model is made of numbers, and those numbers can be stored and calculated in different ways. Fewer bits can reduce memory and data movement, but useful speed and preserved quality depend on the quantization method, the runtime and the hardware together.

## 1. Four separate questions hide behind one label

A download labelled “BF16”, “AWQ” or “GGUF” answers four different questions.

| Layer | Question it answers | Examples |
|---|---|---|
| Numerical representation | How does a bit pattern represent a number? | FP32, BF16, E4M3 FP8, INT4, NF4 |
| Quantization scheme and method | How are original values approximated, grouped and scaled? | Affine group quantization, GPTQ, AWQ, microscaling |
| File/container format | How are tensors and metadata packaged on disk? | Safetensors, GGUF |
| Execution | Which kernels and hardware calculate the result? | Metal GPU kernels, CUDA Tensor Cores, CPU kernels |

**Checkpoint** means saved model state. A BF16 checkpoint and an NVFP4 checkpoint can represent the same model architecture with different numerical approximations. A training checkpoint may also include optimizer state; an inference weight download often does not.

Safetensors packages tensors with a JSON header that may carry metadata; **GGUF** carries richer inference metadata — tensor types, architecture details, tokenizer and chat template — in one file. Neither name specifies one precision. [Safetensors documentation](https://huggingface.co/docs/safetensors/index), [GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md).

## 2. Floating point: range and precision are different

Think of scientific notation: **`sign × significant digits × base^exponent`**. Binary floating point uses powers of two.

| Component | What it controls |
|---|---|
| Sign | Positive or negative |
| Exponent | How large or small the number can be: its **dynamic range** |
| Fraction/significand bits, often called mantissa bits | How finely nearby numbers can be distinguished: their **precision** |

### Bit layouts at a glance

One character is one stored bit. Line length is the total width of the format.

```text
                    S sign   E exponent   M fraction (stored mantissa)

FP64        S EEEEEEEEEEE MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   64 bits
FP32        S EEEEEEEE MMMMMMMMMMMMMMMMMMMMMMM                                  32 bits
BF16        S EEEEEEEE MMMMMMM                                                  16 bits
FP16        S EEEEE MMMMMMMMMM                                                  16 bits
FP8 E4M3    S EEEE MMM                                                           8 bits
FP8 E5M2    S EEEEE MM                                                           8 bits
FP4 E2M1    S EE M                                                                4 bits
```

For ordinary normalized binary numbers the leading `1` is implicit, so a format with 23 stored fraction bits has 24 significant binary digits. Special encodings cover zero, infinity and **NaN** (“not a number”); the rules differ by format. [Microsoft's IEEE representation explanation](https://learn.microsoft.com/en-us/cpp/build/ieee-floating-point-representation?view=msvc-170).

| Format | Where it matters | Main trade-off |
|---|---|---|
| **FP64**, double | Scientific computing; numerical reference calculations | High precision and memory cost; uncommon for LLM weights |
| **FP32**, single | General computation, accumulations and some training state | More precise than 16-bit formats; twice their weight storage |
| **FP16**, half | Training and inference on supported accelerators | More fraction bits than BF16, but a narrower exponent range that can overflow or underflow outside its window |
| **BF16**, bfloat16 | Common training and reference weight format | FP32-like exponent range in 16 bits, bought with coarser precision than FP16 |
| **FP8 E4M3** | Low-precision weights and activations | More local precision than E5M2; narrower range |
| **FP8 E5M2** | Values needing wider range, including gradients in FP8 training recipes | Wider range; fewer fraction bits |
| **FP4 E2M1** | Element representation used in MXFP4 and NVFP4 | Very coarse values; scaling is essential |

Sources for layouts: [IEEE FP32/FP64](https://learn.microsoft.com/en-us/cpp/build/ieee-floating-point-representation?view=msvc-170), [Google's FP32/FP16/BF16 comparison](https://cloud.google.com/blog/products/ai-machine-learning/bfloat16-the-secret-to-high-performance-on-cloud-tpus), [original FP8 paper](https://arxiv.org/abs/2209.05433), [CUDA FP4 API](https://docs.nvidia.com/cuda/cuda-math-api/cuda_math_api/group__CUDA__MATH__FP4__MISC.html).

**Why BF16?** The name comes from **Google Brain**. It keeps FP32's exponent width and spends the saved bits on a truncated fraction, which widens the range of values a network can carry at 16 bits. [Google's BF16 explanation](https://cloud.google.com/blog/products/ai-machine-learning/bfloat16-the-secret-to-high-performance-on-cloud-tpus). “Full precision” in a model card usually means “the publisher's unquantized reference checkpoint”, measured against that release's own FP8 or 4-bit variants rather than against FP32/FP64.

**TF32 is a compute mode.** NVIDIA's TensorFloat-32 matrix-multiply path rounds FP32 inputs to 10 fraction bits, keeps FP32's exponent range and accumulates in FP32, while the tensors themselves stay FP32 in memory. [PyTorch's TF32 documentation](https://docs.pytorch.org/docs/main/notes/cuda.html#tensorfloat-32-tf32-on-ampere-and-later-devices).

**FP8 is a family, not a compatibility promise.** E4M3 and E5M2 use different special-value rules, and the original E4M3 extends its finite range by omitting infinities. E4M3 tops out at a magnitude of **448**; E5M2 reaches **57,344** with only two fraction bits. Exact variants, scaling conventions and kernels have to match between checkpoint and runtime, and “FP” alone does not establish IEEE 754 compliance. [OCP FP8 specification](https://www.opencompute.org/documents/ocp-8-bit-floating-point-specification-ofp8-specification-pdf), [FP8 format proposal](https://arxiv.org/abs/2209.05433).

## 3. INT8 and INT4: small integer codes for real-valued weights

An integer format has no exponent or fraction field. Signed INT8 conventionally spans `−128…127`; signed INT4 spans `−8…7`. Quantizers can use unsigned codes or a narrower symmetric range instead.

The codes are useful because a scale maps them back to real values. One common affine form is:

**`reconstructed weight ≈ scale × (integer code − zero point)`**

An equivalent scale-and-bias convention writes **`scale × code + bias`**. Groups of weights share these extra values. Smaller groups follow local variation better and need more metadata. Symmetric schemes typically center the range around zero. [TensorRT quantization schemes](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-schemes.html).

### A tiny example

With `scale = 0.1` and `zero point = 0`, a weight of `0.26` rounds to code `3` and reconstructs as `0.30`, so the **quantization error is the difference between the original and reconstructed value, `0.26 → 0.30` = 0.04**. A nearby `0.34` also rounds to `3` and reconstructs as `0.30`, an error of 0.04 in the other direction. Values outside the selected range may be clipped instead.

The example is conceptual: practical schemes choose scales and rounding policies across tensors or groups, sometimes using representative **calibration data** to limit errors.

| Deployment notation | What it means | What it leaves unspecified |
|---|---|---|
| **W8A8** | 8-bit weights and 8-bit activations | Integer versus floating point, scales, accumulators |
| **W4A16** | 4-bit weights and 16-bit activations | Exact weight encoding and kernel implementation |
| **Weight-only quantization** | Weight storage is compressed; activations remain at higher precision | Whether the kernel unpacks/dequantizes internally or uses supported low-bit arithmetic |

**Why W8A8 is harder than it looks.** A few activation channels carry outliers roughly 100× larger than typical values, and a single per-tensor scale stretched over those outliers leaves most channels with only a handful of usable levels. [SmoothQuant](https://arxiv.org/abs/2211.10438) moves that difficulty into the weights with a per-channel scaling factor, and [LLM.int8()](https://arxiv.org/abs/2208.07339) instead keeps outlier channels in higher precision at run time. Weight-only INT4 avoids the problem by leaving activations in 16 bits.

INT4 also has direct silicon support: integer dot-product units on NVIDIA Tensor Cores and on CPUs with INT8/INT4 kernels, while a 4-bit floating checkpoint still needs a matching kernel to run as floating-point arithmetic. TensorRT distinguishes weight-only INT4 execution from quantized activation/weight paths. [TensorRT's quantized-type documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/work-with-quantized-types.html).

## 4. FP4, MXFP4 and NVFP4: the scale is part of the story

Raw E2M1 has very few levels. Its nonnegative magnitudes are **`0, 0.5, 1, 1.5, 2, 3, 4, 6`**, with the corresponding negative values. A shared scale lets each block use those levels over a different real-world range. [NVIDIA's NVFP4 explanation](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/).

| Scheme | Element encoding | Shared scale | Idealized bits per weight, including block scale |
|---|---|---|---|
| **MXFP4** | FP4 E2M1 | One 8-bit **E8M0**, power-of-two scale per 32 elements | `4 + 8/32 = 4.25` |
| **NVFP4** | FP4 E2M1 | One FP8 **E4M3** scale per 16 elements; additional tensor-level FP32 scaling | `4 + 8/16 = 4.5`, plus tensor scale |
| **MXFP8** | FP8 E4M3 or E5M2 | One E8M0 scale per 32 elements | `8 + 8/32 = 8.25` |

MX means **microscaling**: small blocks share scales. OCP's specification defines the MX formats; NVIDIA's scheme changes scale granularity and representation. [OCP MX specification, §§5.1–5.4](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf), [NVIDIA's NVFP4 structure](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/).

The per-weight figures are arithmetic from the specified block sizes. They exclude alignment, tensor metadata and layers kept at higher precision.

**Two other names worth recognizing:** **FP6** uses six bits, including E2M3 and E3M2, and OCP also defines MXFP6. **MXINT8** applies microscaling to 8-bit integer elements. Both broaden the menu while staying less common than BF16, FP8 and INT4 in downloadable LLM releases. [OCP MX specification, §§5.2–5.3](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf).

**Reading a packed value is not the same as executing it natively.** Blackwell Tensor Cores accelerate the NVFP4 path; other architectures decode the same bits and compute in higher precision. Vendor benchmark claims concern particular models and software, so treat them as evidence about that configuration rather than a guarantee of negligible loss for every task. [NVIDIA's deployment explanation](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/).

## 5. NF4, GPTQ, AWQ and Q4_K_M: related names at different layers

| Name | What it actually is | Useful distinction |
|---|---|---|
| **NF4**, NormalFloat 4 | A 16-value, nonuniform codebook designed around normally distributed weights | Neither ordinary E2M1 FP4 nor a native NVFP4 Tensor Core format |
| **GPTQ** | A post-training weight-quantization method using approximate second-order information | A method for choosing good low-bit approximations, not a file extension |
| **AWQ** | Activation-aware weight quantization; activation statistics guide channel scaling | “Activation-aware” does not mean activations are stored in 4 bits |
| **Q4_K_M** | A llama.cpp/GGUF quantization preset using a mixture of tensor quantizations | The `4` is a nominal width, not the total bits per parameter |

Primary references: [QLoRA/NF4 paper](https://arxiv.org/abs/2305.14314), [GPTQ paper](https://arxiv.org/abs/2210.17323), [AWQ paper](https://arxiv.org/abs/2306.00978), [llama.cpp K-quants implementation](https://github.com/ggml-org/llama.cpp/blob/master/src/llama-quant.cpp), [Safetensors documentation](https://huggingface.co/docs/safetensors/index).

NF4 places its reconstruction levels nonuniformly instead of on a uniform integer grid, which is a different design from “four exponent/fraction bits”. The K-quants family behind Q4_K_M stores blocks of 32 weights against per-block scales and minima, and the M variant mixes 4-bit and 6-bit tensors, so a real Q4_K_M file averages roughly **4.8–4.9 bits per weight** rather than exactly 4. [llama.cpp K-quants implementation](https://github.com/ggml-org/llama.cpp/blob/master/src/llama-quant.cpp).

**Post-training quantization (PTQ)** converts an already trained model. **Quantization-aware training (QAT)** exposes training to quantization effects so the model can adapt. **QLoRA** freezes a quantized base model and trains low-rank adapters, rather than training every model weight directly in four-bit arithmetic. [TensorRT quantization workflows](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html), [QLoRA paper](https://arxiv.org/abs/2305.14314).

## 6. Storage is only the first part of memory planning

For **P parameters** and **b bits per stored parameter**:

**`raw weight bytes = P × b / 8`**

The table below applies this to an **illustrative 500-billion-parameter model** — a hypothetical figure used only for arithmetic, representative of a large mixture-of-experts checkpoint. Units are decimal: `1 GB = 10⁹ bytes`, `1 TB = 10¹² bytes`.

| Representation | Idealized weight storage |
|---|---:|
| FP32, 32 bits | 2,000 GB = 2.0 TB |
| BF16 / FP16, 16 bits | 1,000 GB = 1.0 TB |
| FP8 / INT8, 8 bits, before scales | 500 GB |
| Raw packed 4-bit codes, before scales | 250 GB |
| MXFP4, including one 8-bit scale per 32 weights | 265.625 GB |
| NVFP4, including one 8-bit scale per 16 weights | 281.25 GB, plus tensor scales |

```text
FP32        32 bits  ████████████████████████████████████████   2,000 GB
BF16/FP16   16 bits  ████████████████████                       1,000 GB
FP8/INT8     8 bits  ██████████                                  500 GB
NVFP4       ~4.5 b   █████▋                                      281 GB
MXFP4      ~4.25 b   █████▎                                      266 GB
raw codes    4 bits  █████                                       250 GB
```

One block = 50 GB. These are calculations, **not measured checkpoint sizes**. The MLX affine scheme is the same arithmetic from a different direction: 4-bit codes with two 16-bit metadata values per 64-weight group average `4 + 32/64 = 4.5` bits per weight, and changing metadata precision changes the result. [MLX quantization representation](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html).

### What else occupies memory?

Beyond weights, scales and any layers kept at higher precision: the **KV cache**, activations and temporary workspaces, and runtime plus communication buffers for the allocator and any distributed execution.

The **KV cache** stores attention keys and values from earlier tokens. For ordinary attention with uniform dimensions, a rough estimate is:

**`KV bytes ≈ 2 × layers × cached tokens × KV heads × head dimension × bytes per element`**

A worked example: an 80-layer model with 8 KV heads and a head dimension of 128, serving one 128K-token sequence in BF16 (2 bytes per element):

`2 × 80 × 131,072 × 8 × 128 × 2 B ≈ 42.9 GB (40 GiB)` — about **43 GB of cache for one long conversation**, before any weights are loaded. The same cache at FP8 KV precision halves to roughly 21 GB. Sum cached tokens over concurrent sequences. Grouped-query attention reduces KV heads; compressed attention designs and implementation choices change the accounting. KV-cache precision is independently configurable in supporting runtimes, so reducing weight precision does not automatically shrink this cache. [TensorRT KV-cache documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/transformers-kv-cache.html).

**Mixture-of-experts (MoE)** models activate only selected experts for each token. Fewer *active* parameters reduce some computation; the other experts still need storage or an explicit offloading/distribution strategy. Total parameters and active parameters answer different questions. [TensorRT MoE documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/transformers-moe.html).

A quoted combined device-memory total therefore does not by itself show that a workload fits: each GPU must hold its own shard plus working memory, and the runtime must support the model, quantization and multi-GPU arrangement. Long context, batch size and communication can change both capacity and speed.

Training adds gradients, optimizer state and saved activations, so a weight-only table is not a training-memory estimate.

## 7. Apple Silicon and MLX: what support means

Apple Silicon's unified memory lets CPU and GPU access shared physical memory. The operating system, applications and inference workspaces share it too, so the advertised capacity is not all available to model weights. MLX's documented execution devices are the **CPU and GPU**; the Neural Engine is not among them. [MLX repository and execution model](https://github.com/ml-explore/mlx).

The checked MLX API lists:

| MLX mode | Group size | Element representation |
|---|---:|---|
| `affine` | 32, 64 by default, or 128 | Integer codes; default four bits; scale and bias |
| `mxfp4` | 32 | E2M1 with E8M0 scale |
| `mxfp8` | 32 | E4M3 with E8M0 scale |
| `nvfp4` | 16 | E2M1 with E4M3 scale |

Other affine bit widths are supported. These are framework quantization modes, so an arbitrary checkpoint still needs model and configuration conversion before it loads. [MLX `quantize` API](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantize.html).

MLX's official implementation is **more than loading and dequantizing**: it ships fast Metal and CUDA quantized matrix-multiplication kernels with a CPU fallback, so packed data can be consumed inside specialized kernels rather than expanded to higher precision for the whole model first. [MLX pull request #2688](https://github.com/ml-explore/mlx/pull/2688), [quantized matrix multiplication API](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantized_matmul.html).

A Metal kernel that supports NVFP4 does not make Apple hardware equivalent to Blackwell's native NVFP4 Tensor Cores. The selected device and kernel determine the unpacking, conversion and arithmetic path. [MLX implementation](https://github.com/ml-explore/mlx/pull/2688), [supported devices](https://github.com/ml-explore/mlx).

## 8. Which hardware accelerates which format

“Native” here means dedicated hardware datapaths for arithmetic in that format, as distinct from a runtime that decodes packed values and computes in a wider type.

| Hardware family | Natively accelerated formats | Notes |
|---|---|---|
| NVIDIA Ampere (A100, A10, RTX 30) | FP16, BF16, TF32, INT8, INT4 Tensor Core | No FP8 datapath; TF32 is an FP32-storage compute mode |
| NVIDIA Hopper (H100, H200) | Adds FP8 E4M3/E5M2 with the FP8 Transformer Engine | First NVIDIA generation with an FP8 path |
| NVIDIA Ada (L40S, RTX 40) | Adds FP8 E4M3/E5M2 alongside FP16/BF16/TF32/INT8/INT4 | Throughput differs by SKU |
| NVIDIA Blackwell (B200, GB200, RTX 50, RTX PRO) | Adds FP4 (E2M1) and FP6 Tensor Core operations with block scaling, including NVFP4 and the OCP MX formats | FP4 throughput is twice FP8 on the same part |
| AMD CDNA3 (MI300X, MI325X) | FP16, BF16, FP8 (FNUZ variants), INT8, TF32 in Matrix Cores | No documented FP4 datapath |
| AMD CDNA4 (MI350X, MI355X) | Adds native MXFP8/MXFP6/MXFP4 | OCP FP8 variants; TF32 emulated through BF16 |
| Apple Silicon (M-series) | No documented FP8/FP4 unit for LLM matrix multiplication | MLX runs quantized matmul in Metal kernels that unpack low-bit values; CPU fallback exists |
| x86 CPU (AVX-512 VNNI, AMX) | INT8 and BF16 | FP8, FP4 and INT4 arrive by unpacking and conversion into a supported type |

NVIDIA format lists: [Blackwell/RTX Blackwell architecture brief](https://cdn.prod.website-files.com/61dda201f29b7efc52c5fbaf/6602ea9d0ce8cb73fb6de87f_nvidia-blackwell-architecture-technical-brief.pdf), [CUDA FP4 API](https://docs.nvidia.com/cuda/cuda-math-api/cuda_math_api/group__CUDA__MATH__FP4__MISC.html). AMD support: [ROCm MI300/MI350 workload optimization](https://rocmdocs.amd.com/en/docs-7.2.4/how-to/rocm-for-ai/inference-optimization/workload.html).

Two caveats apply to the whole table. Generations share architecture families but not identical throughput, so a SKU-level datasheet beats a family name for planning. And a runtime supporting a mode is not the same as hardware accelerating it — MLX exposes an `nvfp4` mode while running on Apple GPUs with no FP4 datapath.

## 9. Shortcuts worth correcting

| Shortcut | More accurate interpretation |
|---|---|
| “BF16 preserves maximal accuracy.” | It is lower precision than FP32; it may be the release's reference format. |
| “FP8 is lossless.” | Some tested workloads retain similar quality; quantization changes values. |
| “Four-bit means exactly half the memory of eight-bit.” | Scales, mixed-precision tensors and runtime memory affect the result. |
| “NVFP4 is the practical choice everywhere.” | It is attractive with matching kernels and hardware; portability and throughput differ. |
| “Only NVIDIA runs four-bit models.” | Integer and codebook quantization have broad CPU/GPU implementations; backend support differs. |
| “A four-bit model computes everything in four bits.” | Weight storage, activation format and accumulation precision can differ. |
| “MLX offloads these operations to the Neural Engine.” | MLX's documented execution devices are the CPU and GPU. |
| “If it fits, it will be fast.” | Memory bandwidth, compute, unpacking, batch size and communication all matter. |
| “A good coding benchmark proves no quality loss.” | It measures that evaluation; reasoning, long context and other tasks need their own checks. |

These distinctions follow the representations and execution paths documented above; they are not model-specific benchmark findings.

## 10. How to choose and verify a checkpoint

1. **Identify the runtime and exact hardware.** Check the supported model architecture, quantization scheme and kernel against the format matrix in §8; the GPU generation alone is insufficient.
2. **Read the quantization configuration.** Look for bit width, element format, group size, scales, activation precision and layers excluded from quantization.
3. **Estimate the full memory budget.** Add context/concurrency-dependent KV cache (§6) and runtime overhead to weights. Check per-device capacity for distributed execution.
4. **Use a reference comparison.** Run representative prompts or evaluations against the publisher's reference checkpoint; inspect important failures as well as aggregate scores.
5. **Measure the intended workload.** Record prompt-processing speed, generation speed, latency and peak memory at the context length and batch size you actually need.

Practical starting points: BF16/FP16 give a useful reference on supported hardware; FP8/INT8 take a smaller step down in storage; INT4/NF4/FP4 families pursue larger savings and depend more on quantization details. Choose between them using measured compatibility, quality and speed rather than the smallest number in the name.

## 11. Source context and verification

Format layouts, scaling schemes and hardware support were cross-checked against Google, NVIDIA, AMD, OCP, MLX, the original FP8/QLoRA/GPTQ/AWQ/SmoothQuant/LLM.int8() papers and container specifications linked inline. Support statements describe documentation read on **22 October 2026**. The 500B table is explicitly hypothetical arithmetic, and no hardware throughput or model-quality benchmark was reproduced for this note.

---

**Related:**
- [LLM Inference](../architecture/LLM-Inference.md) — connects numerical precision to the wider inference process and serving costs.
- [LLM Inference Engines](../architecture/LLM-Inference-Engines.md) — explains the runtimes whose kernels determine whether a quantized checkpoint runs efficiently.
- [Parameter-Efficient Fine-Tuning](../../Fine-Tuning/Parameter-Efficient-Fine-Tuning.md) — connects quantized base weights with LoRA and memory-efficient adaptation.
- [AI Hardware Chips Explained](../../Hardware/AI-Hardware-Chips-Explained.md) — compares the hardware that executes these numerical representations.
