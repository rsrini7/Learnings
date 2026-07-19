# LLM Inference Explained: A Comprehensive Guide

## What is Inference?

In the AI space, everyone knows what inference is. Outside of it, almost no one does. When I tell people I started working at an LLM inference provider, the first question I usually get is: what is inference? This post attempts to answer that question with verified information and real-world examples.

Every day, AI applications support millions of users, giving instant, seemingly magical answers. Behind every AI application is a process that's invisible to end users but determines everything about their product experience: **inference**.

---

## The Two Stages of AI: Training and Inference

Working with AI models involves two distinct stages:

### 1. The Training Stage
During training, a model learns how to perform tasks like recognizing images, generating text, or making decisions. Think of this as the education phase: you're feeding the model massive amounts of data, adjusting its parameters through many iterations, and teaching it to recognize patterns and relationships.

**Real-World Training Example:**
- **GPT-4**: Trained on trillions of tokens from diverse sources (books, websites, code repositories)
- **Training Duration**: Can take weeks to months on thousands of GPUs
- **Cost**: Estimated at $50-100 million for large models
- **Modern Approach**: Many companies use techniques like pre-training (learning general language), mid-training (specialized domains), supervised fine-tuning (following instructions), and reinforcement learning with human feedback (RLHF) to align with user preferences

### 2. The Inference Stage
AI inference is the process of using a trained AI model to make predictions on new data. Unlike training, inference must be fast and efficient, as it often occurs in real-time as users interact with AI applications.

**Real-World Inference Example:**
When you ask ChatGPT "What's the weather like today?" and get a response in 2 seconds, that's inference—getting an output from a model based on your input.

---

## What Happens During AI Inference?

Let's trace the complete lifecycle of a request from end user to model server and back:

### Step 1: User Request
The user hits an API endpoint, either directly or through a user interface. A request is sent containing:
- User's input (e.g., "Explain quantum computing")
- Model parameters (max tokens, temperature, etc.)
- Authentication headers

**Example:** When you type in Claude.ai or ChatGPT, this request travels across the internet to the inference server.

### Step 2: Intelligent Routing
The request is routed to the most appropriate model server through:
- **Geo-aware load balancing**: Routes you to the nearest data center (if you're in London, your request goes to European servers)
- **LoRA-aware routing**: Directs specialized requests to servers with the right model adaptations
- **KV cache-aware routing**: Sends follow-up messages in a conversation to servers that already have your chat history cached
- **Queue management**: If servers are busy, requests wait in prioritized queues with timeouts

### Step 3: Inference Runtime Processing
Once the request reaches a model server equipped with GPU and CPU resources, an inference framework takes over. Popular frameworks include:

#### **TensorRT-LLM** (by NVIDIA)
- **Strengths**: Highly optimized CUDA kernels, maximum performance on NVIDIA GPUs
- **Use Case**: When you need absolute peak performance and use NVIDIA H100/A100 GPUs
- **Real Example**: Used by companies needing sub-100ms latency for code completion
- **Performance**: Can achieve up to 5,000 tokens/second on Llama-8B models

#### **SGLang**
- **Strengths**: RadixAttention for caching repeated prompt patterns, excellent for chatbots
- **Use Case**: Interactive applications where conversation history is reused
- **Real Example**: Powers LMSYS Chatbot Arena serving millions of requests
- **Performance**: Up to 3.1x higher throughput than vLLM on Llama-70B, deployed on 400,000+ GPUs worldwide
- **Innovation**: Keeps conversation history and few-shot examples in cache separately for faster responses

#### **vLLM**
- **Strengths**: PagedAttention for efficient memory management, broad model support
- **Use Case**: General-purpose serving with good balance of features and performance
- **Real Example**: Used by companies like Uber and LinkedIn for production LLM serving
- **Performance**: Industry standard for continuous batching, supports INT8/INT4 quantization
- **Popularity**: Most widely adopted open-source inference framework

These frameworks handle the actual inference steps:

**a) Tokenization**: Converting your text into numbers (tokens) the model understands
- Example: "Hello world" → [15496, 995] 

**b) Prefill Stage**: Processing the entire input prompt to build the KV cache
- **Time Impact**: A 3,000 token document can take 1.4 seconds just for prefill
- **What's Happening**: The model reads and "understands" your entire prompt

**c) Decode Stage**: Generating output tokens one by one
- **Autoregressive Generation**: Each token is generated based on all previous tokens
- **Speed**: Typically 10-100 tokens/second depending on model size and hardware

### Step 4: Response Delivery
Results are sent back to the user through:
- **Streaming (SSE/WebSockets)**: Tokens appear as they're generated (like ChatGPT's typing effect)
- **Batch Response**: Full text returned after completion
- **Webhooks**: For long-running async tasks

---

## AI Inference in Action: Real-World Applications

### Interactive Applications
- **ChatGPT/Claude**: Every conversational response
  - Requirement: Sub-500ms time to first token for responsiveness
  - Volume: Millions of daily users globally

- **GitHub Copilot**: Code completion as you type
  - Requirement: Sub-100ms latency for seamless developer experience
  - Challenge: Must process multiple source files for context

- **Voice Assistants** (Siri, Alexa): Processing spoken commands
  - Requirement: Near-instant response for natural conversation
  - Pipeline: Speech-to-text → LLM inference → Text-to-speech

### Document Processing
- **Google Translate**: Real-time language translation
  - Performance: Mistral Large 2512 achieves 0.40s first token, 0.020s per token
  - Scale: Billions of translations daily

- **Gmail Spam Filter**: Email classification
  - Challenge: Must process millions of emails per second
  - Optimization: Batch processing for efficiency

### Enterprise Applications
- **Medical Search** (e.g., Hippocratic AI): Searching medical literature
  - Requirement: High accuracy with cited sources
  - Input Size: Often 10,000+ tokens from multiple documents

- **AI Video Editing** (e.g., Descript): Understanding and editing video content
  - Challenge: Processing transcripts and visual data simultaneously
  - Multimodal: Combining text and image inference

---

## Why AI Inference is Hard to Build

Building production-ready AI inference systems presents three core challenges:

### 1. Speed Requirements Are Unforgiving
Users expect instant responses. Moving from "decent" to "excellent" latency requires sophisticated optimizations:

**Latency Benchmarks (Real Data from 2024-2026):**
- **Chatbots**: Need <500ms time to first token (TTFT)
- **Code Completion**: Need <100ms TTFT
- **Translation**: Best models achieve 0.40s TTFT (Mistral Large 2512)
- **Long Documents**: Can take 7+ seconds TTFT for complex analysis (DeepSeek V3.2)

**Performance Impact Example:**
- Going from 4 to 8 GPUs only reduces latency by 0.7x for Llama2-70B due to communication overhead
- Each additional input token adds approximately 0.24ms to TTFT
- For a 3K token input, prefill can consume 85% of total inference time

### 2. Reliability for Mission-Critical Applications
Users demand high availability and consistent performance:

**Challenges:**
- **Memory Management**: KV cache grows with conversation length, can cause out-of-memory errors
- **Batching Trade-offs**: Higher concurrency boosts throughput but increases per-user latency
- **Queue Management**: Must handle traffic spikes without dropping requests

**Real Example:** Systems use techniques like least-deadline-first scheduling to ensure time-critical requests get priority, achieving up to 2.83× lower tail TTFT.

### 3. Cost Optimization at Scale
Every inference request consumes expensive compute resources:

**Cost Factors:**
- **GPU Costs**: NVIDIA H100 GPUs cost $30,000+ each
- **Scaling Economics**: Unlike training (one-time), inference runs every request
- **Volume Impact**: A popular application serving 10M requests/day can cost millions annually

**Optimization Strategies:**
- **Batching**: Process multiple requests together (can increase throughput 5-10x)
- **Quantization**: Reduce model from FP16 to INT8/INT4 (50% memory reduction, minimal accuracy loss)
- **Model Compression**: DistilBERT achieves 97% of BERT's performance at 60% faster speed

The challenging part? These requirements often conflict—optimizing for speed might increase costs, while cost-cutting measures can hurt reliability.

---

## The Anatomy of an Inference Stack

Solving these challenges requires optimizations across every layer:

### Runtime-Level Optimizations
- **Custom Kernels**: Highly optimized GPU operations
  - Example: FlashAttention reduces memory movement costs by 10-20x
  
- **Speculation Engine**: Predict and generate multiple tokens in parallel
  - Impact: Can reduce generation time by 2-3x for certain patterns

- **Model Parallelism**: Split model across multiple GPUs
  - Tensor Parallelism: Distribute computation within layers
  - Pipeline Parallelism: Distribute layers across GPUs
  - Challenge: Communication overhead limits scaling beyond 8 GPUs

- **Agentic Tool Use**: Allow models to call external tools mid-generation
  - Example: Web search, calculator, code execution

### Infrastructure-Level Optimizations
- **Geo-aware Load Balancing**: Route requests to nearest data center
  - Impact: Reduces network latency by 50-200ms

- **SLA-aware Autoscaling**: Dynamically adjust capacity
  - Challenge: GPU startup takes 30-60 seconds

- **Protocol Flexibility**: Support SSE, WebSockets, gRPC
  - Trade-off: Streaming adds overhead but improves perceived responsiveness

- **Multi-cluster Management**: Distribute across cloud providers and regions
  - Benefit: Redundancy and geographic coverage

### Advanced Optimizations

**KV Cache Management:**
- **PagedAttention (vLLM)**: Efficient memory paging reduces waste
- **RadixAttention (SGLang)**: Cache repeated prompt patterns
- **Impact**: Can achieve 69× average TTFT reduction for chat applications

**Attention Optimizations:**
- **Multi-Query Attention (MQA)**: Share keys/values across attention heads
- **Grouped-Query Attention (GQA)**: Balance between MQA and standard attention
- **Result**: Reduced memory requirements allow larger batch sizes

---

## How to Measure Inference Success

### 1. Latency: How Fast the Model Responds

**Key Metrics:**

**Time to First Token (TTFT)**
- Definition: Delay between request and first generated token
- Target: <500ms for chatbots, <100ms for code completion
- Factors: Prompt length (linear relationship: ~0.24ms per token), system load, GPU type

**Real-World Examples:**
- GPT-5.2: 0.55s TTFT for translation
- Claude 4.5 Sonnet: 2s TTFT for Q&A
- Grok 4.1: 3-6s TTFT but excellent generation speed

**Time Per Output Token (TPOT)**
- Definition: Average time between consecutive tokens
- Target: <50ms for natural reading speed (450 words/minute)
- Sweet Spot: 10-30ms provides fluid experience

**End-to-End Latency (E2E)**
- Formula: TTFT + (TPOT × number of output tokens)
- Example: 2s TTFT + (0.03s × 100 tokens) = 5s total

### 2. Throughput: How Much the Model Can Handle

**Tokens Per Second (TPS)**
- **Output TPS**: How fast the model generates text
  - High-end: 5,000+ TPS (Llama-8B on optimized systems)
  - Production: 100-1000 TPS typical for served models
  
- **Input TPS**: How fast the model processes prompts
  - Less visible but crucial for long documents

**Requests Per Second (RPS)**
- Varies dramatically based on request size
- Example: 10 RPS for long reports vs. 100 RPS for short queries

**Trade-offs:**
- Higher concurrency → higher total throughput → higher per-user latency
- Example: Processing 16 queries concurrently vs. sequentially doubles throughput but triples per-user latency

### 3. Cost: Hardware and Operational Expenses

**Hardware Selection:**
- **NVIDIA H100** (~$30K each): Peak performance, highest cost
- **NVIDIA A100** (~$15K each): Good balance for most workloads  
- **AMD MI300X**: Competitive alternative, slightly lower cost
- **Considerations**: Memory bandwidth, interconnect speed (NVLink), availability

**Cost-Reduction Strategies:**

**Batching**
- Process multiple requests together
- Impact: 5-10x throughput improvement
- Trade-off: Increased latency for individual requests

**Quantization**
- FP16 → INT8: 50% memory reduction, 2x throughput, <1% accuracy loss
- FP16 → INT4: 75% memory reduction, 4x throughput, 1-3% accuracy loss
- Example: DistilBERT achieves 97% accuracy at 40% size

**Model Selection**
- Smaller models (7B-13B): Good for most tasks, 5-10x cheaper to serve
- Larger models (70B+): Better quality, but exponentially more expensive
- Distilled models: 60-80% cost savings with minimal quality loss

---

## Practical Insights

### Input vs. Output Impact
**Verified Finding:** 100 input tokens have approximately the same latency impact as 1 output token.

**Optimization Strategy:** If you need speed, reducing output length is far more effective than reducing input length.

**Example:**
- Reducing output from 500 to 100 tokens: ~400 × TPOT savings (12-40 seconds)
- Reducing input from 2,000 to 1,500 tokens: ~500 × 0.24ms savings (120ms)

### The Memory Bandwidth Bottleneck
LLM inference is typically **memory-bandwidth bound**, not compute-bound.

**Implication:** Loading model weights from memory is the bottleneck. Solution is to do as much as possible when weights are loaded:
- **In-flight batching**: Process multiple requests simultaneously
- **Speculative inference**: Generate multiple candidate tokens in parallel

### Scaling Diminishing Returns
Adding more GPUs for inference has significantly diminishing returns compared to training.

**Evidence:**
- Llama2-70B going from 4 to 8 GPUs: Only 0.7× latency reduction
- Reasons: Communication overhead, lower GPU utilization
- Sweet Spot: 4-8 GPUs for most models

---

## Conclusion

AI inference is the invisible engine powering every AI application you use. While training gets the headlines, inference is where AI models prove their worth in production—serving millions of users with responses that feel instantaneous.

The field is rapidly evolving:
- New frameworks like SGLang achieve 3.1× better throughput than predecessors
- Hardware advances (H100 → B200) continue to improve performance
- Techniques like speculative decoding and advanced caching push boundaries

For developers and companies building with AI, understanding inference isn't optional—it's fundamental to delivering fast, reliable, and cost-effective AI applications.

**Key Takeaways:**
1. **Inference happens every request** (vs. training once)—so it's where costs accumulate
2. **Latency matters more than raw speed** for user experience
3. **The right optimization depends on your use case**: chatbots need low TTFT, batch processing needs high throughput
4. **No silver bullet exists**: every optimization involves trade-offs between speed, cost, and reliability

Ref: https://x.com/madisonkanna/status/2010950830804123719

Continue Reading : [LLM-Inference-Engines.md](LLM-Inference-Engines.md)

**Related:**
- [OpenResponses-Open-Inference-Standard](../optimization/OpenResponses-Open-Inference-Standard.md) — Defines the inference API standard referenced in this file's protocol section (SSE, WebSockets, OpenAI-compatible endpoints).
- [GenAI-cost-Optimization](../optimization/GenAI-cost-Optimization.md) — Cost-reduction strategies here complement the cost optimization section in this inference guide.
- [Auto-Regression](../training/Auto-Regression.md) — Explains the autoregressive mechanism that makes the decode phase memory-bound as detailed in this file.
- [LLM-Benchmarks](LLM-Benchmarks.md) — Provides benchmarks for measuring the latency and throughput metrics (TTFT, TPOT) defined in this file.
