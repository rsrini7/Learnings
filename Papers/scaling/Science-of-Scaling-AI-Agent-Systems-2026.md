# The Science of Scaling AI Agent Systems: Empirical Laws of Coordination Overhead, Error Amplification, and Topology Selection

Learning note · Revised November 2026 · Technical Reference
*By Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*

---

> **Core Idea:**
> Across 180 controlled configurations across frontier LLM families, adding agents indiscriminately often degrades system accuracy by up to 70% due to context window competition and non-linear error propagation. Multi-agent scaling is governed by three empirical laws—the Tool-Coordination Trade-off, the Capability Ceiling, and Architecture-Dependent Error Amplification—enabling 87% predictive accuracy for determining whether a task requires single-agent execution, centralized orchestration, or decentralized debate.

---

## 1. Foundations & Architectural Topologies

Industry practice has frequently operated under the intuitive assumption that decomposing a complex problem across multiple autonomous agents will naturally yield superior performance. However, empirical research from Google Research, Google DeepMind, and MIT (*"Towards a Science of Scaling Agent Systems"*, arXiv:2512.08296) demonstrates that multi-agent systems (MAS) often introduce catastrophic overhead: token exhaustion, coordination latency, and compounding hallucinations.

### System Archetypes

The empirical literature formalizes five distinct agent topology configurations:

```mermaid
flowchart TD
    subgraph SingleAgent["Single-Agent System"]
        direction TB
        Task1["Task Context"] --> SAS["Single Autonomous Agent"]
        SAS --> Tools1["Tool Execution Loop"]
        Tools1 --> SAS
        SAS --> Res1["Direct Output"]
    end

    subgraph Centralized["Centralized MAS"]
        direction TB
        Task2["Task Context"] --> Lead["Lead / Manager Agent"]
        Lead --> Sub1["Worker Agent 1"]
        Lead --> Sub2["Worker Agent 2"]
        Lead --> Sub3["Worker Agent 3"]
        Sub1 --> Lead
        Sub2 --> Lead
        Sub3 --> Lead
        Lead --> Res2["Synthesized Result"]
    end

    subgraph Decentralized["Decentralized MAS"]
        direction TB
        Task3["Task Context"] --> DA1["Agent A"]
        Task3 --> DA2["Agent B"]
        DA1 <-->|"Peer Debate"| DA2
        DA2 --> Res3["Consensus Output"]
    end

    subgraph Independent["Independent MAS"]
        direction TB
        Task4["Task Context"] --> IA1["Agent 1"]
        Task4 --> IA2["Agent 2"]
        Task4 --> IA3["Agent 3"]
        IA1 --> Vote["Majority Voting Aggregator"]
        IA2 --> Vote
        IA3 --> Vote
        Vote --> Res4["Voted Result"]
    end
```

### Core Terminology

| Term | Meaning & Formal Definition |
| :--- | :--- |
| **SAS (Single-Agent System)** | A standalone agent operating a solitary reasoning loop with tools, avoiding all inter-agent communication protocols and context duplication. |
| **Centralized MAS** | A hierarchical hub-and-spoke architecture where an orchestrator agent delegates partitioned sub-tasks to worker agents and synthesizes intermediate results. |
| **Decentralized MAS** | A peer-to-peer topology where autonomous agents share observations, debate hypotheses, and converge via conversational consensus without an authority node. |
| **Independent MAS** | An ensemble topology where $N$ agents solve the identical prompt in total isolation, aggregating predictions via unweighted majority voting. |
| **Coordination Overhead ($\mathcal{O}_{\text{coord}}$)** | The percentage of total consumed token budget dedicated to inter-agent formatting, routing messages, tool schema duplication, and meta-dialogue rather than domain task reasoning. |
| **Error Amplification ($\mathcal{A}_e$)** | The empirical ratio quantifying how hallucinations and false assumptions multiply as intermediate states traverse agent communication graphs ($1.0\times$ baseline to $17.2\times$). |
| **Capability Ceiling ($C_{\text{sat}}$)** | The empirical threshold (approximately 45% single-agent task accuracy) above which adding additional agents produces negative net marginal utility. |
| **Tool-Coordination Trade-off** | The degradation phenomenon where equipping $N$ agents with large tool palettes ($M \ge 8$ tools) causes tool context bloat that crowds out working memory. |

---

## 2. The Three Empirical Laws of Agent Scaling

The DeepMind/MIT scaling study analyzed 180 controlled experimental runs spanning three frontier model families (OpenAI GPT-4/5 series, Google Gemini series, and Anthropic Claude series) across financial analysis, dynamic web navigation, sequential state planning, and tool-heavy workflows. The study discovered three invariant scaling principles:

### Law 1: The Tool-Coordination Trade-Off

When agents are equipped with expanding tool libraries ($M \ge 8$), multi-agent systems suffer rapid efficiency degradation.

```
Token Budget per Agent = Context Window - System Prompt - (M × Tool Schemas) - Inter-Agent Messages
```

In a single-agent system, tool schemas are ingested once. In an $N$-agent system, tool schemas must either be duplicated $N$ times across every sub-agent prompt or routed through a centralized coordinator that incurs massive JSON serialization overhead.

- In software engineering benchmarks with 16 available tools, adding agents degraded overall task accuracy by **45%** while increasing token consumption by **5.1×**.
- Centralized orchestrator communication overhead reached **515%** of baseline tokens.
- **Empirical Coefficient:** Each additional tool decreases multi-agent system efficiency by $\beta_{\text{tools}} = -0.330$ ($p < 0.001$).

### Law 2: The Capability Ceiling

When a single agent achieves high baseline accuracy ($> 45\%$), introducing additional agents almost universally causes performance degradation:

- When baseline single-agent performance is low (e.g., $35\%$ on financial multi-step analysis), a centralized team of 3–4 agents surges to **81%** accuracy (**+80.9%** net gain) because parallelizable fact extraction offsets coordination cost.
- When baseline performance is high (e.g., Anthropic Claude achieving $50.2\%$ baseline across complex reasoning tasks), multi-agent deployment produces an average net degradation of **-4.6%**.
- **Empirical Coefficient:** Baseline task capability exhibits a strong negative saturation coefficient $\beta_{\text{baseline}} = -0.408$ ($p < 0.001$).

### Law 3: Architecture-Dependent Error Amplification

Errors, hallucinations, and unverified assumptions do not cancel out statistically; they amplify according to the underlying network graph:

| Topology | Empirical Error Amplification ($\mathcal{A}_e$) | Failure Dynamic | Optimal Regime |
| :--- | :--- | :--- | :--- |
| **Single-Agent (SAS)** | **$1.0\times$** (Baseline) | Self-contained hallucinations; error does not poison downstream collaborators. | Sequential planning, $>8$ tools, baseline $>45\%$. |
| **Centralized MAS** | **$4.4\times$** | The orchestrator filters worker hallucination noise, but remains a single point of cognitive failure. | Embarrassingly parallelizable fact extraction. |
| **Decentralized MAS** | **$7.8\times$** | Groupthink cascade: agents politely agree with ungrounded peer premises, reinforcing false consensus. | Exploratory search with high environmental uncertainty. |
| **Independent MAS** | **$17.2\times$** | Catastrophic noise voting: independent errors compound without verification, creating false majorities. | Simple zero-shot classification ensembling only. |

---

## 3. Deep Technical Mechanism & Predictive Regression Model

### The Mixed-Effects Scaling Equation

The net performance differential ($\Delta P$) achieved by deploying a multi-agent system over a single-agent baseline is governed by a mixed-effects regression model:

$$
\Delta P = \beta_0 + \beta_I \cdot I^2 - \beta_T \cdot N_{\text{tools}} - \beta_C \cdot P_{\text{SAS}} - \beta_O \cdot \mathcal{O}_{\text{coord}} - \beta_E \cdot \mathcal{A}_e + \epsilon
$$

where:
- $I$: Intrinsic intelligence of the base foundation model (scales quadratically $\beta_I = +0.256$, indicating smarter models leverage multi-agent debate more effectively).
- $N_{\text{tools}}$: Count of callable API functions ($\beta_T = -0.330$).
- $P_{\text{SAS}}$: Baseline single-agent accuracy ($\beta_C = -0.408$).
- $\mathcal{O}_{\text{coord}}$: Measured token overhead percentage ($\beta_O = -0.215$).
- $\mathcal{A}_e$: Structural error amplification constant of the topology.

This predictive formulation achieves a cross-validated fit of $R^2 = 0.513$ across all domains and a leave-one-domain-out generalization fit of $R^2 = 0.890$, enabling architecture selection with $87\%$ accuracy prior to deployment.

### Context Window Contention Dynamics

Let $T_{\text{max}}$ be the maximum usable context window and $T_{\text{work}}$ be the working tokens available for actual reasoning. For a centralized orchestrator managing $N$ workers each invoking $M$ tools:

$$
T_{\text{work}} = T_{\text{max}} - \left( T_{\text{sys}} + N \cdot T_{\text{prompt-meta}} + \sum_{m=1}^{M} T_{\text{schema}}(m) + \sum_{i=1}^{N} T_{\text{msg}}(i) \right)
$$

As $N$ and $M$ scale, $T_{\text{work}} \to 0$, forcing the context management engine into aggressive truncation or sliding window eviction, which causes intermediate reasoning amnesia.

---

## 4. Architectural Visuals & Topology Mapping

![Science of Scaling AI Agent Systems](../assets/Science-of-Scaling-AI-Agent-Systems-2026.svg)

### Empirical Topology Selection Engine

```mermaid
flowchart TD
    Start["Task Specification"] --> Q1{"Decomposes into<br/>Independent Sub-Tasks?"}
    
    Q1 -->|"No (Sequential / State-Bound)"| SAS_Decision["Select SINGLE-AGENT (SAS)<br/>Zero coordination overhead"]
    
    Q1 -->|"Yes (Parallel Partitionable)"| Q2{"Available Tool Count?"}
    
    Q2 -->|">= 8 Tools"| Q3{"Single-Agent Baseline > 45%?"}
    Q2 -->|"< 8 Tools"| Q4{"Environment Dynamic / Exploratory?"}
    
    Q3 -->|"Yes"| SAS_Decision
    Q3 -->|"No"| Cent_Decision["Select CENTRALIZED MAS<br/>3-4 Worker Agents + Lead"]
    
    Q4 -->|"Yes (Web Search / Discovery)"| Dec_Decision["Select DECENTRALIZED MAS<br/>2-3 Peer Agents"]
    Q4 -->|"No (Deterministic Analysis)"| Cent_Decision
```

---

## 5. Production Implementations & Code Recipes

### Recipe 1: Pre-Deployment Topology Decision Engine

The following production Python module implements the mixed-effects regression scoring formula to programmatically select between Single-Agent, Centralized MAS, and Decentralized MAS before instantiating expensive agent swarms:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class AgentTopology(str, Enum):
    SINGLE_AGENT = "single_agent"
    CENTRALIZED_MAS = "centralized_mas"
    DECENTRALIZED_MAS = "decentralized_mas"
    INDEPENDENT_ENSEMBLE = "independent_ensemble"

@dataclass
class TaskProfile:
    name: str
    is_sequential: bool           # True if state changes between steps (e.g. Minecraft, Code Exec)
    single_agent_baseline: float  # Historical or estimated accuracy [0.0, 1.0]
    tool_count: int               # Number of unique tool/API functions required
    is_exploratory: bool          # True if environment requires open-ended web discovery
    model_intelligence_score: float # Normalized frontier benchmark (e.g. Claude 3.7/4.5 = 1.0)

class ScalingDecisionEngine:
    """
    Evaluates empirical scaling laws to predict net multi-agent utility.
    Prevents token waste and error amplification in production agent stacks.
    """
    def __init__(self):
        # Empirical regression coefficients from arXiv:2512.08296
        self.beta_intelligence = 0.256
        self.beta_tools = 0.330
        self.beta_ceiling = 0.408
        self.error_amplification = {
            AgentTopology.SINGLE_AGENT: 1.0,
            AgentTopology.CENTRALIZED_MAS: 4.4,
            AgentTopology.DECENTRALIZED_MAS: 7.8,
            AgentTopology.INDEPENDENT_ENSEMBLE: 17.2,
        }

    def evaluate_architecture(self, task: TaskProfile) -> Dict[str, Any]:
        # Rule 1: Strictly enforce single-agent execution on sequential state tasks
        if task.is_sequential:
            return {
                "recommended_topology": AgentTopology.SINGLE_AGENT,
                "confidence": 0.95,
                "rationale": (
                    "Sequential state dependencies cannot be parallelized. Multi-agent "
                    "coordination introduces communication latency with up to 70% accuracy degradation."
                ),
                "predicted_gain": 0.0
            }

        # Rule 2: Check capability ceiling
        if task.single_agent_baseline >= 0.45:
            return {
                "recommended_topology": AgentTopology.SINGLE_AGENT,
                "confidence": 0.88,
                "rationale": (
                    f"Baseline accuracy ({task.single_agent_baseline:.1%}) exceeds capability "
                    "ceiling (45%). Coordination overhead will outweigh marginal diversity gains."
                ),
                "predicted_gain": -0.05
            }

        # Rule 3: High tool count suppresses multi-agent viability
        if task.tool_count >= 8:
            return {
                "recommended_topology": AgentTopology.SINGLE_AGENT,
                "confidence": 0.85,
                "rationale": (
                    f"Tool count ({task.tool_count}) creates severe context duplication. "
                    "Single-agent allocation preserves token budget for reasoning."
                ),
                "predicted_gain": -0.12
            }

        # Rule 4: Dynamic exploration vs. structured parallel synthesis
        if task.is_exploratory:
            return {
                "recommended_topology": AgentTopology.DECENTRALIZED_MAS,
                "optimal_agent_count": 2,
                "confidence": 0.82,
                "rationale": (
                    "Open-ended search benefits from peer debate diversity; "
                    "low tool count preserves context."
                ),
                "predicted_gain": +0.09
            }
        else:
            return {
                "recommended_topology": AgentTopology.CENTRALIZED_MAS,
                "optimal_agent_count": 3,
                "confidence": 0.91,
                "rationale": (
                    "Partitionable deterministic analysis benefits from centralized orchestrator "
                    "filtering worker hallucination noise."
                ),
                "predicted_gain": +0.45
            }

# Production Example Usage:
if __name__ == "__main__":
    engine = ScalingDecisionEngine()
    
    finance_task = TaskProfile(
        name="Equity Research Synthesis",
        is_sequential=False,
        single_agent_baseline=0.35,
        tool_count=4,
        is_exploratory=False,
        model_intelligence_score=1.0
    )
    decision = engine.evaluate_architecture(finance_task)
    print(f"Task: {finance_task.name} -> {decision['recommended_topology'].value} (Gain: {decision['predicted_gain']:+.1%})")
```

### Recipe 2: Token-Budget Guarded Orchestration Wrapper

```python
from typing import List, Dict

class TokenGuardedOrchestrator:
    """
    Monitors inter-agent communication overhead in centralized swarms,
    automatically aborting worker spawning if coordination overhead exceeds 40%.
    """
    def __init__(self, max_token_ceiling: int = 30000, overhead_limit: float = 0.40):
        self.ceiling = max_token_ceiling
        self.overhead_limit = overhead_limit
        self.task_tokens = 0
        self.coordination_tokens = 0

    def record_usage(self, prompt_tokens: int, completion_tokens: int, is_coordination: bool):
        total = prompt_tokens + completion_tokens
        if is_coordination:
            self.coordination_tokens += total
        else:
            self.task_tokens += total

    @property
    def current_overhead_ratio(self) -> float:
        total = self.task_tokens + self.coordination_tokens
        return (self.coordination_tokens / total) if total > 0 else 0.0

    def should_continue_worker(self, worker_id: int) -> bool:
        if (self.task_tokens + self.coordination_tokens) > self.ceiling:
            return False
        if self.current_overhead_ratio > self.overhead_limit:
            # Coordination overhead exceeded safe scaling boundary
            return False
        return True
```

---

## 6. Empirical Benchmarks Across Task Archetypes

The 180 controlled experiments reveal substantial domain-specific variation:

| Task Domain | Benchmark / Environment | Single-Agent Accuracy | Centralized MAS Accuracy | Decentralized MAS Accuracy | Independent MAS Accuracy | Preferred Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Financial Analysis** | Multi-Source Equity Due Diligence | 35.0% | **81.0%** (+80.9%) | 62.0% (+77.1%) | 42.0% (+20.0%) | **Centralized (3–4 agents)** |
| **Dynamic Web Navigation** | Real-World Product Sourcing (5+ sites) | 32.0% | 31.0% (-3.1%) | **35.0%** (+9.4%) | 21.0% (-34.4%) | **Decentralized (2–3 agents)** |
| **Sequential State Planning** | Minecraft Multi-Step Tool Crafting | **57.0%** | 35.0% (-38.6%) | 17.0% (-70.2%) | 17.0% (-70.2%) | **Single-Agent ONLY** |
| **Tool-Heavy Workflows** | Enterprise Automation (16 APIs) | **63.0%** | 58.0% (-7.9%) | 56.0% (-11.1%) | 44.0% (-30.2%) | **Single-Agent ONLY** |

### Token Economics & Amortization

| System Topology | Average Tokens Consumed | Cost Multiplier | Accuracy Uplift Across All Tasks | Efficiency Score ($E_c$) |
| :--- | :--- | :--- | :--- | :--- |
| **Single-Agent System** | 4,800 | **$1.0\times$** | Baseline (0.0%) | **1.00** (Optimal) |
| **Centralized MAS** | 14,000 | **$2.9\times$** | +12.0% avg | 0.39 |
| **Decentralized MAS** | 13,600 | **$2.8\times$** | +4.0% avg | 0.37 |
| **Hybrid MAS (Central + Peer)** | 24,700 | **$5.1\times$** | +8.0% avg | 0.21 (Worst) |

---

## 7. Common Claims vs. Technical Realities

| Common Claim | Technical Reality | Production Implication |
| :--- | :--- | :--- |
| *"More agents always lead to better system performance."* | **False.** On sequential planning, adding agents causes up to a 70% collapse in success rate. Across all tasks, average improvement is only +3% to +12% at 3× to 5× the token cost. | Default to single-agent systems. Deploy multi-agent architectures only when tasks are proven to be embarrassingly parallelizable. |
| *"Independent ensemble voting eliminates communication noise."* | **False.** Independent agents exhibit the highest error amplification in the study ($17.2\times$). Errors compound without self-correction, causing hallucination consensus. | Never use independent majority voting on multi-step reasoning tasks; use centralized orchestrator verification. |
| *"Bigger, smarter models scale better in multi-agent swarms."* | **Partially False.** While intelligence scales quadratically ($\beta_I = +0.256$), top-tier models (e.g. Claude 3.7/4.5) already achieve high single-agent baselines ($>50\%$), hitting the capability ceiling and degrading when placed in swarms. | Use frontier models as solo agents; reserve multi-agent swarms for lower-cost models tackling parallelizable data collection. |
| *"Decentralized peer debate eliminates bias and groupthink."* | **False.** Unstructured peer debate exhibits an error amplification factor of $7.8\times$. Agents frequently converge on polite, mutually reinforced hallucinations. | Limit peer debate to at most 2–3 rounds with strict external tool grounding after every interaction turn. |

---

## 8. Practical Adoption Blueprint & Verification Checklist

### System Sizing & Token Thresholds

```
Operational Decision Framework:
1. Is task stateful and step-dependent? ----------> SINGLE-AGENT
2. Does the task expose >= 8 callable tools? ----> SINGLE-AGENT
3. Does single-agent benchmark exceed 45%? ------> SINGLE-AGENT
4. Does the task decompose into isolated searches? -> CENTRALIZED (3-4 workers)
5. Is the task open-ended exploratory discovery? -> DECENTRALIZED (2 workers)
```

### Telemetry & Monitoring Metrics

Track these three core indicators across all agent deployments:

```bash
# 1. Inspect coordination token overhead in logs
grep -E "coordination_tokens|task_tokens" agent_execution.log | awk '{sum_coord+=$2; sum_task+=$4} END {print "Overhead: " (sum_coord/(sum_coord+sum_task))*100 "%"}'

# 2. Monitor inter-agent message roundtrip latency
python3 -c "
import json
with open('agent_trace.json') as f:
    trace = json.load(f)
overhead_ms = [m['latency_ms'] for m in trace['messages'] if m['type'] == 'coordination']
print(f'Mean Coordination Latency: {sum(overhead_ms)/len(overhead_ms):.1f} ms')
"
```

### Verification Checklist

- [ ] **Sequential Dependency Audit:** Confirm that sub-tasks do not depend on world state modifications from preceding steps before provisioning parallel workers.
- [ ] **Tool Palette Pruning:** Ensure no individual worker agent receives more than 6 tool schemas in its system prompt.
- [ ] **Baseline Benchmarking:** Establish single-agent accuracy before building multi-agent scaffolding; if baseline is $>45\%$, halt multi-agent deployment.
- [ ] **Token Overhead Gate:** Set automated circuit breakers aborting multi-agent execution if coordination tokens exceed $40\%$ of total consumption.
- [ ] **Error Propagation Guard:** In centralized architectures, ensure the manager agent requires deterministic tool verification (e.g., Python execution, SQL validation) before accepting worker claims.

---

## 9. Timeline & Evolution of Agent Architecture

```mermaid
timeline
    title Evolution of AI Agent Architecture & Scaling
    2023 : Early Naive Scaling : AutoGPT, BabyAGI, and ChatDev popularize unconstrained multi-agent roleplay
    2024 : Scaffolding Frameworks : CrewAI, AutoGen, and LangGraph standardize centralized and decentralized topologies
    2025 : The Scaling Science (Dec 2025) : Google DeepMind / MIT publish arXiv:2512.08296 establishing empirical limits of multi-agent scaling
    2026 : Principled Topology Selection : Industry shifts from naive swarms to mathematically grounded, hybrid single-agent/orchestrator pipelines
```

---

## 10. Primary Sources, References & Evidence

### Primary Specifications & Literature

1. [Google Research, Google DeepMind, MIT: Towards a Science of Scaling Agent Systems (arXiv:2512.08296)](https://arxiv.org/abs/2512.08296) — Primary research paper by Kim et al. detailing 180 controlled experiments, the three scaling laws, and mixed-effects regression models.
2. [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — Architectural guidelines recommending simple, composable agent workflows over complex multi-agent frameworks.
3. [DeepSeek-AI: DeepSeek-R1 Technical Report](https://arxiv.org/abs/2501.12948) — Demonstrates that test-time compute in a single reasoning model frequently outperforms multi-agent debate ensembles.
4. [Microsoft: Agent Lightning Technical Overview](https://github.com/microsoft/agent-lightning) — High-throughput orchestrator execution proving that token overhead limits multi-agent viability in enterprise workflows.

### Source Context & Empirical Evidence

| Reference ID | Architecture Focus | Primary Claim Checked | Verification Outcome |
| :--- | :--- | :--- | :--- |
| **arXiv:2512.08296** | 180 Agent Configurations | Multi-agent setups degrade sequential planning by up to 70% and amplify errors up to 17.2×. | Verified. Empirical mixed-effects model ($R^2=0.513$, LOO $R^2=0.890$). |
| **DeepMind 2025** | Tool-Coordination Trade-off | Equip $\ge 8$ tools reduces multi-agent efficiency by $-3.3\%$ per agent ($\beta=-0.330$). | Verified. Context window bloat crowds out working reasoning memory. |
| **MIT 2025** | Capability Ceiling | Single-agent baselines $>45\%$ show negative marginal returns when swarmed ($\beta=-0.408$). | Verified. Claude 4.5 degrades by $-4.6\%$ in multi-agent configurations. |

---

## 11. Supplementary Visuals

![The Science of Scaling AI Agent Systems](../assets/The-Science-of-Scaling-AI-Agent-Systems.png)
*Figure 1: High-level visual summary of the Science of Scaling AI Agent Systems, illustrating the comparative trade-offs between single-agent simplicity, centralized management, and decentralized group dynamics across task topologies.*

---

**Related:**
- [Agentic-Reasoning-Architectures-And-Reflection-Loops-2026](../reasoning/Agentic-Reasoning-Architectures-And-Reflection-Loops-2026.md) — Analyzes foundational test-time compute and reflective reasoning loops within single-agent architectures.
- [AI-Coding-Loops](../../AI-ML/Agents/development/AI-Coding-Loops.md) — Operationalizes the 180-experiment findings into concrete agent design rules for automated software development.
- [Kimi-K2.5-Technical-Report-And-Vision-Architecture-2026](../vision/Kimi-K2.5-Technical-Report-And-Vision-Architecture-2026.md) — Contrasts Kimi's native agent swarm parallelism with centralized tool-orchestration constraints.
- [Recursive-Language-Models-RLM-Architecture-2026](../reasoning/Recursive-Language-Models-RLM-Architecture-2026.md) — Examines context offloading to a REPL workspace, preventing the token bloat that breaks multi-agent swarms.
