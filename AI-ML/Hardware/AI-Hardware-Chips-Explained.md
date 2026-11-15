# AI Hardware for Machine Learning: A Practical Guide

**Learning note · Revised 15 November 2026 · Selected vendor documentation checked**

> **Core idea:** AI workloads use several kinds of processors because no single chip is best at every task. Compare the workload, memory system, software support and total cost rather than relying on chip labels.

## 1. Why AI uses specialized hardware

Training and running neural networks involves large amounts of matrix and tensor math. Performance also depends on how quickly a processor can move model weights and intermediate data between memory and compute units. A chip with more arithmetic units may still perform poorly if memory bandwidth, capacity or communication is the bottleneck.

AI systems therefore combine general-purpose processors with accelerators. The right mix depends on whether the system trains a model, serves requests in a data center, or runs a smaller model on a device.

## 2. The main processor types

| Type | Typical role | Common trade-off |
|---|---|---|
| **CPU** | Runs operating systems, application logic, data preparation and orchestration. It can also run small models. | Flexible, but usually less efficient than a suitable accelerator for large parallel tensor workloads. |
| **GPU** | Trains and serves many kinds of neural networks using highly parallel compute. | Broad software support and flexibility; performance depends on memory, interconnect and workload fit. |
| **TPU** | Google's tensor accelerator for supported machine-learning workloads, including large-scale training and inference. | Can be efficient for workloads and software built for the platform; less interchangeable with general-purpose GPUs. [Google Cloud TPU overview](https://cloud.google.com/tpu/docs/intro-to-tpu) |
| **NPU** | Runs supported AI operations efficiently on phones, PCs and other edge devices. | Low-power local inference; model size and supported operations vary by device. [Apple Core ML](https://developer.apple.com/documentation/coreml/mlmodelconfiguration/computeunits) describes how its runtime selects available compute units. |
| **Custom accelerator / ASIC** | Performs a defined set of operations for a provider's own training or inference services. | Can improve cost or energy use at scale, but depends on its software ecosystem and supported workloads. AWS provides [Trainium](https://aws.amazon.com/machine-learning/trainium/) for training and [Inferentia](https://aws.amazon.com/machine-learning/inferentia/) for inference. |
| **DPU** | Offloads infrastructure work such as networking, storage and security in data centers. | Frees host processors for application work; it is not a substitute for a tensor accelerator. [NVIDIA's DPU overview](https://www.nvidia.com/en-us/networking/products/data-processing-unit/) |

**TPU**, **NPU**, **LPU** and **IPU** are labels used by vendors for different products and designs. The names alone do not tell you which operations a chip supports or how it will perform. Check the actual hardware and software specifications.

## 3. Where each type fits

A typical server uses CPUs to handle requests and coordinate work, then sends supported model operations to GPUs or other accelerators. A data-center accelerator may be paired with a high-bandwidth memory system and a fast interconnect so multiple chips can share work. A phone or laptop may use an NPU to run supported inference locally, with the CPU or GPU handling other operations.

Specialized research hardware has different goals. Neuromorphic chips explore event-driven computation. Quantum processors are experimental systems for particular quantum algorithms; they are not general replacements for GPUs in current neural-network training or serving.

## 4. How to choose hardware

Start with a representative end-to-end workload, then compare:

1. **Compute:** Which numeric formats and operations does the model use, and are they supported efficiently?
2. **Memory:** Does the model fit? Is memory bandwidth enough for the workload, especially during token-by-token inference?
3. **Communication:** For multi-chip training or serving, how much data must move between accelerators?
4. **Software:** Are the drivers, compiler, framework and model kernels mature for the tasks you need?
5. **Operations and cost:** Measure throughput, latency, power and total system cost under realistic traffic. Peak chip specifications alone are not a production benchmark.

For a small on-device model, power and local availability may matter most. For large-scale serving, memory capacity, interconnect, utilization and cost per generated token can dominate. Training also places different demands on memory and communication than inference.

## 5. A compact rule of thumb

- Choose a **CPU** for general control flow and flexible application work.
- Consider a **GPU** when you need a programmable, widely supported accelerator.
- Evaluate a **TPU or custom accelerator** when its software stack supports your workload and scale justifies the platform.
- Use an **NPU** when supported inference needs to run locally within a device's power budget.
- Add a **DPU** when data-center networking or storage work is consuming significant host resources.

These are starting points, not universal rankings. Benchmark the model, batch size, sequence length, precision and serving setup you plan to use.

## 6. Source context and references

The product roles were checked against the linked TPU, Core ML, Trainium, Inferentia and DPU documentation. Hardware selection guidance is a workload-based evaluation framework, not a benchmark ranking.


- [Google Cloud TPU documentation](https://cloud.google.com/tpu/docs/intro-to-tpu)
- [Apple Core ML documentation](https://developer.apple.com/documentation/coreml/mlmodelconfiguration/computeunits)
- [AWS Trainium](https://aws.amazon.com/machine-learning/trainium/) and [AWS Inferentia](https://aws.amazon.com/machine-learning/inferentia/)
- [NVIDIA DPU overview](https://www.nvidia.com/en-us/networking/products/data-processing-unit/)

---

**Related:**
- [LLM Inference](../LLMs/architecture/LLM-Inference.md) — Connects model-serving behavior to compute, memory and accelerator choices.
- [KV Cache, Prefix Caching and Storage Tiers](../LLMs/architecture/KV-Cache-Prefix-Caching-And-Storage-Tiering-Nov-2026.md) — Explains memory pressure and data movement during inference.
- [AI Numerical Formats and Quantization](../LLMs/optimization/AI-Numerical-Formats-And-Quantization-Oct-2026.md) — Covers how numeric formats affect model size and hardware execution.
- [FlashAttention](../Comparisons/Self-Attention-vs-Flash-Attention.md) — Shows how attention kernels reduce memory traffic on accelerators.
