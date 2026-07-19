### Tier 1: Easy / Quick Wins

* **1. Use the Right Model for the Task:** Don't use heavy models (like Claude Opus) for everything. Use lighter models (like Haiku) for summarization or chatbots, and balanced models (like Sonnet) for general coding. Save Opus strictly for complex architectural planning.
* **2. Start Fresh Conversations:** Token costs grow exponentially as previous context is continually sent to the model. Clear the context (e.g., using `/clear`) when switching to a new, unrelated topic.
* **3. Disconnect Unnecessary MCP Servers:** MCP servers load all tool definitions into context on every message, burning tokens. Use basic CLI commands and specific "skills" that only load when explicitly needed.
* **4. Maintain a Markdown Configuration File:** Keep a `claude.markdown` or `agent.markdown` file containing your tech stack, coding conventions, and architectural decisions. This acts as a centralized index and prevents wasting tokens on redundant back-and-forth corrections.
* **5. Batch Related Tasks:** Instead of asking the model to read a file, going back and forth, and then asking it to extract issues, give all instructions in a single prompt. This prevents the LLM from repeatedly rereading prior context.
* **6. Monitor Your Costs:** Use native commands (`/cost`), dashboards, or third-party tools like Cline to track token usage. On AWS, set up CloudWatch alarms and budget alerts.

### Tier 2: Intermediate Strategies

* **7. Utilize Memory:** If you don't use a memory system, you have to constantly redescribe your preferences and past decisions. Giving the LLM memory prevents this repetitive token waste.
* **8. Be Mindful of Agent Costs:** Complex multi-agent teams are heavily expensive because each agent maintains its own context and they often repeat tasks. Stick to single agents unless a complex team is strictly necessary.
* **9. Optimize Vector Database Choices:** Default options like OpenSearch can be very expensive. Consider cheaper alternatives like Aurora PostgreSQL (pgvector) or utilizing Amazon S3 as a highly cost-effective vector database for non-real-time needs.
* **10. Clean Up RAG Documents:** Continually clear out old, unused documents from your Retrieval-Augmented Generation (RAG) system. Storing old embeddings costs money, slows down retrieval, and can pollute your context with irrelevant results.

### Tier 3: Advanced Optimization

* **11. Add a Semantic Caching Layer:** Unlike traditional caching, semantic caching (e.g., Redis LangChain) understands "intent." If two users ask the same underlying question using different words, the cache serves the answer directly without hitting the expensive LLM.
* **12. The Karpathy Method (LLM Wiki):** Maintain a structured, living knowledge base of one-liner insights, past failures, and project workarounds. Feeding this compact index to the LLM skips verbose rediscovery phases.
* **13. Model Distillation:** Use outputs from a large, expensive model (like Opus) to train a smaller, cheaper "student" model (like Haiku) to do specific repetitive tasks (e.g., ticket sorting) at a fraction of the cost.
* **14. Embrace Smaller Models (SLMs):** Use Small Language Models (like Gemma 4) fine-tuned for a singular specific task rather than relying on massive foundation models to do simple jobs. You can even run these locally.
* **15. Apply Traditional Cloud Best Practices:** AI is still cloud infrastructure. Apply enterprise discounts, use reserved capacity or spot instances, right-size your hardware, and scale inference endpoints to zero when idle.

### Bonus Tip

* **AWS Bedrock Specifics:** If using the AWS ecosystem, leverage built-in cost savers like batch inference (50% cheaper), prompt caching, and Bedrock Guardrails (to block irrelevant/malicious inputs before they burn inference tokens).

## Reference

https://www.youtube.com/watch?v=lpj9XqEyHjg

**Related:**
- [OpenResponses-Open-Inference-Standard](OpenResponses-Open-Inference-Standard.md) — Both target inference cost; Open Responses reduces token spend via server-side agentic loops that eliminate the round-trips this file calls out as expensive.
- [Unlock-the-Dark-Data](Unlock-the-Dark-Data.md) — Shares the 'PMF before cost optimization' principle and the same tiered pricing table (premium/efficient/local) used to justify gradual model downshifting.
