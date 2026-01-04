# Recursive Language Models (RLMs)
## Quick Reference & Decision Guide

---

## What Are RLMs in 30 Seconds?

Instead of feeding huge documents directly into an AI model (where it gets confused and fails), RLMs:
1. **Store the document outside** the model as a string variable
2. **Let the AI write Python code** to explore and filter the document  
3. **Call smaller AI copies** to process important chunks
4. **Combine results** programmatically

**Result**: Process 100x longer documents, 2-15x better accuracy, same or lower cost.

---

## The Three Problems RLMs Solve

| Problem | Example | RLM Solution |
|---------|---------|------|
| **Context Rot** | "Find pairs of matching users among 3,000 profiles" → Model gets 0.04% accuracy | Process 100 users at a time, aggregate deterministically → 58% accuracy |
| **Attention is Quadratic** | Doubling input length = 4x more compute needed | Explore selectively via code → only process relevant portions |
| **Unmanageable Scale** | 11M token document exceeds model's limits entirely | Work through document in chunks via recursion → 91% accuracy |

---

## The Four Strategies RLMs Use (Naturally)

### 1. **Smart Filtering ("Peeking & Grepping")**
```
Root LLM: "I need festival information"
→ Peeks at 1% of document structure
→ Runs regex for "festival"  
→ Only processes 50 matching lines out of 10,000
→ Result: 50x speedup
```

### 2. **Semantic Chunking**
```
Root LLM: "Classify all 6,000 questions"
→ Breaks into 60 chunks of 100
→ Calls sub-LM on each chunk
→ Combines results programmatically
→ Result: Avoids context rot on large dataset
```

### 3. **Recursive Reasoning**
```
Root LLM: "Find all matching pairs"
→ Instead of comparing all pairs (quadratic = impossible)
→ 1st pass: Classify each item (linear)
→ 2nd pass: Find pairs among classified items (tractable)
→ Result: 1,450x improvement (0.04% → 58%)
```

### 4. **Unbounded Output**
```
Root LLM: "Generate 100K token document"
→ Can't do in one shot (model output limit)
→ Generates in sections, stores in variables
→ Concatenates sections at end
→ Result: No output length limits
```

---

## Performance at a Glance

### The Metrics That Matter

| Metric | RLM Performance | vs. Base Model | vs. RAG |
|--------|-----------------|----------------|--------|
| **Quadratic Tasks** | 58% F1 | +1,450x | Completes (vs fails) |
| **11M Token Docs** | 91% accuracy | Only method that works | Works but less thorough |
| **Cost/Query** | $0.33-$0.99 | Lower or same | 3-9x cheaper |
| **Coverage** | 100% (deterministic) | N/A | ~80% (probabilistic) |

### The Benchmarks (GPT-5)

```
Task: OOLONG-Pairs (Find matching user pairs)
─────────────────────────────────────────
Base Model:        0.04% ✗ (unusable)
CodeAct Agent:     0.28% ✗ (still bad)
Summary Agent:     0.31% ✗ (fails)
RLM (no recursion): 44%  ✓ (good)
RLM (full):        58%  ✓ (excellent)

Task: BrowseComp-Plus (1K documents, 11M tokens)
─────────────────────────────────────────
Base Model:        0% ✗ (exceeds context limit)
Summary Agent:     70% (lossy)
RLM:              91% ✓ (best)

Task: CodeQA (Code repository understanding, 23K-4.2M tokens)
─────────────────────────────────────────
Base Model:        24% (struggles)
Summary Agent:     58%
RLM:              62% ✓ (cheaper: $0.11 vs $1.31)
```

---

## When to Use RLMs

### ✓ YES - Use RLMs If:
- [ ] Document/prompt exceeds 100K tokens
- [ ] Task requires complex reasoning (not just lookup)
- [ ] Need guaranteed data coverage (can't miss any records)
- [ ] Information is spread across many sources
- [ ] Acceptable latency: 2-30 seconds per query
- [ ] Budget somewhat flexible (cost varies by task complexity)

### ✗ NO - Don't Use RLMs If:
- [ ] Context under 4K tokens (overhead too high)
- [ ] Need instant responses (<500ms)
- [ ] Simple retrieval (use RAG instead)
- [ ] Using weak models (need GPT-5 or Qwen3-Coder level)
- [ ] Cost must be absolutely fixed

### Decision Tree:
```
Input Length?
├─ < 4K tokens → Use base LLM (RLM overhead not worth it)
├─ 4K-100K tokens
│  ├─ Simple QA? → Try RAG first
│  └─ Complex reasoning? → Use RLM
└─ > 100K tokens → Use RLM (often the only option)
```

---

## RLM vs. The Alternatives (Side-by-Side)

### RLM vs. RAG (Retrieval-Augmented Generation)

| Dimension | RLM | RAG | Winner |
|-----------|-----|-----|--------|
| **Find all matching pairs** | ✓ 100% coverage (deterministic loop) | ✗ Lossy (might miss pairs) | RLM |
| **Answer factual questions** | ✓ 91% on BrowseComp | ✓ 70-80% typical | Either |
| **Setup complexity** | Low (just Python) | Moderate (vector DB, embeddings) | RLM |
| **Cost on simple QA** | Higher | Lower | RAG |
| **Cost on complex reasoning** | Comparable/Lower | 3-9x higher | RLM |
| **Hallucination mitigation** | Code execution provides ground truth | Grounded in retrieved docs | Both good |

**Verdict**: Use RAG for quick factual retrieval. Use RLM for guaranteed completeness and complex reasoning.

---

### RLM vs. Context Compression (Summarization)

| Dimension | RLM | Summarization | Winner |
|-----------|-----|----------------|--------|
| **Detail loss** | None (can re-examine original) | Permanent | RLM |
| **Cost** | Medium (selective processing) | High (compress all) | RLM |
| **Speed** | 5-30 seconds | 10-60 seconds | RLM |
| **Quadratic tasks** | 58% accuracy | 0.31% accuracy | RLM (186x better) |
| **Simple Q&A** | Works fine | Slightly faster | Summarization |

**Verdict**: Summarization is faster for basic tasks. RLM wins for anything complex.

---

### RLM vs. Larger Context Windows

| Dimension | RLM | Bigger Window | Winner |
|-----------|-----|----------------|--------|
| **Hardware needed** | Same | Exponentially more | RLM |
| **Training required** | None | Full model retrain | RLM |
| **Inference cost** | Low-medium (selective) | High (full context) | RLM |
| **Handles context rot** | Yes (via recursion) | No (still suffers) | RLM |
| **Deployment time** | Days (just inference) | Months (training) | RLM |

**Verdict**: RLMs are faster, cheaper, and work better than scaling context windows.

---

## Cost Model Breakdown

### Typical RLM Query Costs (GPT-5)

**Scenario**: 1,000 documents, 11M tokens total, find key information

```
Old Approach (RAG):
├─ Vector DB lookup: $0.01
├─ Retrieve top 10 docs: $0.01
├─ Feed 50K tokens to GPT-5: $0.15
├─ Get partial answer
└─ Total: $0.17 (but incomplete)

New Approach (Summarization):
├─ Compress all 11M tokens: $2.00
├─ Feed summary + query: $0.50
└─ Total: $2.50 (expensive, still loses details)

RLM Approach:
├─ Root LLM (code generation): $0.05
├─ Peek at structure: $0.02
├─ Regex filtering (code execution): $0.00
├─ Sub-LM calls on filtered docs (100 docs): $0.92
│  └─ (100 × $0.009/mini call)
└─ Total: $0.99 (Cheaper AND more accurate!)
```

### Cost Drivers in RLMs
1. **Root LLM calls** (plan & aggregate): ~$0.05-$0.10
2. **Sub-LM calls** (process chunks): $0.001-$0.01 per chunk
3. **Total proportional to**: Document complexity + recursion depth

**Rule of thumb**: Cost ≈ $0.10 (root) + (# chunks × chunk complexity × $0.005)

---

## Implementation Checklist

### Phase 1: Setup (Day 1)
- [ ] Get API access to GPT-5 or Qwen3-Coder
- [ ] Set up Python environment with `subprocess` for REPL
- [ ] Write basic RLM class with `execute_code()` method

### Phase 2: Basic RLM (Days 2-3)
- [ ] Implement Root LLM loop
- [ ] Create system prompt with examples
- [ ] Test on simple task (single query over 100K tokens)

### Phase 3: Production (Days 4-7)
- [ ] Test on your actual benchmark tasks
- [ ] Tune system prompt for your domain
- [ ] Implement error handling & timeouts
- [ ] Add cost tracking & logging
- [ ] Compare vs. baseline methods

### Phase 4: Optimization (Ongoing)
- [ ] Monitor cost variance (implement alerts if >3x median)
- [ ] A/B test prompt variations
- [ ] Add domain-specific examples to prompts
- [ ] Consider RL training for learned decomposition

---

## Real-World Examples

### Example 1: Legal Document Review
**Task**: Review 500 contracts (50M tokens), find all clauses mentioning "IP ownership"

**Old Way (RAG)**:
```
Search for "IP ownership" → 50 matches
Read those 50 clauses manually
Risk: Miss context-dependent uses
```

**RLM Way**:
```
Root LLM: "Find all IP-related clauses with context"
├─ Peek at contract format
├─ Run regex for "IP" keywords
├─ For each match: Sub-LM reads full clause + context
├─ Aggregate all findings
└─ Return comprehensive report with zero misses
```

**Result**: 100% coverage, ~$45 cost, 15 minutes latency

---

### Example 2: Scientific Literature Synthesis
**Task**: 1,000 research papers (100M tokens), find papers citing both "method A" AND "method B"

**Old Way (Base Model)**:
```
Try to feed all into GPT-5
→ Exceeds context limit
→ Fails
```

**RLM Way**:
```
Root LLM: "Find papers mentioning both methods"
├─ Split papers into groups of 10
├─ For each group: "Which papers mention method A AND B?"
├─ Sub-LMs vote on each paper  
├─ Aggregate into final list
└─ Return 47 papers + citation info
```

**Result**: Complete, accurate results, ~$10 cost, 5 minutes

---

## Common Gotchas & How to Fix Them

### Gotcha 1: High Cost Variance
**Problem**: Some queries cost $0.30, others cost $3.00 for same task size

**Cause**: Model over-verifies (checks answer 5x instead of 1x)

**Fix**:
- Add to system prompt: "Verify at most once. Move forward after verification."
- Set max recursion depth
- Use cost-aware RL training

### Gotcha 2: Slow Performance
**Problem**: Takes 30+ seconds per query

**Cause**: Sequential sub-calls (one finishes before next starts)

**Fix**:
- Implement async/parallel sub-calls (when available)
- Batch sub-calls (10 at a time instead of 1 at a time)
- Use cheaper/faster models for sub-calls (GPT-5-mini instead of GPT-5)

### Gotcha 3: Hallucinations in Sub-LM Calls
**Problem**: Sub-LM invents information not in its chunk

**Cause**: Sub-LMs still have intrinsic hallucination tendency

**Fix**:
- Add to sub-LM prompt: "Only report information explicitly in the text. Do not infer or extrapolate."
- Use code to verify answers (grep the original text)
- Have root LM spot-check sub-LM outputs

### Gotcha 4: Model Can't Code Well
**Problem**: Using a weak model (GPT-4, Qwen3-8B) results in bad code

**Cause**: Model lacks strong coding ability

**Fix**:
- Use frontier models: GPT-5, Qwen3-Coder, Claude 3.7
- Provide code examples in system prompt
- Consider code verification (static analysis, type checking)

---

## Key Takeaways

1. **Context rot is real** — It's not about length, it's about reasoning complexity
2. **RLMs solve it elegantly** — Let the AI explore intelligently, not brute-force process
3. **You get 2-15x accuracy gains** — Especially on complex tasks (quadratic: 0% → 58%)
4. **Cost is comparable or lower** — $0.99 vs $2.50 for same task, with better results
5. **Implementation is straightforward** — Python REPL + LLM loop, days to production
6. **Best for long, complex documents** — Short documents don't need RLMs
7. **Complement existing techniques** — RLM + RAG + fine-tuning = optimal system

---

## Resources

**Official Paper**: 
- arXiv: 2512.24601
- Authors: Alex Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)

**Code**:
- GitHub: `github.com/alexzhang13/rlm`
- Minimal implementation: `github.com/alexzhang13/rlm-minimal`

**Benchmarks**:
- OOLONG: Long-context reasoning
- BrowseComp-Plus: Multi-hop web research
- CodeQA: Code repository understanding

**Related Work**:
- Prime Intellect RLMENV implementation
- Inference-time scaling (OpenAI o1 reasoning)
- Context folding techniques

---

## Summary Table: RLM Feature Matrix

| Feature | Status | Notes |
|---------|--------|-------|
| **Handles 10M+ tokens** | ✓ Works | Only mainstream approach that does this |
| **Quadratic complexity tasks** | ✓ Excellent | 58% accuracy vs 0.04% baseline |
| **Parallel sub-calls** | ✗ Not yet | Sequential only, 10x slowdown potential |
| **Learned decomposition** | ✗ Not yet | Uses model priors + code, RL coming |
| **Multi-turn conversations** | ✓ Yes | Can maintain context across turns |
| **Streaming output** | ✓ Yes | Can output while processing |
| **Works with weak models** | ✗ No | Needs GPT-5 level minimum |
| **Requires fine-tuning** | ✗ No | Works with base models |
| **Production ready** | ✓ Yes | Being used in Prime Intellect |

---

**Document Version**: 1.0  
**Last Updated**: January 4, 2026

This quick reference complements the full whitepaper for decision-makers and engineers evaluating RLM adoption.