# White Paper: The Unified Agent Context Framework (UACF)
**Version 1.2 | December 2025**

## Executive Summary
The rapid proliferation of AI coding assistants—from GitHub Copilot to specialized IDEs like Trae, Cursor, and Windsurf—has created a "File Soup" crisis. Developers currently manage context across disparate configuration files (`.cursorrules`, `copilot-instructions.md`, `.trae/project_rules.md`, etc.), leading to fragmentation, drift, and inconsistent agent behavior.

This white paper formalizes the **Unified Agent Context Framework (UACF)**, a standardized methodology to consolidate AI instructions. It leverages the industry-emerging `AGENTS.md` standard as the "Single Source of Truth" while ensuring backward compatibility through symlinks and generation scripts. Furthermore, it outlines the transition to the **Model Context Protocol (MCP)**, where static context files evolve into dynamic context servers.


![Unified Agent Context Framework](../assets/UnifiedAgentContextFramework.png)

[PDF for Unified Agent Context](../assets/Unified_Agent_Context.pdf)
---

## 1. The Crisis: Context Fragmentation
In 2025, a typical modern repository might require 5+ different configuration files to ensure all developers (and their varied AI tools) follow the same architectural patterns.

### The "File Soup" Inventory
| Tool | Configuration File | Location | Behavior |
| :--- | :--- | :--- | :--- |
| **Cursor** | `.cursorrules` | Root | High-priority system prompt injection. |
| **Trae** | `project_rules.md` | `.trae/` | Strict rules for the "Builder" agent. |
| **Windsurf** | `.windsurfrules` | Root | Guidance for the "Cascade" flow. |
| **GitHub Copilot** | `copilot-instructions.md` | `.github/` | Instructions for Chat & Inline completion. |
| **VS Code (Cline)** | `.clinerules` | Root | System prompt for the Cline extension. |
| **Aider** | `CONVENTIONS.md` | Root | Architectural conventions for CLI agents. |

**The Risk:** When a team decides to migrate from *React* to *SolidJS*, they update `.cursorrules` but forget `.trae/project_rules.md`. Half the team's agents continue suggesting React code, creating silent technical debt.

---

## 2. The Solution: Unified Agent Context Framework (UACF)
The UACF proposes a **Two-Tier Architecture**: decoupling the *Source of Truth* (Knowledge) from the *Tool Configuration* (Implementation).

### Tier 1: The Master Knowledge Base (`AGENTS.md`)
The `AGENTS.md` file serves as the universal "README for AI." It is a human-readable and machine-parseable Markdown file located at the repository root.

**Standard `AGENTS.md` Structure:**
```markdown
# Agent Context & Rules
> **Role**: Senior Full-Stack Engineer
> **Stack**: Next.js 15, TypeScript, Tailwind, Supabase

## 1. Universal Principals
- **Code Style**: Functional components, immutable state, early returns.
- **Security**: RLS enabled on all database queries. No sensitive keys in client code.

## 2. Tool-Specific Instructions
<!-- Tools parse these specific sections using regex or MCP adapters -->

### @Trae
- Use `project_rules.md` syntax for strictly enforcing folder structures.

### @Windsurf
- Prioritize the Cascade agent for multi-file refactoring.
```

### Tier 2: The Implementation Layer (Symlinks & Generation)
Instead of manually editing tool-specific files, the framework enforces a "Generate or Link" policy.

**Implementation Strategy:**
1.  **Symlinks (Preferred):** For tools that support standard Markdown at the root.
    *   `ln -s AGENTS.md .cursorrules`
    *   `ln -s AGENTS.md .windsurfrules`
    *   `ln -s AGENTS.md .clinerules`
    *   `ln -s AGENTS.md CONVENTIONS.md`
2.  **Hard Copies (Required):** For tools with strict path requirements (e.g., Trae, Copilot).
    *   *Script:* `cp AGENTS.md .trae/project_rules.md`
    *   *Script:* `cp AGENTS.md .github/copilot-instructions.md`

---

## 3. The Comprehensive Agent Catalog
*A verified taxonomy of 30+ agent ecosystems to structure your repository's `/agents/` documentation folder.*

### A. Core Assistants & IDE Agents
| Agent / Tool | Documentation Files | Active Config File (Runtime) |
| :--- | :--- | :--- |
| **Claude** | `claude.md`, `claude-system-prompt.md` | `CLAUDE.md` (CLI), `.clinerules` (VSCode) |
| **ChatGPT/OpenAI** | `chatgpt.md`, `openai-system-prompt.md` | N/A (Web UI), Custom API `system` msg |
| **GitHub Copilot** | `copilot.md`, `copilot-instruction.md` | `.github/copilot-instructions.md` |
| **Cursor** | `cursor.md`, `cursor-agent.md` | `.cursorrules`, `.cursor/rules/*.mdc` |
| **Windsurf** | `windsurf.md`, `windsurf-agent.md` | `.windsurfrules`, `~/.windsurf/global_rules.md` |
| **VS Code** | `vscode-agent.md`, `tasks-agent.md` | `tasks.json`, `.vscode/settings.json` |
| **JetBrains AI** | `jetbrains-ai.md`, `jetbrains-system.md` | `.jetbrains/` (Limited custom prompt support) |
| **Zed AI** | `zed-ai.md`, `zed-system.md` | `.rules` (Falls back to `.cursorrules`) |
| **Amazon Q** | `amazon-q.md`, `amazon-q-system.md` | `.aws/` config (Project context limited) |

### B. Automation & Workflow Agents
| Agent / Tool | Documentation Files | Active Config File (Runtime) |
| :--- | :--- | :--- |
| **Trae** | `trae.md`, `trae-system-prompt.md` | `.trae/project_rules.md`, `.trae/user_rules.md` |
| **Aider** | `aider.md`, `aider-system.md` | `CONVENTIONS.md`, `.aider.conf.yml` |
| **Continue** | `continue.md`, `continue-system.md` | `.continue/config.json` (System prompt field) |
| **Sourcegraph Cody**| `cody.md`, `cody-system.md` | `.cody/ignore`, context via embeddings |
| **Replit Agent** | `replit-agent.md`, `replit-system.md` | `.replit` (Agent settings section) |

### C. Research, Retrieval, and Web Grounded
| Agent / Tool | Documentation Files | Context Strategy |
| :--- | :--- | :--- |
| **Perplexity** | `perplexity.md`, `perplexity-system.md` | Collections & Profiles (Web UI) |
| **Poe** | `poe.md`, `poe-bot-prompts.md` | Bot Server prompts (API/Web) |
| **RAG Setups** | `rag-agent.md`, `rag-system-prompt.md` | `knowledge.json`, Vector DB metadata |

### D. Specialized and Emerging Tools
| Agent / Tool | Documentation Files | Notes / Config |
| :--- | :--- | :--- |
| **Devin AI** | `devin.md`, `devin-system.md` | Proprietary; reads repo `README.md` heavily |
| **v0 (Vercel)** | `v0.md`, `v0-system.md` | `.v0rules` (Emerging support), Project "Rules" tab |
| **Dia** | `dia.md`, `dia-system-prompt.md` | Model-specific context injection via API |
| **NotionAI** | `notion-ai.md`, `notion-system.md` | Page context, Custom Instructions block |
| **Botpress** | `botpress.md`, `botpress-system.md` | Botpress Studio "Persona" settings |

### E. Open-Source Frameworks (LangChain, etc.)
| Agent / Tool | Documentation Files | Active Config File (Runtime) |
| :--- | :--- | :--- |
| **LangChain** | `langchain-agent.md` | `system_message` in Python/JS code |
| **CrewAI** | `crewai.md`, `crewai-system.md` | `agents.yaml` (Role definitions) |
| **AutoGen** | `autogen.md`, `autogen-system.md` | `OAI_CONFIG_LIST`, Python config |

---

## 4. Future-Proofing: The Model Context Protocol (MCP)
The industry is currently transitioning from static files (Text) to active servers (Protocol).

### The Role of MCP
The Model Context Protocol (MCP) allows agents to *ask* for context rather than just reading a file.
*   **Static Era (Now):** Agent reads `AGENTS.md` -> Context Window.
*   **MCP Era (Next):** Agent queries local MCP Server -> Server reads `AGENTS.md` -> Server returns *only relevant sections*.

**Action Item:** Ensure your `AGENTS.md` is structured with clear headers (`## Database Schema`, `## API Routes`). This allows future MCP servers to parse the file semantically and serve only the necessary chunks to the agent, saving token costs and reducing hallucinations.

## 5. Strategic Recommendations
1.  **Adopt `AGENTS.md`**: Create this file at the root of every repository immediately.
2.  **Script the Sync**: Use a simple CI/CD script or `makefile` to copy `AGENTS.md` to `.trae/project_rules.md` and `.github/copilot-instructions.md` automatically.
3.  **Build the Catalog**: Use the directory structure in Section 3 to document *why* you configured the agents the way you did, preserving institutional knowledge.
4.  **Monitor Trae & v0**: These tools are evolving rapidly. Trae's reliance on `.trae/project_rules.md` is likely to expand to include standard MCP support soon.

## 5. Conclusion
Your catalog index is an excellent Taxonomy of Agents. By combining it with the technical implementation of AGENTS.md, you create a robust system where:

Humans read the /agents/ catalog to learn about tools.

Machines read AGENTS.md (via symlinks) to enforce rules.

Documentation stays in sync with Execution.