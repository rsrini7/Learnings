# 🚀 Engineering & AI Knowledge Hub

*Curated and maintained by Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*

Welcome to the central repository for technical deep dives, architectural whitepapers, system design models, and empirical research notes across artificial intelligence, distributed systems, quantum computing, and modern software engineering.

---

## 🧭 Domain Hubs

Explore focused technical hubs with dedicated roadmaps, architecture diagrams, and complete categorized indexes:

| Domain | Hub | Scope / Focus | Articles |
|:---|:---|:---|:---:|
| 🧠 **AI & Machine Learning** | [AI-ML/README.md](AI-ML/README.md) | Autonomous agents, scalar autograd (microGPT), KV caching, prompt tokenomics, multimodal RAG, and MCP protocols. | 128 |
| ☁️ **Software Engineering** | [Engineering/README.md](Engineering/README.md) | High-scale systems (1M RPS), HTTP QUERY (RFC 10008), JVM internals (Babylon & Panama), and Kafka 4.0 KRaft. | 24 |
| ⛓️ **Blockchain & DLT** | [Blockchain/README.md](Blockchain/README.md) | Ethereum L1/L2, RWA tokenization rails (ERC-20/721/1400), Hardhat testnets, and macro crypto cycles. | 17 |
| ⚛️ **Quantum Computing** | [QuantumComputing/README.md](QuantumComputing/README.md) | Qubit state mechanics, Bloch sphere geometry, Google Willow benchmarks, and post-quantum cryptography. | 5 |
| 📄 **Research Papers** | [Papers/README.md](Papers/README.md) | DeepSeek-V3/R1 co-design (MLA, DualPipe), recursive reasoning models, and VL-JEPA vision. | 19 |
| 🛠️ **Development Setup** | [DevSetup/README.md](DevSetup/README.md) | Workstation environments, local model runners (llama.cpp), and Headroom / RTK multi-agent caching. | 8 |
| ✍️ **Content Creation** | [Content/README.md](Content/README.md) | Systematic LLM prompts for software development, technical diagramming, and concise writing. | 43 |
| 📰 **News & Updates** | [News/README.md](News/README.md) | In-depth security advisories (CVEs/RCEs), major cloud outage postmortems, and weekly industry briefings. | 64 |
| 📚 **References & Guides** | [References/README.md](References/README.md) | Gang of Four (GoF) design patterns, Passkeys / WebAuthn authentication, and paper discovery guides. | 3 |

> 📖 **Prefer a single-page list for searching?**  
> Open the **[Complete Repository Index (INDEX.md)](INDEX.md)** to browse or search (`Ctrl+F` / `Cmd+F`) all 311 articles across all domains.

---

## 🌟 Curated Starting Points

Representative, high-depth architectural investigations and verified implementations to start with:

1. [microGPT: Scalar Autograd Engine & Transformer Architecture](AI-ML/LLMs/architecture/microGPT-Technical-Deep-Dive.md)  
   *Algorithmic walkthrough of pure-Python scalar autograd, multi-head causal attention, and complete 240-line GPT architecture.*
2. [OpenClaw / Moltbot: Autonomous Agent Security Analysis](AI-ML/Agents/openclaw/OpenClaw-Moltbot-Security-Analysis-2026.md)  
   *Comprehensive threat modeling, Shodan discovery data, and execution-node hardening for local-first autonomous agents.*
3. [HTTP QUERY Method (RFC 10008)](Engineering/Architecture/HTTP-QUERY-Method-RFC-10008-Nov-2026.md)  
   *IETF RFC 10008 analysis: safe request-body queries, idempotent semantic caching, and Gateway/WAF configuration.*
4. [Java Next-Gen Programming Models: Babylon & Panama](Engineering/JVM/Java-Next-Gen-Programming-Models-Babylon-Panama-Nov-2026.md)  
   *Deep dive into OpenJDK Project Babylon (Code Reflection / Code Models) and Project Panama (Foreign Function & Memory API).*
5. [Kafka 4.0: KRaft Consensus Architecture & Migration](Engineering/Middleware/Kafka-4.0-KRaft-Architecture-And-Migration-2026.md)  
   *Complete removal of ZooKeeper, Raft-based metadata quorum dynamics, and zero-downtime cluster cutover guide.*
6. [The Crypto Supercycle & Ethereum Tokenization](Blockchain/ethereum/Crypto-Supercycle-and-Ethereum.md)  
   *Real-world asset (RWA) tokenization mechanics, institutional settlement rails, and four-year cycle breakdown.*
7. [Quantum Computing Foundations & State Mechanics](QuantumComputing/Quantum-Computing-Foundations-And-State-Mechanics-2026.md)  
   *Qubit state vectors, superposition, Bloch sphere geometry, unitary quantum gates, and post-quantum threat analysis.*
8. [eMudhra Weak CA Keys & PKI Trust Infrastructure](News/Security/EMudhra-Weak-CA-Keys-And-PKI-Trust-Oct-2026.md)  
   *Cryptographic root failure analysis of public CA key generation, certificate revocation, and global browser trust.*
9. [DeepSeek-V3: Architecture & Hardware/Software Co-Design](Papers/deepseek/DeepSeek-V3-Architecture-And-Hardware-Software-CoDesign-2026.md)  
   *Multi-head Latent Attention (MLA), DeepSeekMoE auxiliary-loss-free routing, DualPipe pipelining, and FP8 mixed precision.*

---

## 📁 Repository Structure

```
Learnings/
├── AI-ML/                       # AI & Machine Learning (128 articles)
│   ├── Agents/                  # Agent frameworks, skills, MCP
│   ├── LLMs/                    # Models, architectures, inference
│   ├── RAG/                     # RAG architectures & guides
│   ├── Hardware/                # AI chips, accelerators, silicon
│   ├── Protocols/               # MCP, A2A, UCP
│   ├── Fine-Tuning/             # PEFT, training guides
│   ├── Comparisons/             # Model & tool comparisons
│   ├── Tabular-ML/              # Tabular / structured-data models
│   └── Algorithms/              # Recommendation algorithms
│
├── Engineering/                 # Software Engineering (24 articles)
│   ├── Architecture/            # System design, scaling, RFCs
│   ├── JVM/                     # Java, Panama, Babylon, JDWP
│   ├── Databases/               # Graph DB, PostgreSQL
│   ├── Middleware/              # Kafka KRaft, workflows
│   ├── Cloud/                   # AWS, Hetzner, cloud services
│   └── Languages/               # Rust, Go, TypeScript, WASM
│
├── Blockchain/                  # Blockchain & DLT (17 articles)
│   ├── ethereum/                # Hardhat, EVM, L1/L2
│   ├── crypto/                  # Tokens, ISO 20022, Stablecoins
│   ├── enterprise/              # Institutional tokenization, RWAs
│   ├── development/             # Hedera, payment rails
│   └── reference/               # Ecosystem guides, taxonomies
│
├── QuantumComputing/            # Quantum computing & state mechanics (5 articles)
├── DevSetup/                    # Workstation & AI developer tooling (8 articles)
├── Papers/                      # Research papers & critical reviews (19 articles)
├── Content/                     # Structured prompts & technical writing (43 articles)
├── News/                        # Security advisories, outages & weekly updates (64 articles)
├── References/                  # Quick references, GoF, Passkeys (3 articles)
├── Scripts/                     # Utility scripts & verification tools
└── assets/                      # Shared styling & chart libraries
```

---

## 🔧 Utility & Verification Scripts

- [GitHub Repos & Links](Scripts/github-repos.py) — Manage repo links, check broken references (`links`), and repair TOCs.
- [Markdown & Diagram Validator](Scripts/check-markdown.py) — Lints Mermaid diagrams, KaTeX math blocks, and SVG container overflows.
- [SVG Infographic Validator](Scripts/check-svg.py) — Validates SVG XML syntax, text bounds, and responsive viewBox integrity.
- [Hub & README Generator](Scripts/generate-readme.py) — Auto-generates root `README.md`, domain hub `README.md`s, and `INDEX.md`.

---

> **Last updated:** November 2026
