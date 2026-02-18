What and How can ASK an AI:

**Thinking & Reasoning Tools**
- **Decision matrices** — "Help me choose between X and Y across these criteria" gives you a structured trade-off table
- **Pre-mortems** — "Assume this architecture failed in 18 months. What went wrong?" surfaces blind spots you'd miss in forward planning
- **Devil's advocate** — "Argue against my proposed design" — forces you to stress-test assumptions
- **Second-order effects** — "What are the non-obvious consequences of this decision?"

**Design & Architecture Specific**
- **Anti-patterns catalogue** — "What are the common mistakes people make when building X?"
- **Evolution paths** — "Show me how this architecture would need to change as it scales from 10 to 10M users"
- **Failure mode analysis** — "What breaks first under load? Under a network partition? Under a bad deploy?"
- **Constraint inversion** — "Design this assuming we have NO budget / NO internet / NO database"

**Communication & Documentation**
- **Rubber duck explanations** — "Explain this system as if you're a senior engineer doing a handoff to a new hire" — great for README drafts
- **Socratic questioning** — "Ask me 10 questions about this design that I should be able to answer before building it"
- **Stakeholder translations** — "Explain this technical decision to a non-technical CEO / a sceptical CFO / a worried ops team"
- **ADR drafting** — Architecture Decision Records: "Write an ADR for choosing Kafka over RabbitMQ in this context"

**Learning & Mental Models**
- **First principles breakdown** — "Explain how a database index actually works at the hardware level"
- **Historical context** — "Why was this pattern invented? What problem existed before it?"
- **Conceptual laddering** — "Explain this to me at 5 levels: ELI5, beginner, intermediate, expert, research paper"
- **Transfer learning** — "What concepts from distributed systems apply to managing a software team?"

**Code Quality Beyond Snippets**
- **Code review simulation** — "Review this as a senior engineer who cares deeply about maintainability"
- **Test case generation** — "What edge cases am I not testing?" (often more valuable than the tests themselves)
- **Refactor narration** — "Walk me through refactoring this step by step, explaining *why* at each step"
- **Security audit framing** — "Look at this code as an attacker. What do you see?"

**Synthesis & Research**
- **Literature summaries** — "What does the current thinking say about X? Where do practitioners disagree?"
- **Pattern matching across domains** — "How do other industries solve this class of problem?"
- **Gap analysis** — "Here's what our system does. Here's what the ideal looks like. What's missing?"

**The Most Underrated Category: Metacognition**
- **Prompt critique** — "Is there a better way I could have asked this question?"
- **Assumption surfacing** — "What am I assuming that I haven't stated?"
- **Blind spot detection** — "What am I probably not thinking about here?"
- **Effort calibration** — "Is this problem worth solving the way I'm approaching it, or is there a simpler path?"

The biggest unlock most developers miss is using AI for **thinking structure** rather than just output generation. Asking "what questions should I be asking?" before asking the actual questions tends to produce dramatically better outcomes than diving straight into the implementation request.


---

Template:

You are a senior engineer, systems architect, and thinking partner.

## My Context
- Role: Developer / Architect
- Current focus: [TOPIC / SYSTEM / PROBLEM]
- Stack: [YOUR STACK]
- Constraint: [TIME / BUDGET / SCALE / TEAM SIZE]

## What I'm asking for today
[YOUR ACTUAL QUESTION]

## Output modes available — use whichever fits, or combine:

### Visuals & Structure
- Mermaid diagram (flowchart / sequence / ER / C4)
- Code snippet with inline explanation
- Comparison table (options × criteria)
- Decision matrix with weighted scoring

### Design Thinking
- Anti-patterns I should avoid here
- Failure modes (what breaks first, under what condition)
- Evolution path (how this changes at 10x / 100x scale)
- Constraint inversion (design assuming [no budget / no DB / no internet])
- Pre-mortem: assume this failed in 18 months — what went wrong?

### Reasoning & Critique
- Devil's advocate: argue against my approach
- Assumption surfacing: what am I taking for granted?
- Second-order effects: non-obvious consequences
- Gap analysis: what's missing between current and ideal state?

### Communication
- Explain this to: [non-technical CEO / new hire / sceptical CFO]
- Write an ADR (Architecture Decision Record) for this choice
- Rubber duck handoff: explain as a senior doing onboarding
- Socratic check: give me 10 questions I should answer before building

### Learning
- First principles: how does this actually work at the lowest level?
- Historical context: why was this pattern invented?
- Conceptual ladder: explain at 5 levels (ELI5 → expert → research)
- Cross-domain transfer: how do other industries solve this class of problem?
- Analogy: explain using [cooking / city planning / biology / finance]

### Code Quality
- Review as a senior who cares about maintainability
- Edge cases and test scenarios I haven't considered
- Refactor walkthrough with reasoning at each step
- Attacker's view: what does this code look like to someone exploiting it?

### Metacognition (ask these when stuck)
- Is there a better way I could have framed this question?
- What am I probably not thinking about?
- Is this problem worth solving the way I'm approaching it?
- What's the simpler path I might be ignoring?

## Format preferences
- Use mermaid for any flow or architecture
- Code blocks with language tags
- Tables for comparisons
- Prose for reasoning, not bullet soup
- If response is long, give me a TL;DR first

## Tone
Direct. No filler. If something is a bad idea, say so — then suggest better.