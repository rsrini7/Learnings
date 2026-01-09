# The **Ralph** (Ralph Wiggum) pattern: 

A simple bash `while` loop that keeps re‑invoking Claude Code with the same prompt so it can work autonomously for many iterations, using the filesystem as persistent memory instead of chat history.[1][2]

## Core idea

- You write a `prompt.md` that describes the goal, constraints, and what “done” looks like.[3][1]
- A bash loop repeatedly runs Claude Code with that prompt; after each run, Claude modifies files in the repo and exits.[4][1]
- On the next iteration, Claude inspects the existing codebase (including its own prior changes) and continues from there, so the **project files become memory** across loops.[2][1]

### Minimal Ralph loop (conceptual)

```bash
while true; do
  claude-code < prompt.md
done
```

In practice, people add safeguards like max iterations, sleep delays, logging, and stop conditions.[1][3]

## When it works well

The pattern is best for well‑specified, grindy work where success can be checked automatically.[5][1]

- **Greenfield builds**: Implementing a new service or app from clear specs where there is “nothing to break.”[6][1]
- **Large refactors/migrations**: Converting frameworks, switching styles (OOP → FP), or updating APIs where behavior must stay the same and tests can verify correctness.[3][1]
- **Test generation and coverage goals**: E.g., “keep writing tests until coverage ≥ 80%,” where coverage tools give a measurable signal.[5][1]
- **Batch tasks**: Documentation sweeps, cleanup, or repetitive edits across a codebase when “done” can be defined clearly.[6][1]

The philosophy is: define outcomes and success criteria, then let the agent **iterate** instead of micromanaging every step.[2][1]

## When to avoid it

Ralph is “deterministically bad in an undeterministic world”: its failures are predictable and teach you about missing specs, but it will happily grind in the wrong direction if you set the wrong goal.[1][2]

Avoid Ralph loops for:[5][1]

- **Security‑critical code**: Auth, encryption, payments, sensitive data handling; the loop can produce insecure code that still passes naive tests.[1][5]
- **Architecture decisions**: Choosing microservices vs monolith, SQL vs NoSQL, or core system structure needs human context and tradeoff analysis.[5][1]
- **Exploratory work**: Vague tasks like “figure out why the app is slow” have no clear stopping condition; the loop may never converge or may stop after finding a wrong or partial explanation.[1][5]
- **Anything requiring nuanced business judgment**: Product priorities, tradeoffs, or constraints that are not fully encoded in the prompt.[6][1]

## Cost and safety limits

Because each iteration can be a large, tool‑heavy Claude Code run, costs can spike quickly on API pricing.[5][1]

- A 50‑iteration loop on a large repo can easily cost tens or hundreds of dollars in API credits, especially with large models.[1][5]
- People have reported sessions costing a few hundred dollars when they forgot limits.[5][1]

Practical safeguards:[3][1]

- Always set a **max iteration** limit (e.g., 10–20 to start) and increase only once you understand the loop’s behavior.  
- Prefer running on **fixed‑price plans** (like a “max” subscription) rather than raw per‑token APIs when experimenting.  
- Define explicit completion signals (e.g., having the model print `DONE` when all tests pass and goals are satisfied).

## How to think about Ralph

- Ralph is more a **philosophy** than a specific tool: treat failures as data about your prompt and specs, not as random model errors.[2][1]
- Your job shifts from step‑by‑step direction to writing prompts that define clear end states and measurable success criteria.[6][1]
- It is great for multi‑hour or multi‑day autonomous grinding on well‑defined tasks, but you still need humans in the loop for design, security, and exploration.[1][5]

[1](https://www.youtube.com/watch?v=dPG-PsOn-7A)
[2](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)
[3](https://awesomeclaude.ai/ralph-wiggum)
[4](https://anandchowdhary.com/blog/2025/running-claude-code-in-a-loop)
[5](https://dev.to/sivarampg/the-ralph-wiggum-approach-running-ai-coding-agents-for-hours-not-minutes-57c1)
[6](https://www.atcyrus.com/stories/ralph-wiggum-technique-claude-code-autonomous-loops)
[7](https://www.facebook.com/groups/rasikas/posts/10159578929253263/)
[8](https://dopt.gov.in/sites/default/files/AR2023-24English.pdf)
[9](https://ir.library.oregonstate.edu/downloads/sn00b447j?locale=en)
[10](https://www.facebook.com/peteranspachmusic/posts/thank-you-resonance-%EF%B8%8F-the-love-was-there-the-energy-was-bursting-the-mud-pit-was/1255378455293240/)
[11](https://gist.github.com/wong2/e0f34aac66caf890a332f7b6f9e2ba8f)
[12](https://www.sec.gov/Archives/edgar/data/1445815/000121390020006060/0001213900-20-006060.txt)
[13](https://zencoder.ai/blog/wigging-out-controlled-autonomous-loops-in-zenflow)
[14](https://planet.mozilla.org)
[15](https://ghuntley.com)
[16](https://motlin.com/blog/claude-code-workflow-commands)
[17](https://www.facebook.com/groups/infamouslifersgroup/posts/1232719561163304/)
[18](https://github.com/frankbria/ralph-claude-code)
[19](https://stevekinney.com/courses/ai-development/claude-code-and-bash-scripts)
[20](https://www.facebook.com/groups/RandBSlowJamsOldandNew/posts/8708282532550512/)