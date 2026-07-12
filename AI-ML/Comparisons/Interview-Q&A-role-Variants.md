# 1️⃣ Senior Engineer — *“Can build, debug, and operate”*

**Expectation:**
Hands-on ownership of **production AI components**, latency, failures, and on-call reality.

### Core Focus Areas

* Inference performance
* Model integration
* Debugging under SLAs
* Monitoring & rollback
* Payments / regulated constraints awareness

---

## Senior Engineer: Top Questions + Probing Follow-ups

### 1. Inference & Latency

**Q:** What are the main contributors to inference latency in production?
**Good answer:** Model size, batching, serialization, cold start, tokenization, network hops.

**Probe:**

* *Which one usually dominates p99 latency in your experience?*
* *How would you prove it in prod, not in theory?*

---

### 2. Vanishing / Exploding Gradients

**Q:** Why do gradients vanish, and how do modern models mitigate it?
**Good answer:** Depth causes gradient shrinkage; mitigated via residuals, normalization, better initialization.

**Probe:**

* *How would you detect this issue from training logs alone?*
* *What metric degrades first?*

---

### 3. Model Rollout Safety

**Q:** How do you deploy a new model without risking payment failures?
**Good answer:** Shadow mode → canary → rollback hooks → SLO monitoring.

**Probe:**

* *What signal tells you to roll back automatically?*
* *What if business metrics lag behind technical metrics?*

---

### 4. False Positives vs False Negatives

**Q:** Why are false positives dangerous in payments?
**Good answer:** They block legitimate transactions → revenue + trust loss.

**Probe:**

* *Who decides the tradeoff — engineering or risk?*
* *How do you encode that decision in the model?*

---

### 5. Explainability

**Q:** How do you explain a declined transaction to audit?
**Good answer:** Feature attribution + rule context + stored model version.

**Probe:**

* *Where is this stored, and for how long?*
* *What breaks if you don’t store raw features?*

---

### 6. Production Incidents

**Q:** Walk me through a model-related incident you handled.
**Good answer:** Detect → isolate → rollback → fix → postmortem.

**Probe:**

* *What would you do differently next time?*
* *Which metric caught it first?*

---

### 7. Vendor Models

**Q:** Would you use a black-box vendor model in payments?
**Good answer:** Only with strong SLAs, shadow testing, limited scope.

**Probe:**

* *What’s the worst-case failure mode?*
* *How do you exit the vendor if needed?*

---

### 8. Monitoring

**Q:** What do you monitor for a fraud model in prod?
**Good answer:** Latency, score drift, FP/FN, volume anomalies.

**Probe:**

* *Which alert would wake you at 2am?*
* *Which ones are informational only?*

---

### 9. Human-in-the-Loop

**Q:** Where should humans intervene in payments AI?
**Good answer:** Reviews, disputes, escalations — not auth path.

**Probe:**

* *What happens if humans become the bottleneck?*

---

### 10. Security & PII

**Q:** How do you protect sensitive data during inference?
**Good answer:** Masking, encryption, least privilege, tokenization.

**Probe:**

* *What data should never reach the model at all?*

---

**Senior Engineer red flag 🚩**
Uses buzzwords but can’t explain **what breaks first in prod**.

---

# 2️⃣ Staff Engineer / Architect — *“Designs systems that survive audits”*

**Expectation:**
Owns **end-to-end architecture**, cross-team decisions, and long-term risk.

### Core Focus Areas

* System boundaries
* Governance & compliance
* Blast-radius control
* Cost & scalability
* Org-level standards

---

## Staff / Architect: Top Questions + Probing Follow-ups

### 1. Architecture Boundaries

**Q:** Why separate model decision from payment execution?
**Good answer:** Limits blast radius, enables audit and rollback.

**Probe:**

* *What failure does this separation prevent?*
* *Where have you seen this violated?*

---

### 2. Python vs Java Split

**Q:** Why use Python for models and Java for orchestration?
**Good answer:** Python for ML velocity; Java for reliability, governance.

**Probe:**

* *What happens if this boundary is ignored?*

---

### 3. AI Gateway

**Q:** Why centralize model access behind a gateway?
**Good answer:** Cost control, policy enforcement, observability.

**Probe:**

* *What breaks if teams call models directly?*

---

### 4. Regulatory Readiness

**Q:** How do you design for future audits?
**Good answer:** Immutable logs, versioned models, replayable decisions.

**Probe:**

* *How would you answer an audit 18 months later?*

---

### 5. Cost Governance

**Q:** How do you prevent AI cost explosions?
**Good answer:** Budgets, quotas, batching, model tiering.

**Probe:**

* *Who owns the AI bill in your org?*

---

### 6. Drift Strategy

**Q:** What’s your response to detected drift?
**Good answer:** Alert → shadow retrain → evaluate → controlled rollout.

**Probe:**

* *When do you retrain vs adjust thresholds?*

---

### 7. Agent Usage

**Q:** Where do agents belong in payments?
**Good answer:** Ops, investigations, compliance — never auth.

**Probe:**

* *What’s the blast radius of a bad agent?*

---

### 8. Org Enablement

**Q:** How do you raise AI maturity across teams?
**Good answer:** Shared platforms, standards, review gates.

**Probe:**

* *How do you stop “rogue AI” projects?*

---

### 9. Vendor Risk

**Q:** How do you assess AI vendor risk?
**Good answer:** Explainability limits, exit strategy, data control.

**Probe:**

* *What’s your de-risking plan if vendor shuts down?*

---

### 10. MD Conversation

**Q:** How do you justify AI investment to leadership?
**Good answer:** Reduced fraud loss, fewer incidents, audit safety.

**Probe:**

* *What metric would make an MD stop funding you?*

---

**Staff/Architect red flag 🚩**
Can design diagrams but can’t explain **failure containment**.

---

# 3️⃣ ML Researcher — *“Understands theory AND its limits”*

**Expectation:**
Knows **why models behave the way they do** and how theory degrades in real data.

### Core Focus Areas

* Optimization theory
* Generalization
* Evaluation rigor
* Failure modes
* Translating research → prod

---

## ML Researcher: Top Questions + Probing Follow-ups

### 1. Optimization

**Q:** Why do Transformers train stably at scale?
**Good answer:** Residuals, normalization, attention structure.

**Probe:**

* *What happens when these assumptions fail?*

---

### 2. Loss Functions

**Q:** Why accuracy is a poor metric for fraud?
**Good answer:** Class imbalance + asymmetric costs.

**Probe:**

* *What loss would you propose instead?*

---

### 3. Generalization

**Q:** How do you detect overfitting in time-series payments data?
**Good answer:** Temporal validation, stability checks.

**Probe:**

* *Why does random split fail here?*

---

### 4. Drift

**Q:** Is drift a data problem or a model problem?
**Good answer:** Both — behavior changes break assumptions.

**Probe:**

* *Which drift is harder: covariate or label drift?*

---

### 5. Explainability

**Q:** What are the limits of SHAP/LIME?
**Good answer:** Local approximations, instability, correlation issues.

**Probe:**

* *When can explanations be misleading?*

---

### 6. Robustness

**Q:** How do adversarial patterns show up in payments?
**Good answer:** Fraudsters adapt to model signals.

**Probe:**

* *How do you defend against adaptive adversaries?*

---

### 7. Model Choice

**Q:** Why might you prefer a simpler model in prod?
**Good answer:** Stability, interpretability, latency.

**Probe:**

* *How do you quantify “simpler but safer”?*

---

### 8. Research → Prod Gap

**Q:** Why do research gains fail in production?
**Good answer:** Data shift, infra constraints, human behavior.

**Probe:**

* *What research signal correlates best with prod success?*

---

### 9. Evaluation

**Q:** How do you evaluate models without labels?
**Good answer:** Proxy metrics, drift signals, human review sampling.

**Probe:**

* *What’s the risk of proxy metrics?*

---

### 10. Collaboration

**Q:** How do you work with engineers on deployment?
**Good answer:** Constraints first, theory second.

**Probe:**

* *What research tradeoff did you accept for production?*

---

**ML Researcher red flag 🚩**
Brilliant theory, no intuition for **business or adversarial reality**.

---

## Final Interview Heuristic (MD-level)

* **Senior Engineer:** *Can I trust this person on-call?*
* **Staff/Architect:** *Will this reduce org-level risk?*
* **ML Researcher:** *Does this person understand where theory breaks?*

**Related:**- [Top-50-Q&A-AI-ML-Eng](Top-50-Q&A-AI-ML-Eng.md) — Sibling Q&A set covering the same engineering-depth signals at MD/interview panel level.- [Top-50-Q&A-AI-ML-Math](Top-50-Q&A-AI-ML-Math.md) — Sibling Q&A set providing the math foundations behind the probing follow-ups here.- [Java-Python-Enterprise-AI](Java-Python-Enterprise-AI.md) — Production playbook detailing the Spring AI / LangChain4j / DJL stack a Senior Engineer would actually own.- [AI-Coding-Loops](../Agents/development/AI-Coding-Loops.md) — Agentic coding loops that frame how a senior engineer ships and verifies AI components.
