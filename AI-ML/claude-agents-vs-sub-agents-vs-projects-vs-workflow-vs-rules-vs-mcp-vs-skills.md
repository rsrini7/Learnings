## **Claude Agents (via Agent SDK)**
Claude agents operate in a specific feedback loop: gather context → take action → verify work → repeat. The Agent SDK allows you to build custom AI agents that can use tools, manage context, and perform complex multi-step tasks. Think of agents as the overall orchestrator that coordinates everything.

## **Sub-agents**
Sub-agents transform a single AI assistant into a powerful, customizable team of specialized experts. They have two key benefits:

1. **Context Management**: Each subagent uses its own isolated context window and only sends relevant information back to the orchestrator, rather than their full context
2. **Parallelization**: You can spin up multiple subagents to work on different tasks simultaneously

In Claude Code, you define sub-agents as markdown files in `.claude/agents/` directories with custom system prompts and tool restrictions.

## **Projects**
Projects allow you to ground Claude's outputs in your internal knowledge—be it style guides, codebases, interview transcripts, or past work. They're available on claude.ai and provide:

- A 200K context window, the equivalent of a 500-page book
- Custom instructions that apply to all chats within the project
- Document upload capabilities for persistent knowledge
- Team collaboration features (on Team/Enterprise plans)

Projects are best for: organized workspaces where you need persistent context across multiple conversations with uploaded documents and custom instructions.

## **Workflows**
Workflows define sets of automation rules for repetitive development tasks. In Claude Code, workflows can include:

- Custom slash commands stored in `.claude/commands/`
- Event-driven triggers (e.g., automatically running tests when code changes)
- Multi-step automation sequences
- Integration with CI/CD pipelines

Workflows are essentially automation patterns—you're defining "when X happens, do Y."

## **Rules (CLAUDE.md files)**
CLAUDE.md files are special configuration files that Claude automatically loads into context when starting a session. They act as the governance layer, ensuring that every implementation goes through structured verification before being approved. You can have:

- Global rules in the repository root
- Directory-specific rules that override global ones
- Instructions about which tools to use, coding standards, verification steps, etc.

## **MCP (Model Context Protocol)**
MCP is an open-source standard for connecting AI applications to external systems. Think of MCP like a USB-C port for AI applications—it provides a standardized way to connect AI systems with data sources.

MCP enables Claude to connect to:
- Data sources (Google Drive, Slack, GitHub, databases)
- Tools (search engines, calculators, Playwright for browser automation)
- Custom integrations via MCP servers

The Model Context Protocol provides standardized integrations to external services, handling authentication and API calls automatically.

## **Skills**
A Skill is a markdown file that teaches Claude how to do something specific: reviewing PRs using your team's standards, generating commit messages in your preferred format, or querying your company's database schema.

Skills use progressive disclosure: Claude loads information in stages as needed, rather than consuming context upfront. At startup, Claude loads metadata and includes it in the system prompt, meaning you can install many Skills without context penalty.

---

## **How They Work Together**

**Hierarchy**: Agent → Sub-agents → Skills/MCP tools
- Your **agent** is the main orchestrator
- It spawns **sub-agents** for specialized tasks
- Sub-agents use **Skills** (packaged expertise) and **MCP** (external tools)
- Everything operates within **Projects** (for persistent context) or follows **workflows** (automation rules)
- **CLAUDE.md** provides guardrails for how everything should behave

**Example workflow**: An agent building a web app might:
1. Use a **design-verification sub-agent** that leverages a **Figma MCP server** and a **design-review Skill**
2. Follow **workflow rules** that auto-run tests after code changes
3. Operate within **Project** constraints defined in **CLAUDE.md**

The ecosystem is modular—use what you need based on your complexity level!

---

# Claude Ecosystem Features Comparison

| Feature | What It Is | Primary Use Case | Where Available | Context Window | Best For | Key Limitation |
|---------|-----------|------------------|-----------------|----------------|----------|----------------|
| **Agents** | Main orchestrator with feedback loops (gather context → act → verify) | Building autonomous AI systems that complete complex tasks | API, Claude Code | Manages own context | Multi-step workflows, decision-making, tool coordination | Requires development setup |
| **Sub-agents** | Specialized agents spawned by main agent with isolated contexts | Parallel task execution & context isolation | Claude Code, custom implementations | Independent 200K each | Breaking complex tasks into specialized components, parallel processing | Adds complexity, needs orchestration logic |
| **Projects** | Persistent workspace with uploaded docs & custom instructions | Organized knowledge base for ongoing work | claude.ai (web/mobile) | 200K (~500 pages) | Long-term collaboration, team workspaces, document-grounded conversations | Only on claude.ai interface |
| **Workflows** | Automation rules & event-driven triggers | Repetitive task automation | Claude Code | N/A (automation layer) | CI/CD integration, automated testing, deployment pipelines | Requires Claude Code setup |
| **Rules (CLAUDE.md)** | Configuration files auto-loaded into context | Governance & coding standards enforcement | Claude Code | Counts against session context | Ensuring consistent behavior, project guidelines, verification steps | Static text files, limited to Claude Code |
| **MCP (Model Context Protocol)** | Standardized protocol for external integrations | Connecting to external tools & data sources | API, Claude Desktop, Claude Code | Per tool/server | Database connections, third-party APIs, browser automation | Requires MCP server setup |
| **Skills** | Reusable markdown instructions with progressive disclosure | Teaching Claude specific procedures | Claude Code | Lazy-loaded (minimal upfront cost) | Team standards, reusable workflows, knowledge packaging | Currently Claude Code only |

---

## Practical Usage Examples

| Scenario | What You'd Use | Why |
|----------|---------------|-----|
| Building a full-stack app autonomously | **Agent** + **Sub-agents** + **MCP** | Agent orchestrates, sub-agents handle frontend/backend separately, MCP connects to GitHub |
| Team documentation chatbot | **Project** + **MCP** | Project holds company docs, MCP connects to Slack/Google Drive |
| Automated code review process | **Workflow** + **Skills** + **Rules** | Workflow triggers on PR, Skill defines review standards, Rules enforce requirements |
| Database query assistant | **Agent** + **MCP** | Agent interprets requests, MCP server handles DB connections |
| Maintaining coding standards | **Rules (CLAUDE.md)** | Automatically enforces style guides and verification steps |
| Parallel data processing | **Sub-agents** | Each sub-agent processes different data chunks simultaneously |
| Reusable team procedures | **Skills** | Package "how we do X" once, reuse across projects |

---

## Key Differences Summary

### **Scope**
- **Projects**: Workspace-level (all chats share context)
- **Agents/Sub-agents**: Task/session-level (runtime only)
- **Rules/Skills**: Repository/directory-level (auto-loaded)
- **MCP**: Integration-level (external connections)
- **Workflows**: Event/trigger-level (automation)

### **Persistence**
- **Projects**: ✅ Persistent across sessions
- **Rules/Skills**: ✅ Persistent (file-based)
- **Agents**: ❌ Session-only
- **MCP**: ✅ Connections persist
- **Workflows**: ✅ Automation persists

### **Parallelization**
- **Sub-agents**: ✅ Run in parallel
- **All others**: ❌ Sequential

### **Development Required**
- **Low**: Projects (web UI)
- **Medium**: MCP (install servers), Rules/Skills (write markdown)
- **High**: Agents, Sub-agents, Workflows (code implementation)

---

## Combination Patterns

| Pattern | Components | Use Case |
|---------|-----------|----------|
| **Simple Assistant** | Project only | Personal knowledge base, Q&A |
| **Team Workspace** | Project + MCP | Collaborative work with external tools |
| **Development Agent** | Agent + MCP + Rules | Autonomous coding with guardrails |
| **Enterprise System** | Agent + Sub-agents + MCP + Workflows + Skills | Full automation with specialization |
| **Standardized Team** | Rules + Skills | Enforced best practices without full agents |