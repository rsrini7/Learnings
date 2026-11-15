# FlashAttention: Exact Attention with Less GPU Memory Traffic

**Learning note · Revised 15 November 2026 · Original paper and reference implementation checked**

> **Core idea:** FlashAttention keeps the standard attention calculation but changes how it is executed. Tiling and fused operations reduce data movement and avoid storing the full attention matrix in high-bandwidth memory.

## 1. The attention workload

For a sequence of *N* tokens, standard self-attention compares each token with the others. The pairwise calculation therefore grows approximately with *N²*. In a straightforward implementation, the score and probability matrices also contain *N²* values, which can consume substantial GPU memory.

GPUs have small, fast on-chip memory and larger high-bandwidth memory (HBM). Moving intermediate results between them can limit speed, especially when the implementation repeatedly writes a large attention matrix to HBM.

## 2. What FlashAttention changes

FlashAttention divides the query, key and value matrices into tiles. It loads a tile into fast on-chip memory, computes attention for that tile, and combines the results using an online softmax calculation. Fused kernels avoid writing the full score and probability matrices to HBM. During backpropagation, the algorithm recomputes selected values instead of storing every intermediate.

The [original paper](https://arxiv.org/abs/2205.14135) describes FlashAttention as an **IO-aware exact attention algorithm**: it reduces memory traffic without replacing softmax attention with an approximation. Floating-point operation order can still produce small numerical differences; the [reference implementation](https://github.com/Dao-AILab/flash-attention) documents its numerical-tolerance checks.

![FlashAttention tiled memory flow](assets/FlashAttention-Tiled-Memory-Flow-2026.svg)

*Both paths compute dense attention. The key difference is whether the full attention intermediates are stored in HBM.*

## 3. Comparison

| | Straightforward attention implementation | FlashAttention |
|---|---|---|
| Attention calculation | Pairwise attention; work grows roughly with sequence length squared. | Same attention function and asymptotic pairwise work. |
| Intermediate matrix | May materialize and store an N × N score or probability matrix. | Computes tiled blocks without materializing the full matrix in HBM. |
| Memory use | Can grow quadratically for the attention intermediates. | Reduces attention-intermediate memory; the algorithm's extra memory grows linearly with sequence length. |
| Data movement | May repeatedly read and write large intermediates. | Reuses tiles in on-chip memory to reduce HBM traffic. |
| Speed and memory savings | Depend on the baseline kernel and hardware. | Depend on hardware, sequence length, dimensions and implementation. |

The table compares FlashAttention with a straightforward implementation. Other optimized attention kernels may have different trade-offs.

## 4. What it does not change

FlashAttention does **not** make standard attention's pairwise calculation linear in sequence length. It reduces memory movement and the storage required for attention intermediates. Model weights, activations, key-value caches and other system costs still matter.

It also does not set a model's context window by itself. Context length depends on model design, training, serving software, available memory and latency requirements. FlashAttention can make some long-sequence workloads more practical, but it does not guarantee a particular context length or speedup.

## 5. When it helps

FlashAttention is useful when attention intermediates or memory traffic limit training or inference, and when the model's hardware and software stack can use a supported implementation. The [reference repository](https://github.com/Dao-AILab/flash-attention) provides kernels and setup guidance; follow its compatibility notes, then benchmark your own batch size, sequence length, head dimensions, precision and GPU generation. The kernels only help supported configurations.

For a system-level view of how memory constraints affect token generation, see [LLM inference](../LLMs/architecture/LLM-Inference.md).

## 6. Source context and references

The mechanism and complexity explanation were checked against the original FlashAttention paper and its reference implementation. No fixed speedup or proprietary model implementation is inferred from those sources.


- Tri Dao et al., [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135), NeurIPS 2022.
- Tri Dao, [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691), 2023.
- [FlashAttention reference implementation](https://github.com/Dao-AILab/flash-attention).

---

**Related:**
- [Beyond Softmax Attention](../LLMs/attention/Beyond-SoftMax-Attention.md) — Compares changes to the attention mechanism itself, which differ from FlashAttention's kernel optimization.
- [LLM Inference](../LLMs/architecture/LLM-Inference.md) — Covers serving constraints such as memory, batching and token-generation latency.
- [AI Hardware Explained](../Hardware/AI-Hardware-Chips-Explained.md) — Introduces the memory and accelerator concepts behind IO-aware kernels.
- [Top 50 AI/ML Math Q&A](Top-50-Q&A-AI-ML-Math.md) — Reviews the softmax and attention math used by the algorithm.
