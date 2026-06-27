# Top 50 interview Q/A to separate a “Twitter Expert” from an Engineer

Below are **50 crisp questions** an MD or hiring panel can use to evaluate whether a candidate has *practical engineering depth* (the kind that matters for regulated, production AI) — each with a short model answer and the reason you should accept that answer. These are drawn from the team-level roadmap and payments-specific context. 

---

## Foundations & Math (1–10)

1. **Q:** What is a Transformer at a high level?
   **A:** A sequence model using self-attention that computes token relationships in parallel for scalable context modeling.
   **Reason:** Tests whether they understand architecture, not just buzzwords.

2. **Q:** Why does softmax appear in attention?
   **A:** To convert raw similarity scores into a probability distribution that weighs value aggregation.
   **Reason:** Shows grasp of the math behind attention weighting.

3. **Q:** Explain vanishing gradients and one concrete mitigation.
   **A:** Gradients shrink across many layers; use residual connections or layer norm to preserve gradient flow.
   **Reason:** Demonstrates practical technique to fix training instability.

4. **Q:** How do you choose a loss function for fraud scoring?
   **A:** Align loss with business objective (e.g., weighted cross-entropy or cost-sensitive loss to reflect FP/FN costs).
   **Reason:** Links metric choice to dollar impact.

5. **Q:** What is calibration and why does it matter?
   **A:** Calibration aligns predicted probabilities with empirical frequencies—critical when decisions map to actions (decline/approve).
   **Reason:** Shows operational understanding beyond accuracy.

6. **Q:** Explain bias vs variance in production.
   **A:** Bias = systematic error (underfitting); variance = instability on new data (overfitting). Both affect long-term risk.
   **Reason:** Fundamental debugging concept.

7. **Q:** What is concept drift and a simple detection method?
   **A:** Data distribution changing over time; detect via monitoring feature/score distributions and KL divergence or population stability index.
   **Reason:** Proves they can operationalize monitoring.

8. **Q:** Why prefer AUC sometimes, but not always, in imbalanced payments data?
   **A:** AUC measures rank ordering but ignores calibration/threshold costs—false positives can be costlier in payments.
   **Reason:** Shows trade-off thinking.

9. **Q:** How would you set a decision threshold for a fraud model?
   **A:** Use cost-sensitive analysis (expected loss per threshold) and constraints (e.g., max FP rate) to pick threshold.
   **Reason:** Ties model to business KPIs.

10. **Q:** When is a simpler model preferable in production?
    **A:** When latency, explainability, or stability outweigh marginal accuracy gains.
    **Reason:** Real-world constraint-aware answer.

---

## Model Internals & Inference (11–20)

11. **Q:** What causes inference latency besides model size?
    **A:** I/O overhead, batching strategy, cold starts, tokenization, serialization, and blocking operations.
    **Reason:** Shows operational root-cause thinking.

12. **Q:** How does batching trade off throughput and latency?
    **A:** Larger batches increase throughput but add queuing latency; choose dynamic batching or small max batch for low-p99 latency.
    **Reason:** Practical tuning knowledge.

13. **Q:** Explain quantization and when to use it.
    **A:** Reduces numeric precision for weights/activations to lower memory/compute with small accuracy loss—good for edge/low-latency.
    **Reason:** Shows optimization toolbox.

14. **Q:** What is knowledge distillation?
    **A:** Train a smaller model to mimic a larger model’s outputs to get lighter inference with similar behavior.
    **Reason:** Useful for production constraints.

15. **Q:** How do you protect inference from prompt injection or bad inputs?
    **A:** Input sanitization, schema validation, guardrails, rate limits, and a safe-fallback policy.
    **Reason:** Security-aware operational practice.

16. **Q:** When would you deploy a model as local LLM vs cloud API?
    **A:** Local for data privacy, latency, or cost predictability; cloud for scale and rapid iteration.
    **Reason:** Shows tradeoffs important to enterprises.

17. **Q:** What’s the role of a model server (e.g., Triton)?
    **A:** Provides unified inference, batching, GPU optimization, versioning, and metrics for production serving.
    **Reason:** Tests knowledge of serving infrastructure.

18. **Q:** How to measure model regression post-deploy?
    **A:** Monitor key metrics (FP/FN, latency), data drift, user feedback, and A/B testing with holdouts.
    **Reason:** Connects monitoring to decision-making.

19. **Q:** Explain cold-start effects and mitigations.
    **A:** Cold-start: slow first requests due to JIT/initialization. Mitigate via warm pools, preloading models, or lightweight proxies.
    **Reason:** Operational smoothing matter.

20. **Q:** How do you validate a model’s inference under adversarial inputs?
    **A:** Use adversarial testing, fuzzing, out-of-distribution detectors, and robust training techniques.
    **Reason:** Ensures model robustness.

---

## Systems, Integration & Architecture (21–30)

21. **Q:** Why keep model training and serving separated?
    **A:** Different SLAs, dependencies, compute profiles, security boundaries, and deployment cadences.
    **Reason:** Basic architecture principle.

22. **Q:** How do you handle model versioning and rollout?
    **A:** Use model registry, semantic versioning, canary rollouts, shadow testing, and automated rollback.
    **Reason:** Shows mature delivery pipeline planning.

23. **Q:** What is a shadow deployment and why use it?
    **A:** Mirror live traffic to new model without affecting production decisions—to validate behavior on real traffic.
    **Reason:** Low-risk validation technique.

24. **Q:** How to ensure auditability of a decline decision?
    **A:** Persist input features, model version, score, decision rule, reason code, and human review notes in an immutable store.
    **Reason:** Enables post-incident traceability.

25. **Q:** Explain separation of decision logic and execution in payments.
    **A:** Decision (score + reason) should be separated from execution (fund movement) with explicit approval and safeguards.
    **Reason:** Limits blast radius of errors.

26. **Q:** What observability signals are critical for payments AI?
    **A:** Authorization latency, score distribution, FP/FN rates, decline reasons, queue lengths, and cost-per-inference.
    **Reason:** Shows what to monitor for trust.

27. **Q:** How do you manage model secrets and keys in production?
    **A:** Use secret management (Vault, KMS), least privilege, rotation, and audit trails.
    **Reason:** Security best practice.

28. **Q:** When integrating third-party ML APIs, what’s your top concern?
    **A:** Data privacy, SLAs, explainability limits, and vendor lock-in/cost.
    **Reason:** Practical vendor evaluation.

29. **Q:** How would you design retry/backoff for model inference?
    **A:** Idempotent requests, exponential backoff, circuit breakers, and prioritization to protect p99 latency.
    **Reason:** Resilience engineering.

30. **Q:** Why centralize model access in an AI gateway?
    **A:** Centralized policy, cost control, auditing, and consistent enforcement of guardrails.
    **Reason:** Enterprise control-plane rationale.

---

## Evaluation, Testing & Metrics (31–38)

31. **Q:** How do you evaluate a model for production readiness?
    **A:** Business-aligned metrics, stability over time, explainability, resource profile, and failure-mode analysis.
    **Reason:** Prevents launching on vanity metrics.

32. **Q:** What is a service-level objective (SLO) for an ML model?
    **A:** A measurable reliability target (e.g., p99 latency < X ms, FP rate < Y) tied to business impact.
    **Reason:** Operationalizes expectations.

33. **Q:** How do you do offline vs online evaluation?
    **A:** Offline uses historical labeled data; online uses live traffic (A/B, canary) to measure real impact.
    **Reason:** Shows end-to-end validation approach.

34. **Q:** What tests should be in CI for model changes?
    **A:** Unit tests, data schema checks, model quality gates, inference smoke tests, and fairness/regulatory checks.
    **Reason:** Ensures safe deployments.

35. **Q:** How to set up drift detection for features?
    **A:** Track per-feature distributions, set thresholds, and alert when drift crosses defined bounds.
    **Reason:** Early warning for model degradation.

36. **Q:** How do you quantify explainability for audit purposes?
    **A:** Provide feature attributions, counterfactuals, and human-readable reason codes tied to decision logic.
    **Reason:** Makes explanations actionable for auditors.

37. **Q:** What A/B experiment would you run before full rollout?
    **A:** Measure business KPIs (fraud loss, authorization rate), user impact, and system metrics over a sufficient volume window.
    **Reason:** Directly ties efficacy to outcomes.

38. **Q:** How to test model fairness in payments?
    **A:** Group-level performance checks, disparate impact metrics, and bias audits with mitigation plans.
    **Reason:** Regulatory and reputational necessity.

---

## Agents, Multimodal & Edge (39–46)

39. **Q:** Where are agents appropriate in payments?
    **A:** Investigations, dispute summaries, ops automation—not real-time auth or fund movement.
    **Reason:** Matches risk-versus-value tradeoff.

40. **Q:** How do you ensure an agent’s action is auditable?
    **A:** Log prompts, context, tool calls, outcomes, and provide human-approval checkpoints.
    **Reason:** Maintains accountability for autonomous steps.

41. **Q:** What’s a safe pattern for human-in-the-loop?
    **A:** Agent suggests, human approves/rejects, and system enforces final authority with recorded rationale.
    **Reason:** Keeps humans responsible for high-risk actions.

42. **Q:** When is multimodal useful for payments?
    **A:** Document/image-based KYC, invoice reconciliation, or dispute evidence extraction—not core auth scoring.
    **Reason:** Shows targeted use-cases.

43. **Q:** Edge inference—when adopt it in payments?
    **A:** Rarely—only for physical POS devices requiring offline decisions or privacy constraints.
    **Reason:** Reflects practical adoption curve.

44. **Q:** How do you limit agent “blast radius”?
    **A:** Rate limits, scope restrictions, sandboxed tool access, and predefined action templates.
    **Reason:** Prevents uncontrolled automation.

45. **Q:** What logging must accompany multimodal predictions?
    **A:** Input artifacts (hashed or masked), extracted features, model version, and explanation artifacts.
    **Reason:** Preserves provenance for non-text inputs.

46. **Q:** How to handle sensitive PII in models/agents?
    **A:** Mask/obfuscate PII, minimize retention, encrypt at rest/in transit, and use tokenization where possible.
    **Reason:** Legal and compliance requirement.

---

## Behavioral, Risk & Leadership (47–50)

47. **Q:** Describe a time you debugged a production model incident. What steps did you take?
    **A:** Triage (metrics), isolate change, reproduce, rollback/canary, patch, root cause, postmortem with action items.
    **Reason:** Tests incident process literacy and ownership.

48. **Q:** How do you prioritize fixes: accuracy vs latency vs explainability?
    **A:** Prioritize by business impact and regulatory risk; pick the fix that reduces expected loss or exposure.
    **Reason:** Shows product-oriented decision-making.

49. **Q:** If a vendor’s model is a black box, what’s your approach?
    **A:** Push for SLA/metrics, shadow test, add monitoring, require explainability contracts, and limit vendor scope on critical paths.
    **Reason:** Pragmatic vendor risk management.

50. **Q:** How would you convince an MD to fund a 6-month model hardening program?
    **A:** Present expected ROI in reduced fraud loss/incidents, regulatory risk reduction, and faster time-to-production—backed by pilot numbers and SLOs.
    **Reason:** Aligns technical investment to hard business outcomes.

