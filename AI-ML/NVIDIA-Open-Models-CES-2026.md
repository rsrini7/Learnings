# NVIDIA's Open Models at CES 2026

## Executive Summary

At CES 2026, NVIDIA announced 13 groundbreaking open-source AI models spanning six critical domains: autonomous driving, robotics, healthcare, climate science, agentic AI, and embodied intelligence[1]. This represents NVIDIA's commitment to democratizing frontier AI, with all models available on Hugging Face and compatible with the new Vera Rubin platform[2].

---

## Hardware Context: Vera Rubin Platform

Before diving into the models, understanding the hardware foundation is essential[3].

**Key Specifications:**
- **5x faster inference** than Blackwell architecture for data centers
- **10x reduction** in token generation costs compared to previous platforms
- **Six-chip codesigned system** optimized for both training and inference
- **Major adopters**: AWS, Google, Microsoft, Oracle

**Strategic Impact:** The Vera Rubin platform shifts NVIDIA's focus from gaming GPUs to developer tools and enterprise AI infrastructure, with no new consumer GPU launches announced at CES[3].

---

## 1. Nemotron: Agentic AI Models

Nemotron is NVIDIA's multimodal AI model family designed for building intelligent agents[2][4].

### 1.1 Nemotron Speech ASR (Automatic Speech Recognition)

**Purpose:** Real-time voice transcription for AI agents and applications

**Technical Specifications[5]:**
- **Architecture:** FastConformer RNNT with 24 encoder layers
- **Parameters:** 600M (lightweight for edge deployment)
- **Input:** 16 kHz streaming audio
- **Output:** English text with automatic punctuation and capitalization
- **Model Size:** Same as previous Parakeet models (~600M parameters)

**Latency Options (Runtime Configurable):**
| Mode | Latency | Use Case |
| --- | --- | --- |
| 80ms | Ultra-low latency | Voice agents, real-time interactions |
| 160ms | Balanced | Production voice applications |
| 560ms | Higher accuracy | Transcription accuracy priority |
| 1.12s | Maximum accuracy | Non-real-time applications |

**Performance Metrics[5]:**
- **Median time-to-final transcription:** 24ms (fastest in industry)
- **End-to-end voice-to-voice loop:** <900ms for local deployment
- **Finalization stability:** Constant even for long utterances (critical for natural conversations)

**Key Innovation:** Cache-aware streaming architecture with 8x downsampling using depth-wise separable convolutions—compared to traditional 4x systems, processes significantly fewer tokens per second while maintaining accuracy[5].

**Availability:** Fully local inference with MLX versions for Mac, Gradio interfaces for testing on Hugging Face Spaces[1]

**Use Cases:**
- Voice agents and conversational AI
- Live meeting transcription and captioning
- In-car voice assistance
- Edge device applications (phones, IoT)
- Replacing Whisper for superior accuracy and speed

### 1.2 Nemotron RAG Embedding Model

**Purpose:** Retrieval-augmented generation for multimodal documents

**Key Feature:** Unlike traditional text-only RAG, this model handles:
- Vision embeddings
- Text embeddings
- Multimodal document embeddings (PDFs, images with text, etc.)

### 1.3 Nemotron RAG Reranker

**Purpose:** Rerank retrieved documents in RAG pipelines

**Multimodal Support:** Processes vision and text simultaneously for improved relevance ranking

---

## 2. Alpamayo: Autonomous Vehicle Reasoning Models

Alpamayo is NVIDIA's first open-source reasoning model family specifically designed for Level 4 autonomous vehicles[6][7].

### Core Philosophy

Unlike perception-only systems, Alpamayo enables vehicles to **explain decisions** through chain-of-thought reasoning, crucial for safety validation and regulatory compliance[6].

### 2.1 Alpamayo 1 Model Family

**Model Type:** Vision-Language-Action (VLA)

**Technical Specifications:**
- **Size:** 10B parameters (compact for vehicle deployment)
- **Architecture:** Reasoning-based decision making with explainability
- **Training Data:** Cosmos Reason foundation models

**Capabilities:**

| Capability | Description |
| --- | --- |
| **Interpretability** | Generates human-readable reasoning traces explaining *why* vehicles make specific decisions |
| **Complex Scenarios** | Handles "long-tail" driving scenarios (rare, unpredictable situations) |
| **Chain-of-Thought** | Structured reasoning for novel situations not in training data |
| **Trajectory Planning** | Bridges reasoning with precise motion planning |
| **Real-World Judgment** | Perceives, reasons, and acts with human-like decision-making |

**Addressing the "Long-Tail Problem:**
- Traditional autonomous driving struggles with rare, unpredictable scenarios
- Alpamayo's reasoning approach anticipates novel situations
- Improves safety for Level 4 autonomy (driverless capability)[7]

### 2.2 AlpaSim Simulation Framework

**Purpose:** Closed-loop testing without extensive real-world validation

**Capabilities:**
- Neural reconstruction tools
- Synthetic scenario generation
- Testing across diverse:
  - Traffic patterns
  - Weather conditions
  - Edge cases and rare scenarios

**Impact:** Dramatically reduces real-world testing time and accelerates validation cycles[6]

### 2.3 Physical AI Open Datasets

**Dataset Size:** 1,700+ hours of driving data

**Geographic Diversity:** Collected across widest range of geographies and conditions

**Data Quality:**
- Real-world edge cases
- Complex driving scenarios
- Diverse weather and traffic conditions
- Essential for training reasoning architectures[2][6]

### Industry Adoption

**Mercedes-Benz:** Launching vehicle with Alpamayo early 2026[1]

**Industry Leaders:** 
- Uber: Recognizes Alpamayo's potential to accelerate Level 4 deployments[6]
- S&P Global: Notes model enables transparency for regulatory collaboration[6]

---

## 3. Cosmos: Physical AI and Robotics

Cosmos is NVIDIA's platform for world models, simulation, and embodied AI[1][2].

### 3.1 Cosmos Models Family

**Purpose:** Generate synthetic training data for robotics and physical AI

**Model Types:**

| Model | Purpose | Application |
| --- | --- | --- |
| **Cosmos Transfer** | Domain adaptation | Fine-tuning for specific robot tasks |
| **Cosmos Predict** | World modeling | Generate synthetic training videos for robot learning |
| **Cosmos Reason** | Reasoning foundation | Underlying reasoning engine for VLAs |

**Applications:**
- Generating synthetic training videos for real-world robot tasks
- Transfer learning across different robot morphologies
- Reducing dependency on extensive real-world data collection

### 3.2 Isaac GR00T N1.6

**Type:** Vision-Language-Action (VLA) Model

**Specialization:** Humanoid robots

**Specifications:**
- **Purpose-Built:** Full-body control for humanoid platforms
- **Reasoning:** Built on Cosmos Reason for contextual understanding
- **Open Source:** Available on Hugging Face

**Capabilities:**
- Complete body control (not just manipulation)
- Contextual reasoning for task planning
- Adaptation across humanoid robot designs

### 3.3 Video Search and Summarization Blueprint

**Component:** Part of NVIDIA Metropolis platform

**Purpose:** Reference workflow for vision AI agents

**Capabilities:**
- Analyze large volumes of recorded video
- Real-time video stream analysis
- Application: Operational efficiency and public safety

---

## 4. Clara: Healthcare and Life Sciences

Clara is NVIDIA's initiative to accelerate drug discovery and medical treatment development[2].

### 4.1 Clara Models Overview

**Strategic Goal:** Bridge gap between digital discovery and real-world medicine

**Model Applications:**
- Protein folding and structure prediction
- Drug-protein interaction modeling
- Clinical outcome prediction
- Medical imaging analysis
- Healthcare cost reduction

**Impact:** Lower costs and faster time-to-treatment through AI-accelerated discovery and development[2]

**Status:** New Clara AI models launched at CES 2026 for expanded healthcare applications

---

## 5. Earth-2: Climate Science

**Purpose:** AI models for climate science research and environmental monitoring[2]

**Applications:**
- Climate pattern prediction
- Environmental impact modeling
- Weather forecasting improvement
- Carbon footprint tracking

**Status:** Part of NVIDIA's domain-specific AI initiative

---

## 6. Additional Robotics and Embodied Intelligence

### Isaac Blueprint and Tools

**NVIDIA's Robotics AI Stack:**
- Foundation models for robotic perception and control
- Simulation environments for robot training
- Edge hardware deployment options
- All available on Hugging Face

**Market Vision:** Position NVIDIA as "Android for robotics"—a default platform comparable to Android's role in smartphones[2]

---

## Key Technical Innovations

### 1. Streaming Architecture (Nemotron Speech ASR)

**Challenge:** Previous streaming models waste compute by processing overlapping audio frames multiple times

**Solution:** Cache-aware design that tracks computed vs. uncomputed frames, eliminating redundant processing[5]

**Benefit:** 8x more efficient downsampling without accuracy loss

### 2. Vision-Language-Action (VLA) Models

**Common across:** Alpamayo, Isaac GR00T, agentic models

**Advantage:** Unified architecture combining:
- **Vision:** Environmental perception
- **Language:** Reasoning and explanation
- **Action:** Trajectory planning or control commands

**Significance:** Enables interpretable AI—models can explain decisions, crucial for safety-critical applications

### 3. Multimodal Embeddings

**Innovation:** RAG embeddings handle not just text but vision + multimodal documents

**Practical Impact:** Better retrieval for complex document types (PDFs with images, technical specs, etc.)

### 4. Open and Interpretable Design

**Theme across all models:** Emphasis on transparency and auditability

**Why it matters:**
- Safety-critical applications (AVs) require explainability
- Regulatory compliance
- Enterprise trust and deployment

---

## Comparison: NVIDIA Models vs Alternatives

### Speech Recognition

| Model | Latency (160ms mode) | Deployment | Cost | Interpretability |
| --- | --- | --- | --- | --- |
| **Nemotron Speech ASR** | 24ms median | Local or cloud | Open-source | N/A |
| **Whisper** | 200ms+ | Cloud API | Paid | Limited |
| **Industry APIs** | 200ms+ | Cloud only | Per-call fees | Limited |

### Autonomous Vehicle Models

| Aspect | Traditional AV Systems | Alpamayo |
| --- | --- | --- |
| **Decision Making** | Black-box perception → planning | Reasoning-based with explanations |
| **Long-Tail Handling** | Requires massive data collection | Chain-of-thought reasoning generalizes |
| **Interpretability** | Limited | Full transparency |
| **Regulatory Alignment** | Challenging | Built for compliance |
| **Ecosystem** | Proprietary | Open-source, extensible |

---

## Practical Implementation Path

### For Voice AI Developers

1. **Get Started:** Access Nemotron Speech ASR on Hugging Face or local MLX version
2. **Test:** Use Gradio Space for quick evaluation
3. **Deploy:** Choose latency mode (80ms-1.12s) based on use case
4. **Scale:** Integrate with Nemotron 3 Nano (4-bit) for efficient inference

### For Roboticists

1. **Simulation:** Start with Cosmos models for synthetic data generation
2. **VLA Training:** Fine-tune Isaac GR00T or Alpamayo for specific tasks
3. **Deployment:** Run on NVIDIA edge hardware (Jetson) or cloud
4. **Datasets:** Leverage Physical AI Open Datasets (1,700+ hours)

### For Autonomous Vehicle Teams

1. **Evaluation:** Use Alpamayo 1 on AlpaSim simulator
2. **Datasets:** Incorporate 1,700+ hours of driving data
3. **Fine-Tuning:** Customize chain-of-thought reasoning for specific OEM requirements
4. **Testing:** Run closed-loop validation before real-world trials

### For Enterprise AI

1. **Infrastructure:** Deploy on Vera Rubin platform
2. **Model Selection:** Choose from Clara (healthcare), Earth-2 (climate), or Nemotron (general AI)
3. **Inference Optimization:** Reduce token costs by 10x vs. previous systems
4. **Cost Management:** Open-source models eliminate per-call API fees

---

## Market Implications

### Industry Shifts

**1. Localized AI:** Models like Nemotron Speech ASR enable local deployment, reducing dependency on cloud APIs[1]

**2. Transparency in Safety-Critical Systems:** Alpamayo's reasoning approach sets new standards for explainable AI in autonomous vehicles[7]

**3. Robotics Acceleration:** Physical AI models and simulation tools lower barriers to robot development[2]

**4. Democratization:** Open-source models on Hugging Face enable every company to build AI systems[2]

### NVIDIA's Strategic Position

- **From Hardware Only** → **Full Stack AI Provider**
- **From Proprietary** → **Open Ecosystem**
- **From Consumer Focus (gaming)** → **Enterprise Focus (AI infrastructure)**
- **From Training-Centric** → **Training + Inference Optimization**

---

## Getting Started Resources

### Official Documentation

- **NVIDIA Blog:** https://blogs.nvidia.com/blog/open-models-data-tools-accelerate-ai/
- **Developer Documentation:** NVIDIA Developer portal
- **Hugging Face Hub:** All models available for download and experimentation

### Model Repositories

- **Nemotron Speech ASR:** `nvidia/nemotron-speech-streaming-en-0.6b`
- **Cosmos Models:** Hugging Face NVIDIA collection
- **Isaac GR00T:** Hugging Face robotics collection
- **Alpamayo:** NVIDIA Autonomous Driving Hub

### Community Resources

- **GitHub:** NVIDIA official repositories
- **Papers:** Technical whitepapers for each model family
- **Tutorials:** Video demonstrations and implementation guides

---

## Summary: Six Key Takeaways

1. **Nemotron Speech ASR:** 24ms latency streaming speech-to-text—fastest in industry, now available open-source for voice agents and transcription

2. **Alpamayo:** First open-source reasoning models for autonomous vehicles with explainable chain-of-thought logic, addressing the long-tail problem

3. **Cosmos:** Physical AI world models generating synthetic training data for robotics, reducing real-world data requirements

4. **Clara:** Healthcare-focused models accelerating drug discovery and medical treatment development

5. **Vera Rubin Platform:** 10x reduction in token generation costs, making large-scale AI deployment economically viable

6. **Open Ecosystem:** All 13 models available on Hugging Face with source code, enabling companies globally to build frontier AI systems

---

## References

[1] Witteveen, S. (2026, January 6). NVIDIA's new open models. YouTube. Retrieved from https://www.youtube.com/watch?v=JrCKb6gM9KM

[2] NVIDIA. (2026, January 5). NVIDIA Rubin Platform, open models, autonomous driving. Blog. Retrieved from https://blogs.nvidia.com/blog/2026-ces-special-presentation/

[3] NVIDIA. (2026, January 5). NVIDIA unveils new open models, data and tools to accelerate AI. Blog. Retrieved from https://blogs.nvidia.com/blog/open-models-data-tools-accelerate-ai/

[4] Hugging Face. (2026, January 5). Scaling real-time voice agents with cache-aware streaming ASR. Blog. Retrieved from https://huggingface.co/blog/nvidia/nemotron-speech-asr-scaling-voice-agents

[5] Daily.co. (2026, January 5). Building voice agents with NVIDIA open models. Blog. Retrieved from https://www.daily.co/blog/building-voice-agents-with-nvidia-open-models/

[6] NVIDIA. (2026, January 4). Alpamayo—Open models for autonomous vehicles. Developer documentation. Retrieved from https://www.nvidia.com/en-in/solutions/autonomous-vehicles/alpamayo/

[7] NVIDIA. (2026, January 4). Building autonomous vehicles that reason with NVIDIA Alpamayo. Developer Blog. Retrieved from https://developer.nvidia.com/blog/building-autonomous-vehicles-that-reason-with-nvidia-alpamayo/