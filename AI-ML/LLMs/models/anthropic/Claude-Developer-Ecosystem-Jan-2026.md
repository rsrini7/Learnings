# Complete Claude Developer Ecosystem Guide (2026)

**The Ultimate Reference for Developers, Architects, and Vibe Coders**

This comprehensive guide covers Anthropic's entire Claude ecosystem—from models and APIs to agentic workflows, developer tools, and enterprise integrations. Updated January 2026 with historical context, community best practices, and field-tested optimization strategies.

---

## Table of Contents

1. [Core Models & Pricing](#core-models--pricing)
2. [History & Evolution of Agent Features](#history--evolution-of-agent-features)
3. [Claude Code - The Flagship Developer Tool](#claude-code---the-flagship-developer-tool)
4. [Agent SDK - Build Custom Agents](#agent-sdk---build-custom-agents)
5. [Projects & Workspaces](#projects--workspaces)
6. [Skills - Modular Capabilities](#skills---modular-capabilities)
7. [Sub-Agents - Parallel Task Execution](#sub-agents---parallel-task-execution)
8. [Plugins - Shareable Extensions](#plugins---shareable-extensions)
9. [Slash Commands - Custom Shortcuts](#slash-commands---custom-shortcuts)
10. [Hooks - Lifecycle Automation](#hooks---lifecycle-automation)
11. [Ralph Loop - Autonomous Iteration](#ralph-loop---autonomous-iteration)
12. [Model Context Protocol (MCP)](#12-model-context-protocol-mcp)
13. [Session Management & Worktrees](#session-management--worktrees)
14. [Cowork - No-Code AI Assistant](#cowork---no-code-ai-assistant)
15. [APIs & Integrations](#apis--integrations)
16. [Best Practices](#best-practices)

---

## Core Models & Pricing

### Model Lineup (January 2026)

| Model | API String | Strengths | Input/Output ($/M tokens) | Release |
|-------|-----------|-----------|---------------------------|---------|
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | Fast, cost-effective; simple agents, quick code | $0.25 / $1.25 | Oct 2025 |
| **Sonnet 4.5** | `claude-sonnet-4-5-20250929` | Balanced reasoning/coding; agent orchestration, multi-agent systems | $3 / $15 | Sep 2025 |
| **Opus 4.5** | `claude-opus-4-5-20251124` | Highest intelligence; frontier coding, complex agents, token compression | $15 / $75 | Nov 2025 |

**Key Features Across Models:**
- Multimodal inputs (text, images, PDFs, code)
- Tool use and function calling
- 200K+ token context windows
- Constitutional AI safety alignments
- Streaming responses
- Vision capabilities (Sonnet 4.5+)

**Model Selection Strategy:**
- **Haiku**: Drafts, simple tasks, high-volume operations
- **Sonnet**: Default for most development work, agent orchestration
- **Opus**: Complex reasoning, production code, critical systems

---

## History & Evolution of Agent Features

Understanding how agent capabilities evolved helps you use them effectively. Here's the progression from early AI limitations to today's sophisticated systems:

### Timeline of Development

**Early Days (Pre-2025): Fighting Hallucinations**
- AI models frequently hallucinated, making up facts or generating incorrect code
- Solution: **Rules files** (like CLAUDE.md) provided static context in every conversation
- Goal: Include business requirements and common corrections to prevent repeated errors
- Limitation: Rules were static—loaded every time, regardless of relevance

**Mid-2025: Context Organization**
- Rules expanded into sub-files for better organization
- Teams wanted conditional rule inclusion, but early models had inconsistent tool-calling
- Context bloat emerged as a problem: too much static information consumed tokens
- Introduction of **slash commands** for repeatable workflows (git commits, PR creation)

**Late 2025: Dynamic Systems**
- **MCP servers** launched, allowing agents to:
  - Run full servers and execute code
  - Connect to existing systems (databases, APIs)
  - Use OAuth for third-party tools (Slack, Linear, GitHub)
- Trade-off: Many MCP tools caused context bloat
- **Sub-agents and modes** introduced for scoped tasks with limited tool access

**2026: Optimization Era**
- **Skills** emerged as the solution to context bloat:
  - Dynamic loading: Only included when needed
  - Portable: Shareable across teams via git
  - Advanced forms: Scripts, executables, and assets bundled as code
- **Hooks** added for 100% deterministic actions (vs. non-deterministic agent responses)
- Focus shifted to optimizing tool loading: activate tools only when used

### Core Conceptual Framework

Modern agent systems are built on two fundamental types of context:

**Static Context (Always Included)**
- **What**: CLAUDE.md, project rules, coding standards
- **When**: Loaded at the start of every conversation
- **Purpose**: Prevent consistent errors, establish conventions
- **Best Practice**: Keep minimal and high-quality
- **Example**: Code style guides, common corrections, project overview

**Dynamic Context (On-Demand)**
- **What**: Skills, MCP tools, sub-agents
- **When**: Loaded only when relevant to the task
- **Purpose**: Avoid token waste, extend capabilities as needed
- **Best Practice**: Use for non-essential extensions
- **Example**: Excel processing, GitHub integration, web scraping

### Key Evolution Insights

**From Static to Dynamic**: The industry moved from "include everything" to "include only what's needed right now" to optimize token usage and model performance.

**Tool Calling Maturity**: Early models couldn't reliably decide when to use tools. Modern models (Claude 4 family) have consistent tool-calling, enabling advanced features like Skills and MCP.

**Open Standards**: Skills and MCP are designed as open standards (like "USB-C for AI"), promoting ecosystem growth and portability across different AI tools.

---

## Claude Code - The Flagship Developer Tool

![AI-ML/assets/Claude-Code-Modernization.gif](../../../assets/Claude-Code-Modernization.gif)

Refer to : [Using Claude Code to Modernize Legacy Codebases](https://newsletter.rakeshgohel.com/p/using-claude-code-to-modernize-legacy-codebases)

---

![AI-ML/assets/Claude-Code-Cheatsheet.png](../../../assets/Claude-Code-Cheatsheet.png)

Refer to : [ClaudeCode Mastery Handbook](https://github.com/hamodywe/ClaudeCode-Mastery-Handbook)

---

### Overview

**Claude Code** is an agentic coding assistant that runs in your terminal, understanding your codebase and autonomously executing development tasks. Launched February 2025, it reached $1B+ ARR and is used internally at Anthropic for 80% of tech tasks.

### Core Capabilities

**Built-in Tools:**
- **Read** - Read any file in working directory
- **Write** - Create new files
- **Edit** - Precise edits to existing files
- **Bash** - Run terminal commands
- **Glob** - Find files by pattern
- **Grep** - Search file contents
- **WebSearch** - Search the internet
- **Task** (sub-agents) - Delegate to specialized agents

### Installation

```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Node.js/NPM (alternative)
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

### Authentication

```bash
# Interactive authentication (recommended)
claude

# API key authentication
export ANTHROPIC_API_KEY="your-key-here"
claude

# Third-party providers
export CLAUDE_CODE_USE_BEDROCK=1  # AWS Bedrock
export CLAUDE_CODE_USE_VERTEX=1   # Google Vertex AI
export CLAUDE_CODE_USE_FOUNDRY=1  # Microsoft Foundry
```

### Usage Modes

**1. Interactive Mode**
```bash
# Start in current directory
claude

# Start with specific model
claude --model opus

# Plan mode (review before execution)
claude --permission-mode plan

# Auto-accept edits
claude --permission-mode acceptEdits

# Headless/background mode
claude --permission-mode bypassPermissions --dangerously-skip-permissions
```

**2. One-Shot Mode**
```bash
# Execute single prompt
claude -p "Create a hello.py file that prints 'Hello World'"

# With file context
claude -p "Add unit tests for utils.py"

# Chain commands
claude -p "Refactor auth.js" && git commit -am "Refactored auth"
```

**3. Background Mode**
```bash
# Start remote session
claude --remote &

# Resume session
claude --resume session-name

# Teleport between local/web
/teleport  # from CLI to claude.ai/code
```

### Configuration Files and Memory Hierarchy

#### The Memory Hierarchy for CLAUDE.md

Claude Code loads CLAUDE.md files in a specific order, allowing layered instructions from enterprise to personal levels:

| Level | Location | Purpose |
|-------|----------|---------|
| **Enterprise** | `/etc/claude-code/CLAUDE.md` | Org-wide policies |
| **Global User** | `~/.claude/CLAUDE.md` | Your standards for ALL projects |
| **Project** | `./CLAUDE.md` | Team-shared project instructions |
| **Project Local** | `./CLAUDE.local.md` | Personal project overrides |

This hierarchy ensures consistent application of rules across environments.

#### CLAUDE.md - Project Memory/Instructions (Static Context)

**Basic Example:**
```markdown
# Project Overview
This is a Next.js e-commerce platform using TypeScript and Tailwind.

## Code Style
- Use functional components with hooks
- Prefer named exports
- Follow Airbnb style guide
- All tests in __tests__ directories

## Common Commands
- `npm run dev` - Start dev server
- `npm test` - Run tests
- `npm run build` - Production build

## Known Issues
- Auth middleware sometimes fails on cold starts
- Database migrations require manual review
```

#### Global CLAUDE.md as Security Gatekeeper

Your global `~/.claude/CLAUDE.md` applies to every project and serves as a behavioral gatekeeper, especially since Claude can automatically read sensitive files like `.env` without explicit permission. Include absolute rules to prevent leaks:

```markdown
## NEVER EVER DO
These rules are ABSOLUTE:

### NEVER Publish Sensitive Data
NEVER publish passwords, API keys, tokens to git/npm/docker
Before ANY commit: verify no secrets included

### NEVER Commit .env Files
NEVER commit `.env` to git
ALWAYS verify `.env` is in `.gitignore`
```

**Why this matters:** Security research shows Claude may access and potentially leak secrets from `.env`, AWS credentials, or similar files. These rules create a "behavioral gatekeeper" that Claude follows even if it has file access.

#### Syncing Global CLAUDE.md Across Machines

For multi-machine workflows, sync your `~/.claude/` directory using a dotfiles manager:

```bash
# Using GNU Stow
cd ~/dotfiles
stow claude
# Symlinks ~/.claude to dotfiles/claude/.claude
```

Benefits: Version control, consistent configuration, and easy recovery.

#### Global Rules for New Project Scaffolding

Turn your global CLAUDE.md into a "project factory" for automatic standards in new projects:

```markdown
## New Project Setup
When creating ANY new project:

### Required Files
`.env` — Environment variables (NEVER commit)
`.env.example` — Template with placeholders
`.gitignore` — Must include: .env, node_modules/, dist/
`CLAUDE.md` — Project overview

### Required Structure
project/
├── src/
├── tests/
├── docs/
├── .claude/skills/
└── scripts/

### Node.js Requirements
Add to entry point:
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  process.exit(1);
});
```

This ensures every "create new project" prompt inherits your standards, reducing scope creep and maintaining quality.

#### Team Workflows: Evolving CLAUDE.md

Adopt Anthropic's internal pattern: Treat CLAUDE.md as living documentation. When Claude makes a mistake, fix it and add a rule to CLAUDE.md to prevent recurrence. This embodies "Compounding Engineering," where each fix makes future work easier.

#### settings.json - Tool Permissions & Preferences

```json
{
  "allowedTools": ["Read", "Edit", "Write", "Bash", "WebSearch"],
  "enableThinking": true,
  "respectGitignore": true,
  "autoSave": true,
  "maxTokens": 8000
}
```

#### .claude.json - MCP Servers & Advanced Config

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Permission Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `normal` | Approve each action | Learning, careful review |
| `acceptEdits` | Auto-approve file edits | Trusted refactoring |
| `plan` | Review plan before execution | Complex features |
| `bypassPermissions` | No approvals (⚠️ risky) | Trusted environments, CI/CD |

### Key Features (v2.1.0 - January 2026)

- **Session Teleportation** (`/teleport`) - Move sessions between CLI and web
- **Hot-Reload Skills** - Skills update without restarting
- **Forked Sub-Agent Context** - Isolated skill execution
- **Wildcard Tool Permissions** - `Bash(npm *)` pattern matching
- **Real-Time Thinking Display** - `Ctrl+O` transcript mode
- **Multilingual Output** - Language-specific responses
- **Vim Motions** - Full Vim keybindings in editor
- **Session History** - Resume any past conversation
- **LSP Integration** (New in 2026) - Language Server Protocol support for IDE-level code intelligence: go-to-definition, find-references, diagnostics. Enables 900x faster navigation and semantic understanding.

### Why Single-Purpose Chats Are Critical

Research shows mixing topics causes a 39% performance drop and context rot. Follow the "One Task, One Chat" rule:

| Scenario | Action |
|----------|--------|
| New feature | New chat |
| Research vs implementation | Separate chats |
| 20+ turns elapsed | Start fresh |

Use `/clear` frequently to reset context.

---

## Agent SDK - Build Custom Agents

### Overview

The **Claude Agent SDK** (formerly Claude Code SDK) lets you programmatically build AI agents with Claude Code's capabilities. Available in Python and TypeScript, it powers autonomous agents that read files, run commands, and execute complex workflows.

### Installation

**Python:**
```bash
pip install claude-agent-sdk

# Verify Claude Code is installed
claude --version
```

**TypeScript:**
```bash
npm install @anthropic-ai/claude-agent-sdk

# Or with Yarn
yarn add @anthropic-ai/claude-agent-sdk
```

### Basic Usage

**Python:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # Simple query
    async for message in query(prompt="What is 2 + 2?"):
        print(message)
    
    # With options
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Bash"],
        permission_mode="acceptEdits",
        system_prompt="You are a senior Python engineer.",
        max_turns=10
    )
    
    async for message in query(
        prompt="Fix bugs in utils.py and add tests",
        options=options
    ):
        if message.type == "result":
            print(message.result)

asyncio.run(main())
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  for await (const message of query({
    prompt: "Review TypeScript files for bugs",
    options: {
      allowedTools: ["Read", "Edit", "Glob"],
      permissionMode: "acceptEdits",
      systemPrompt: "You are a TypeScript expert.",
      cwd: "./src"
    }
  })) {
    if (message.type === "result") {
      console.log(message.result);
    }
  }
}

main();
```

### Advanced Features

**Custom Tools (In-Process MCP):**
```python
from claude_agent_sdk import ClaudeSDKClient

client = ClaudeSDKClient()

# Define custom tool
@client.tool
async def fetch_weather(location: str) -> dict:
    # Your implementation
    return {"temp": 72, "condition": "sunny"}

# Use in conversation
response = await client.send("What's the weather in SF?")
```

**Bidirectional Conversations:**
```typescript
import { ClaudeSDKClient } from "@anthropic-ai/claude-agent-sdk";

const client = new ClaudeSDKClient();

// Multi-turn conversation
await client.send("Refactor the auth module");
await client.send("Now add TypeScript types");
await client.send("Run the tests");
```

**File System Integration:**
```python
from pathlib import Path

options = ClaudeAgentOptions(
    cwd=Path("/path/to/project"),
    setting_sources=["project"]  # Load CLAUDE.md
)
```

### Key Differences from Raw API

| Feature | Raw API | Agent SDK |
|---------|---------|-----------|
| Agent loop | Manual implementation | Automatic |
| Tool execution | You implement | Built-in |
| Context management | Manual tracking | Automatic |
| File operations | Custom code | Native tools |
| Session persistence | External storage | CLAUDE.md integration |

---

## Projects & Workspaces

### Claude Projects (Web/App)

**Projects** are customized workspaces in claude.ai with persistent context, knowledge bases, and custom instructions.

**Features:**
- Upload up to 200MB of documents (Pro/Max)
- Custom instructions per project
- Conversation history preservation
- Cross-session memory
- Team sharing (Team/Enterprise)

**Use Cases:**
- Research & knowledge management
- Code review with project context
- Documentation analysis
- Customer support with company docs
- Content creation with style guides

**Setup:**
1. Click "Projects" in claude.ai sidebar
2. Create new project with name/description
3. Upload documents (PDFs, code, markdown)
4. Set custom instructions
5. Start conversations with full context

**Free vs Paid:**
- **Free**: 5 projects, 10MB per project
- **Pro**: 50 projects, 200MB per project, RAG
- **Team**: Shared projects, team knowledge bases

### Claude Code Projects

Projects in Claude Code are **directory-based** with per-project configuration.

**Project Structure:**
```
my-project/
├── .claude/
│   ├── commands/       # Custom slash commands
│   ├── skills/         # Project-specific skills
│   ├── agents/         # Sub-agent definitions
│   └── hooks/          # Lifecycle hooks
├── .claude.json        # MCP servers, tool permissions
├── CLAUDE.md           # Project context & instructions
└── settings.json       # Tool allowances
```

**Project-Level vs Global:**
- **Project**: `.claude/` configs in repo (team-shared via git)
- **Global**: `~/.claude/` configs (personal preferences)

---

## Skills - Modular Capabilities


### Overview

**Skills** are reusable packages (folder with instructions + resources) that give Claude specialized capabilities. They represent **dynamic context**—loaded only when needed to avoid token bloat—and are portable across Claude Code, API, and claude.ai.

### Conceptual Foundation

Skills evolved as the solution to MCP's context bloat problem:

**The Context Bloat Challenge:**
- Early implementations loaded all available tools at conversation start
- Example: 10 MCP servers with 5 tools each = 50 tools in initial context
- Result: Wasted tokens, slower responses, higher costs

**Skills Solution:**
- **On-Demand Loading**: Skills activate only when relevant to the task
- **Tool Optimization**: If a skill has 10 MCP tools, only used tools are loaded
- **Bundled Resources**: Scripts, executables, assets included in skill package
- **Open Standard**: Shareable via git, portable across AI tools

### Structure

```
my-skill/
├── skill.md            # Main instructions (required)
├── script.py           # Helper scripts (optional)
├── config.json         # Configuration (optional)
└── resources/          # Additional files (optional)
```

**skill.md Frontmatter:**
```markdown
---
description: Process Excel files and generate reports
category: data-analysis
dependencies: 
  - pandas
  - openpyxl
allowed-tools:
  - Read
  - Write
  - Bash(python *)
context: fork  # Run in isolated context
user-invocable: true
---

# Excel Analysis Skill

When the user provides an Excel file, follow these steps:

1. Read the file using pandas
2. Analyze data structure
3. Generate summary statistics
4. Create visualizations
5. Export report

## Examples

User: "Analyze sales.xlsx"
Claude: *reads file, analyzes, generates report*
```

### Merged Commands and Skills

As of late 2025, commands and skills share the same schema for a simpler mental model:

- Old: Commands in `~/.claude/commands/review.md`
- New: Skills in `~/.claude/skills/review/SKILL.md`

**Key Difference:**
- Slash commands (e.g., `/review`) are explicitly invoked.
- Skills can trigger automatically based on context.

Format for SKILL.md:

```markdown
---
name: review
description: Review code for bugs and security issues
---
# Code Review Skill
When reviewing code:
1. Check for security vulnerabilities
2. Look for performance issues
3. Verify error handling
```

### Progressive Disclosure for Token Efficiency

Skills load content on-demand:
1. Startup: Only name/description.
2. Triggered: Full SKILL.md.
3. As needed: Additional resources.

**Rule of thumb:** If instructions apply to <20% of conversations, use a skill instead of CLAUDE.md to avoid context bloat.

### Skill Types and Forms

**Basic Skills (Command-Like):**
- Simple workflows executed as repeatable prompts
- Example: Git PR workflow, code formatting
- Similar to slash commands but with dynamic loading

**Advanced Skills (Bundled Capabilities):**
- Combination of scripts, executables, and assets
- Dependencies and configurations included
- Example: Data pipeline with Python scripts, SQL schemas, sample data
- Distributed as code packages

### Pre-Built Skills

**Official Anthropic Skills:**
- **pptx** - PowerPoint creation/editing
- **xlsx** - Excel spreadsheet manipulation
- **docx** - Word document generation
- **pdf** - PDF processing and extraction
- **data-analysis** - Statistical analysis
- **web-scraping** - Extract web data

**Community Skills:**
- **github-workflow** - Automate GitHub actions
- **docker-compose** - Container orchestration
- **terraform** - Infrastructure as code
- **api-testing** - Automated API validation
- **oauth-integration** - Handle authentication flows (OAuth/OOTH support)
- **parallel-research** - Delegate sub-tasks like web research
- **sql-query** - Database operations
- **pixel-art-editor** - Creative tools with bundled assets

### Skills vs Other Features

| Feature | Type | When Loaded | Use Case |
|---------|------|-------------|----------|
| **Rules (CLAUDE.md)** | Static | Every conversation | Consistent guidance, error prevention |
| **Skills** | Dynamic | On-demand | Reusable workflows, code execution |
| **MCP Servers** | Dynamic (code-based) | On-demand | Third-party integrations, OAuth |
| **Sub-Agents** | Scoped dynamic | Task-specific | Parallel execution, limited tools |
| **Slash Commands** | Static prompt | User-invoked | Quick shortcuts, team conventions |

### Using Skills

**In Claude Code:**
```bash
# Auto-detected based on task
claude -p "Create a sales report from data.xlsx"
# Claude automatically uses xlsx skill

# Explicitly invoke
/skills/excel-analysis @data.xlsx
```

**Via API:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    skills=["xlsx", "data-analysis"]
)

async for msg in query(
    prompt="Analyze Q4 sales data",
    options=options
):
    print(msg)
```

### Creating Custom Skills

**1. Create Skill Directory:**
```bash
mkdir -p ~/.claude/skills/my-custom-skill
```

**2. Write skill.md:**
```markdown
---
description: Custom API testing framework
allowed-tools:
  - Bash(curl *)
  - Read
  - Write
context: fork  # Isolated execution
---

# API Testing Skill

Test REST APIs with automatic validation...
```

**3. Upload via Skills API:**
```python
import requests

response = requests.post(
    "https://api.anthropic.com/v1/skills",
    headers={"x-api-key": "your-key"},
    json={
        "name": "my-custom-skill",
        "files": {...}
    }
)
```

### Skill Best Practices

- **Scope**: One skill = one specialized task
- **Token Efficiency**: Keep instructions concise (30-50 tokens awareness cost)
- **Context**: Use `context: fork` for isolation (prevents main agent pollution)
- **Dependencies**: Document clearly in frontmatter
- **Examples**: Include 2-3 usage examples for better AI understanding
- **Versioning**: Maintain backward compatibility
- **Shareable**: Design for team distribution via git
- **Optimization**: Bundle related functionality to minimize skill loading overhead

### Skills and Open Ecosystem

Skills are designed as an **open standard** for the AI agent ecosystem:
- **Portability**: Same skill works in Claude Code, API, other AI tools (future)
- **Distribution**: Share via GitHub, npm, package managers
- **Community Growth**: Expected to become dominant pattern in 2026+
- **Future-Proof**: As AI tools standardize, skills become universal capabilities

Refer to :  [Awesome Claude Skills](https://github.com/ComposioHQ/awesome-claude-skills) for a curated list of skills.

---

## Sub-Agents - Parallel Task Execution

### Overview

**Sub-agents** are specialized AI assistants that handle specific tasks in parallel or with isolated context. They evolved from early "modes" to make agent behavior more reliable, discoverable, and consistent. Sub-agents enable multi-agent architectures where a lead agent delegates to worker specialists.

### Historical Context

**Evolution from Modes:**
- Early AI agents struggled with complex tasks requiring multiple perspectives
- "Modes" introduced system prompt modifications for focused behavior
- Sub-agents extended this with: isolated context, limited tool access, persona definitions
- Goal: Reliability through specialization and discoverability through clear interfaces

### Core Features

**Specialization Capabilities:**
- **Scoped Context**: Forked or isolated execution (as in skills' `context: fork`)
- **Tool Limitations**: Restrict to specific tools (e.g., only Bash for scripts)
- **Modes Integration**: Modify system prompts and UI (e.g., "planning mode" with reminders like "Focus on outlining before coding")
- **Parallel Execution**: Run multiple sub-agents simultaneously
- **Persona-Based**: Each sub-agent has specialized expertise

### Built-In Sub-Agents

**Explore** - Research and information gathering
```bash
/task explore "Find best practices for React 19 Server Components"
```

**Plan** - Strategic planning and architecture
```bash
/task plan "Design a microservices architecture for e-commerce"
```

### Custom Sub-Agents

**agents/researcher.json:**
```json
{
  "name": "researcher",
  "description": "Deep research specialist",
  "systemPrompt": "You are a research expert. Always cite sources and provide comprehensive analysis.",
  "allowedTools": ["WebSearch", "Read", "Write"],
  "model": "claude-sonnet-4-5-20250929",
  "mode": "research",
  "maxTurns": 20
}
```

**agents/security-auditor.md:**
```markdown
---
name: security-auditor
description: Security vulnerability scanner
persona: Senior security engineer with OWASP expertise
allowed-tools:
  - Read
  - Bash(npm audit)
  - Bash(bandit *)
context: fork
mode: audit
---

# Security Auditor Sub-Agent

## Instructions
Perform comprehensive security audits:
1. Scan dependencies for known vulnerabilities
2. Check for common security anti-patterns
3. Review authentication/authorization logic
4. Identify injection risks (SQL, XSS, etc.)
5. Report findings with severity levels

## Mode Behavior
In "audit" mode, focus exclusively on security without suggesting feature improvements.
```

**Usage:**
```bash
# Invoke custom agent
/task researcher "Research quantum computing trends"

# Parallel execution
/task researcher "Study GraphQL vs REST" &
/task researcher "Analyze microservices patterns" &
wait

# With specific mode
/task security-auditor "Audit authentication system"
```

### Modes and UI Integration

**What Modes Do:**
- **System Prompt Modifications**: Change agent behavior for specific contexts
- **UI Reminders**: Display persistent reminders (e.g., "Planning phase: Focus on architecture")
- **Tool Filtering**: Further restrict available tools based on mode
- **Discoverable Workflows**: Users can select modes from UI, making capabilities clear

**Example Mode Configuration:**
```json
{
  "mode": "planning",
  "systemPromptAddition": "You are in planning mode. Focus on high-level architecture and design decisions. Do not write implementation code yet.",
  "uiReminder": "📋 Planning Mode: Outline before implementing",
  "allowedTools": ["Read", "WebSearch", "Write(*.md)"]
}
```

### Multi-Agent Patterns

**1. Manager-Worker:**
```python
# Manager agent
main_agent = query(
    prompt="Build a full-stack app",
    options={"allowed_tools": ["Task", "Read", "Write"]}
)

# Manager delegates:
# - Backend agent: API development
# - Frontend agent: UI components
# - DevOps agent: Docker/CI setup
```

**2. Specialist Team:**
```bash
# Security agent
/task security "Audit authentication flow"

# Performance agent
/task performance "Optimize database queries"

# Testing agent
/task testing "Generate e2e tests"

# Documentation agent
/task docs "Update API documentation"
```

**3. Research Synthesis:**
```markdown
---
# agents/synthesis.json
{
  "name": "synthesis",
  "systemPrompt": "Combine research from multiple sources into coherent report",
  "allowedTools": ["Read", "Write"],
  "context": "shared"
}
---
```

### Sub-Agent Context Management

**Isolated Context (Forked):**
```markdown
---
context: fork  # in skill/agent frontmatter
---
```
- No main agent pollution
- Safe for experimental logic
- Parallel execution without conflicts
- Each sub-agent has independent conversation history

**Shared Context:**
```markdown
---
context: shared
---
```
- Access to main conversation
- Builds on prior work
- Sequential dependencies
- Useful for synthesis or follow-up tasks

### Use Cases by Type

**Parallel Tasks (Forked Context):**
- Research multiple topics simultaneously
- Code reviews across different modules
- Testing different approaches
- Data gathering from multiple sources

**Sequential Tasks (Shared Context):**
- Implement → Test → Document workflow
- Research → Summarize → Present pipeline
- Plan → Build → Deploy sequence
- Design → Code → Review process

### Best Practices for Sub-Agents

**DO:**
- ✅ Use for well-defined, scoped tasks
- ✅ Limit tools to minimum needed
- ✅ Default to out-of-box sub-agents (explore, plan) first
- ✅ Fork context for parallel execution
- ✅ Name sub-agents descriptively

**DON'T:**
- ❌ Create too many sub-agents (complexity overhead)
- ❌ Share context when tasks are independent
- ❌ Give sub-agents access to all tools
- ❌ Use for tasks requiring human judgment
- ❌ Nest sub-agents too deeply (3+ levels)

---

## Plugins - Shareable Extensions

### Overview

**Plugins** are collections of slash commands, agents, skills, MCP servers, and hooks bundled for easy sharing and installation.

### Plugin Components

A plugin can include any combination of:
- **Slash Commands** - Custom shortcuts
- **Sub-Agents** - Specialized agents
- **MCP Servers** - Tool integrations
- **Hooks** - Lifecycle automation
- **Skills** - Reusable capabilities

### Installing Plugins

**1. Add Marketplace:**
```bash
# Official Anthropic marketplace
/plugin marketplace add anthropics/claude-plugins-official

# Community marketplace
/plugin marketplace add username/marketplace-repo
```

**2. Browse Plugins:**
```bash
/plugin discover
# Tab to explore available plugins
```

**3. Install Plugin:**
```bash
# From marketplace
/plugin install ralph-wiggum@claude-plugins-official

# From GitHub repo
/plugin install username/repo-name

# Specific version
/plugin install ralph-wiggum@v1.2.0
```

**4. Manage Plugins:**
```bash
# List installed
/plugin list

# Update all
/plugin update

# Remove
/plugin remove ralph-wiggum
```

### Creating Plugins

**Directory Structure:**
```
my-plugin/
├── plugin.json         # Metadata
├── commands/           # Slash commands
├── agents/             # Sub-agents
├── skills/             # Skills
├── hooks/              # Hooks
└── mcp/                # MCP server configs
```

**plugin.json:**
```json
{
  "name": "my-awesome-plugin",
  "version": "1.0.0",
  "description": "Does awesome things",
  "author": "Your Name",
  "license": "MIT",
  "components": {
    "commands": ["./commands/"],
    "agents": ["./agents/"],
    "skills": ["./skills/"],
    "hooks": ["./hooks/"]
  }
}
```

### Publishing Plugins

**1. Create GitHub Repo:**
```bash
git init my-plugin
cd my-plugin
# Add plugin files
git add .
git commit -m "Initial plugin"
git push origin main
```

**2. Tag Release:**
```bash
git tag v1.0.0
git push --tags
```

**3. Submit to Marketplace:**
```bash
# Fork anthropics/claude-plugins-official
# Add your plugin to marketplaces/community.json
# Submit PR
```

### Popular Plugins

**Development:**
- **ralph-wiggum** - Autonomous iteration loops
- **tdd-guard** - Test-driven development enforcement
- **code-review** - Automated PR reviews
- **lsp-integration** - Language server protocol

**DevOps:**
- **docker-workflow** - Container management
- **k8s-helper** - Kubernetes operations
- **terraform-agent** - IaC automation

**Data:**
- **sql-wizard** - Database operations
- **data-pipeline** - ETL workflows
- **analytics-suite** - Data analysis

---

## Slash Commands - Custom Shortcuts

### Overview

**Slash commands** are custom shortcuts for frequently-used prompts, stored as Markdown files that Claude Code executes. They represent team conventions and personal workflows as reusable, discoverable actions.

### Conceptual Understanding

Slash commands evolved as a way to:
- **Package Prompts**: Turn repeated workflows into one-command actions
- **Share with Teams**: Encode team standards in version control
- **Discover Capabilities**: Auto-complete shows available commands
- **Reduce Friction**: Execute complex prompts instantly

### Command Scopes

**Project Commands** (`.claude/commands/`)
- Shared with team via git
- Project-specific workflows
- Listed as `(project)` in `/help`

**Personal Commands** (`~/.claude/commands/`)
- Your global shortcuts
- Available in all projects
- Private preferences

**Plugin Commands**
- Installed from plugins
- Discoverable via `/plugin discover`

### Creating Commands

**Basic Command:**
```bash
# .claude/commands/optimize.md
---
description: Analyze code for performance issues
---

Review the current file or specified files for:
- Inefficient algorithms
- Memory leaks
- Unnecessary computations
- Database query optimization opportunities

Provide specific recommendations with code examples.
```

**Usage:**
```bash
/optimize auth.js
```

**With Arguments:**
```bash
# .claude/commands/test.md
---
description: Generate tests with coverage target
---

Generate comprehensive tests for $ARGUMENTS.
Aim for >80% code coverage.
Include unit, integration, and edge case tests.
```

**Usage:**
```bash
/test utils.py
```

### Advanced Command Features

**Hooks in Commands:**
```markdown
---
description: Deploy to staging with validation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-deploy.sh"
          once: true
---

Deploy the current branch to staging environment.
```

**MCP-Based Commands:**
```bash
# Commands from MCP servers are auto-discovered
/mcp__github__create_pr "Add new feature" main
/mcp__jira__create_issue "Bug fix needed" high
```

**Namespaced Commands:**
```
.claude/commands/
├── api/
│   ├── test.md
│   └── deploy.md
└── db/
    ├── migrate.md
    └── backup.md
```

**Usage:**
```bash
/api/test
/db/migrate
```

### Command Best Practices

- **Descriptive Names**: `/refactor-for-testing` not `/r`
- **Clear Descriptions**: Users see these in autocomplete
- **Argument Flexibility**: Use `$ARGUMENTS` for dynamic input
- **Documentation**: Include examples in command
- **Team Standards**: Project commands encode team conventions

---

## Hooks - Lifecycle Automation

### Overview

**Hooks** are event-driven automations that run at specific points in Claude Code's workflow. They provide **100% deterministic** code execution at lifecycle events—unlike non-deterministic agent responses—enabling validation, formatting, notifications, and workflow enforcement.

### Conceptual Foundation

**Why Hooks Exist:**
- AI agents are non-deterministic: you can't guarantee specific actions
- Some workflows need guaranteed execution (e.g., security checks, formatting)
- Hooks bridge the gap: inject deterministic actions into agent lifecycle

**Use Cases:**
- **Pre-Conversation**: Inject static context, log session starts
- **Post-Tool-Use**: Auto-format code, run linters
- **Pre-Tool-Use**: Security scanning, permission checks
- **On-Error**: Automated recovery, logging
- **Post-Conversation**: Save outputs, database logging, cleanup

### Hook Types (9 Lifecycle Events)

1. **SessionStart** - When Claude Code session begins
2. **UserPromptSubmit** - After user sends prompt
3. **PreToolUse** - Before any tool execution
4. **PostToolUse** - After tool execution
5. **Stop** - When Claude tries to exit
6. **Notification** - System notifications
7. **Error** - Error handling
8. **Success** - Task completion
9. **AgentLifecycle** - Agent state changes

### Hook Configuration

**In settings.json:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $FILE"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./security-check.sh $COMMAND",
            "once": false
          }
        ]
      }
    ]
  }
}
```

### Hooks for Deterministic Enforcement

Unlike CLAUDE.md rules (suggestions that can be overridden), hooks are deterministic and always execute.

Hook Events:

| Event | When | Use Case |
|-------|------|----------|
| PreToolUse | Before tool executes | Block dangerous ops |
| PostToolUse | After tool completes | Run linters |
| Stop | Claude finishes turn | Quality gates |

Example: Block secrets access in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/block-secrets.py"
          }
        ]
      }
    ]
  }
}
```

Hook script (`block-secrets.py`):

```python
#!/usr/bin/env python3
import json, sys
from pathlib import Path

SENSITIVE = {'.env', '.env.local', 'secrets.json', 'id_rsa'}
data = json.load(sys.stdin)
tool = data.get('tool', {})
if 'path' in tool and Path(tool['path']).name in SENSITIVE:
    sys.exit(1)  # Block access
sys.exit(0)
```

### Common Hook Patterns

**1. Auto-Formatting:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit.*\\.py$",
        "hooks": [
          {
            "type": "command",
            "command": "ruff format $FILE || true"
          }
        ]
      },
      {
        "matcher": "Edit.*\\.(ts|tsx)$",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $FILE || true"
          }
        ]
      }
    ]
  }
}
```

**2. Security Scanning:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*npm install",
        "hooks": [
          {
            "type": "command",
            "command": "npm audit || echo 'Warning: vulnerabilities found'"
          }
        ]
      }
    ]
  }
}
```

**3. Test Execution:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit.*test\\.py$",
        "hooks": [
          {
            "type": "command",
            "command": "pytest $FILE -v"
          }
        ]
      }
    ]
  }
}
```

**4. Git Integration:**
```json
{
  "hooks": {
    "Success": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git add -A && git commit -m 'Claude Code changes'"
          }
        ]
      }
    ]
  }
}
```

**5. Static Context Injection:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat .claude/context/project-state.md"
          }
        ]
      }
    ]
  }
}
```

**6. Post-Conversation Logging:**
```json
{
  "hooks": {
    "Success": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/log-conversation.py $SESSION_ID"
          }
        ]
      }
    ]
  }
}
```

### Hook Matchers

**Tool Matchers:**
- `Edit` - Any file edit
- `Bash` - Any bash command
- `Edit.*\\.js# Complete Claude Developer Ecosystem Guide (2026)
- JavaScript files
- `Bash(npm *)` - NPM commands (wildcard)

**Advanced Patterns:**
```json
{
  "matcher": "Edit.*src/.*\\.ts$",  // TypeScript in src/
  "matcher": "Bash(docker-*)",       // Docker commands
  "matcher": "Write.*\\.json$"       // JSON file creation
}
```

### Interactive Hooks via `/hooks`

```bash
# Interactive hook configuration
/hooks

# Available options:
# - Add PreToolUse hook
# - Add PostToolUse hook  
# - Add Stop hook
# - View current hooks
# - Remove hook
```

### Hooks Best Practices

**DO:**
- ✅ Use for deterministic requirements (formatting, security)
- ✅ Keep hook commands fast (avoid blocking agent)
- ✅ Include error handling (`|| true` for non-critical)
- ✅ Document hook purposes in comments
- ✅ Test hooks independently before deploying

**DON'T:**
- ❌ Use for logic that should be in agent prompts
- ❌ Create circular dependencies (hook triggers hook)
- ❌ Block on user input in hooks
- ❌ Assume hooks always succeed (handle failures)
- ❌ Overuse (keep to essential automations)

---

## Ralph Loop - Autonomous Iteration

### Overview

**Ralph Wiggum** (named after the Simpsons character) is a development methodology based on continuous AI agent loops. It allows Claude to iteratively improve work until truly complete, preventing premature exits. Ralph uses a **Stop hook** to intercept Claude's exit attempts and re-feed the prompt, enabling continuous refinement.

### How It Works

Ralph uses a **Stop hook** to intercept Claude's exit attempts and re-feed the same prompt, enabling continuous refinement:

```
You: /ralph-loop "Implement auth system" --max-iterations 20

[Iteration 1]
Claude: *implements basic auth*
Stop hook: *checks for completion signal - not found*
Stop hook: "Continue working"

[Iteration 2]  
Claude: *reviews own work, finds issues*
Claude: *fixes session handling*
Stop hook: *checks completion - not found*
Stop hook: "Keep going"

[Iteration N]
Claude: *tests pass, all requirements met*
Claude: "Authentication complete. <promise>DONE</promise>"
Stop hook: *found "DONE" - exit loop*
```

### Installation

**Official Plugin:**
```bash
/plugin marketplace add anthropics/claude-plugins-official
/plugin install ralph-wiggum@claude-plugins-official
```

**Community Version (Advanced):**
```bash
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code
./install.sh
```

### Basic Usage

**Simple Task:**
```bash
/ralph-loop "Fix all ESLint errors" --max-iterations 10 --completion-promise "CLEAN"
```

**Complex Feature:**
```bash
/ralph-loop "Build complete user authentication system with tests" \
  --max-iterations 50 \
  --completion-promise "COMPLETE"
```

**With Detailed Prompt:**
```bash
/ralph-loop "
Create a REST API for todos:
- CRUD endpoints (GET/POST/PUT/DELETE)
- Input validation
- Error handling
- Unit tests (>80% coverage)
- API documentation

Output <promise>API_READY</promise> when:
- All endpoints working
- Tests passing
- README with examples
" --max-iterations 30
```

### Advanced Features

**Phased Development:**
```bash
# Phase 1: Models
/ralph-loop "Create database models. Output <promise>MODELS_DONE</promise>" \
  --max-iterations 15

# Phase 2: API
/ralph-loop "Build API layer. Output <promise>API_DONE</promise>" \
  --max-iterations 20

# Phase 3: Tests
/ralph-loop "Write comprehensive tests. Output <promise>TESTS_DONE</promise>" \
  --max-iterations 25
```

**Overnight Work:**
```bash
#!/bin/bash
# overnight-tasks.sh

cd ~/project1
claude -p "/ralph-loop 'Implement feature A' --max-iterations 50"

cd ~/project2  
claude -p "/ralph-loop 'Refactor module B' --max-iterations 40"

cd ~/project3
claude -p "/ralph-loop 'Add test coverage' --max-iterations 30"
```

**With Custom Timeout:**
```bash
# Community version with advanced options
ralph --monitor --timeout 60 --calls 50
```

### Ralph Best Practices

**DO:**
- ✅ Set `--max-iterations` (required safety net)
- ✅ Use clear completion promises
- ✅ Include success criteria in prompt
- ✅ Test in git-tracked directories
- ✅ Monitor first runs closely
- ✅ Use for mechanical, well-defined tasks

**DON'T:**
- ❌ Rely solely on `--completion-promise` (use max-iterations)
- ❌ Use for exploratory/research tasks
- ❌ Leave unattended without iteration limits
- ❌ Expect perfect results every time
- ❌ Use for judgment-heavy decisions

### Cost Considerations

Ralph loops can consume significant tokens:
- 50-iteration loop on large codebase: $50-100+ API costs
- Team subscriptions: Faster usage limit depletion
- Recommendation: Start with 10-20 iterations, increase as needed

### Success Patterns

**Works Best For:**
- Large refactors with clear patterns
- Test coverage generation
- Documentation writing
- Code style enforcement
- Batch operations
- Linting/fixing errors

**Less Suitable For:**
- Creative design decisions
- Architecture choices
- Research and exploration
- Ambiguous requirements
- Human judgment calls

---

## Model Context Protocol (MCP)

### Overview

**MCP** (Model Context Protocol) is an open protocol—often described as "USB-C for AI"—that standardizes how AI applications connect to external tools and data sources. It enables Claude to access databases, APIs, filesystems, and enterprise tools through a uniform interface.

### Conceptual Foundation

**The Standardization Problem MCP Solves:**
- Before MCP: Every AI tool had custom integrations (N tools × M apps = N×M implementations)
- With MCP: Standardized protocol (N tools + M apps with MCP = N+M implementations)
- Similar to USB-C: One connector for all devices

**MCP's Role in the Ecosystem:**
- **Skills** use MCP servers as underlying tools
- **MCP servers** provide the raw capabilities
- **Dynamic loading** prevents context bloat
- **OAuth/OOTH support** enables secure third-party integrations

### Architecture

```
┌─────────────────┐
│  Host (Claude)  │
│                 │
│  ┌───────────┐  │
│  │MCP Client│  │
│  └──────┬────┘  │
└────────┼────────┘
         │
         │ MCP Protocol
         │
    ┌────┴────┬────────┬─────────┐
    │         │        │         │
┌───┴──  ┌───┴───┐ ┌──┴───┐ ┌───┴────┐
│GitHub│  │Slack │ │Drive │ │Postgres│
└──────┘  └──────┘ └──────┘ └────────┘
  MCP       MCP      MCP       MCP
 Server    Server   Server    Server
```

### When NOT to Use MCP Servers

MCP servers extend capabilities but consume tokens and context. For simple or one-off tasks, alternatives are more efficient:

| Use Case | MCP Overhead | Alternative |
|----------|--------------|-------------|
| Trello tasks | High | CLI tool (e.g., `trello-cli`) |
| Simple HTTP calls | Overkill | `curl` via Bash |
| One-off queries | Wasteful | Direct command |

**Rule of thumb:** Use MCP for repeated interactions within a session; opt for CLIs otherwise to avoid context bloat.

### Recommended MCP Servers for Developers

Categorized list of essential servers (install via `claude mcp add <name> -- <command>`):

#### Core Development

| Server | Purpose | Install Command |
|--------|---------|-----------------|
| **Context7** | Live docs for any library | `npx -y @upstash/context7-mcp@latest` |
| **GitHub** | PRs, issues, CI/CD | `npx -y @modelcontextprotocol/server-github` |
| **Filesystem** | Advanced file operations | `npx -y @modelcontextprotocol/server-filesystem` |
| **Sequential Thinking** | Structured problem-solving | `npx -y @modelcontextprotocol/server-sequential-thinking` |

#### Databases

| Server | Purpose | Install Command |
|--------|---------|-----------------|
| **MongoDB** | Atlas/Community, Performance Advisor | `npx -y mongodb-mcp-server` |
| **PostgreSQL** | Query Postgres naturally | `npx -y @modelcontextprotocol/server-postgres` |
| **DBHub** | Universal (MySQL, SQLite, etc.) | `npx -y @bytebase/dbhub` |

#### Documents & RAG

| Server | Purpose | Install Command |
|--------|---------|-----------------|
| **Docling** | PDF/DOCX parsing, 97.9% table accuracy | `uvx docling-mcp-server` |
| **Qdrant** | Vector search, semantic memory | `npx -y @qdrant/mcp-server` |
| **Chroma** | Embeddings, vector DB | `npx -y @chroma/mcp-server` |

#### Browser & Testing

| Server | Purpose | Install Command |
|--------|---------|-----------------|
| **Playwright** | E2E testing, scraping | `npx -y @anthropic-ai/playwright-mcp` |
| **Browser MCP** | Use your logged-in Chrome | (via browsermcp.io) |
| **Brave Search** | Privacy-first web search | `npx -y @anthropic-ai/brave-search-mcp` |

#### Cloud & Hosting

| Server | Purpose | Install Command |
|--------|---------|-----------------|
| **AWS** | Full AWS service access | `uvx awslabs.aws-api-mcp-server@latest` |
| **Cloudflare** | Workers, KV, R2 | `npx -y @cloudflare/mcp-server` |
| **Hostinger** | Domains, DNS, VMs, billing | `npm i -g hostinger-api-mcp` (then configure) |
| **Kubectl** | Kubernetes natural language | `npx -y @modelcontextprotocol/server-kubernetes` |

#### Workflow & Communication

| Server | Purpose | Install Command |
|--------|---------|-----------------|
| **Slack** | Messages, channel summaries | `npx -y @anthropic-ai/slack-mcp` |
| **Linear** | Issue tracking | `npx -y @linear/mcp-server` |
| **Figma** | Design specs, components | `npx -y @anthropic-ai/figma-mcp` |

Discovery resources: awesome-mcp-servers (76k+ stars), mcpservers.org, Claude Market.

### Context7 — Live Documentation Example

Context7 provides up-to-date library docs, solving training cutoff issues:

Installation: `claude mcp add context7 -- npx -y @upstash/context7-mcp@latest`

Example: "Using context7, show me the Next.js 15 cache API" → Fetches current docs for accurate responses.

### Installing MCP Servers

**.claude.json:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed"],
      "enabled": true
    }
  }
}
```

**Environment Variables (.env):**
```bash
GITHUB_TOKEN=ghp_xxxxx
DATABASE_URL=postgresql://user:pass@localhost/db
SLACK_TOKEN=xoxb-xxxxx
```

### Using MCP Tools

**Auto-Discovery:**
```bash
# Claude automatically discovers available MCP tools
claude -p "Create a GitHub PR for the auth refactor"
# Uses: mcp__github__create_pull_request

claude -p "Find all Slack messages about the outage"
# Uses: mcp__slack__search_messages
```

**Explicit Invocation:**
```bash
# List available MCP tools
/tools

# Use specific tool
/mcp__postgres__query "SELECT * FROM users WHERE active = true"
/mcp__google-drive__search "Q4 Sales Report"
```

**In Skills:**
```markdown
---
allowed-tools:
  - mcp__github__*
  - mcp__postgres__query
---

# Deployment Skill

When deploying:
1. Query database for migration status
2. Create GitHub release
3. Tag version
```

### Creating Custom MCP Servers

**Python Server:**
```python
from mcp import MCPServer, Tool

server = MCPServer("my-custom-server")

@server.tool("analyze_logs")
async def analyze_logs(filepath: str) -> dict:
    """Analyze log files for errors"""
    # Your implementation
    return {"errors": [], "warnings": []}

if __name__ == "__main__":
    server.run()
```

**TypeScript Server:**
```typescript
import { MCPServer } from "@modelcontextprotocol/sdk";

const server = new MCPServer({
  name: "my-custom-server",
  version: "1.0.0"
});

server.tool("fetch_metrics", async (params) => {
  // Your implementation
  return { metrics: {...} };
});

server.start();
```

**Register in .claude.json:**
```json
{
  "mcpServers": {
    "my-custom": {
      "command": "python",
      "args": ["./mcp-servers/my_server.py"]
    }
  }
}
```

### MCP and Context Optimization

**The Context Bloat Problem:**
- Early MCP implementations loaded all server tools at start
- Example: 5 MCP servers × 10 tools each = 50 tools in context
- Result: Wasted tokens, degraded performance

**Optimization Strategy:**
- **On-Demand Activation**: Tools load only when skill/command needs them
- **Skill Integration**: Skills wrap MCP tools for dynamic loading
- **Tool Filtering**: Only expose relevant tools per task

### MCP Best Practices

- **Security**: Validate environment variables, limit file access scopes
- **Error Handling**: Graceful failures with clear messages
- **Documentation**: Describe tools clearly for AI understanding
- **Rate Limiting**: Respect API limits of integrated services
- **Caching**: Cache expensive operations when possible
- **OAuth/OOTH**: Use secure authentication for third-party services

---

## Session Management & Worktrees

### Session Persistence

**Save & Resume:**
```bash
# Name a session for later
/save-session auth-refactor

# Resume named session
claude --resume auth-refactor

# List all sessions
/sessions

# Resume last session
claude --resume
```

**Session Data Stored:**
- Full conversation history
- Tool execution results
- File state snapshots
- CLAUDE.md context
- Sub-agent states

### Worktrees - Multi-Session Workspaces

**Worktrees** allow multiple concurrent Claude sessions in the same repo, each on different branches, without conflicts.

**Create Worktree:**
```bash
# Create worktree for feature branch
git worktree add ../myproject-feature feature/auth-v2

# Start Claude in worktree
cd ../myproject-feature
claude
```

**Use Cases:**
- **Parallel Development**: Feature A in main worktree, Bug fix in secondary
- **Experimentation**: Safe exploration without affecting main branch
- **Code Review**: Review PR in isolated worktree
- **Testing**: Test different approaches simultaneously

**Management:**
```bash
# List worktrees
git worktree list

# Remove worktree
git worktree remove ../myproject-feature

# Cleanup stale
git worktree prune
```

### Teleportation

**Claude Code Session Teleportation** lets you seamlessly move sessions between CLI and web interfaces.

**CLI → Web:**
```bash
# In terminal session
/teleport

# Opens browser to claude.ai/code with full session context
# Continue in web UI with same history, files, state
```

**Web → CLI:**
```bash
# In claude.ai/code, run:
/teleport

# Displays command to resume in terminal:
claude --resume session-abc123

# Run in terminal to continue
```

**Benefits:**
- Switch devices mid-task
- Use web UI for planning, CLI for execution
- Share sessions with team via web links
- Access session from mobile (web) or desktop (CLI)

---

## Cowork - No-Code AI Assistant

### Overview

**Cowork** is a desktop application (macOS, January 2026) that brings Claude Code's capabilities to non-coders. It autonomously manages files, edits documents, creates presentations, and controls browsers—all without coding knowledge.

### Key Features

**File Operations:**
- Create/edit Word docs, Excel sheets, PowerPoints
- PDF processing and extraction
- Batch file renaming and organization
- Document conversion

**Document Creation:**
- Write reports from templates
- Generate presentations with data
- Create formatted emails and letters
- Build forms and surveys

**Browser Control:**
- Fill out web forms
- Extract data from websites
- Automate repetitive web tasks
- Research compilation

**Data Analysis:**
- Excel data manipulation
- Chart/graph generation
- Report summarization
- Trend analysis

### Installation

**Requirements:**
- macOS 12.0+
- Claude Max subscription
- 2GB disk space

**Download:**
```bash
# From claude.ai
https://claude.ai/download/cowork

# Or via Homebrew (unofficial)
brew install --cask claude-cowork
```

### Usage Examples

**Create Presentation:**
```
You: "Create a sales presentation with our Q4 data from revenue.xlsx"

Cowork:
✓ Reading revenue.xlsx
✓ Analyzing data trends
✓ Creating PowerPoint slides
✓ Adding charts and visualizations
✓ Applying company template
→ Saved as "Q4_Sales_Presentation.pptx"
```

**Organize Files:**
```
You: "Organize my Downloads folder by file type"

Cowork:
✓ Scanning Downloads/
✓ Creating folders: Documents, Images, Videos, Archives
✓ Moving 347 files
✓ Renaming duplicates
→ Downloads organized
```

**Research Task:**
```
You: "Research top 5 CRM tools and create comparison spreadsheet"

Cowork:
✓ Searching web for CRM tools
✓ Extracting features and pricing
✓ Creating Excel comparison
✓ Adding recommendation column
→ Saved as "CRM_Comparison.xlsx"
```

### Sandbox Security

Cowork operates in a **sandboxed environment**:
- Limited file system access (user-specified folders)
- No access to system files or other applications
- Browser actions require confirmation for sensitive operations
- All actions logged for audit trail

### Differences from Claude Code

| Feature | Claude Code | Cowork |
|---------|-------------|--------|
| **Target Users** | Developers | Non-coders |
| **Primary Interface** | Terminal | Desktop GUI |
| **Code Generation** | Yes (programming) | No (document automation) |
| **Document Editing** | Basic | Advanced (Office suite) |
| **Browser Control** | Via Puppeteer/MCP | Built-in UI automation |
| **File Operations** | Developer-focused | User-friendly |
| **Pricing** | Pro/Team/API | Max subscription |

---

## APIs & Integrations

### Messages API

**Core Chat Endpoint:**
```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    system="You are a senior software architect.",
    messages=[
        {"role": "user", "content": "Design a microservices architecture"}
    ]
)

print(message.content[0].text)
```

**Streaming:**
```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain async/await"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Tool Use:**
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in SF?"}]
)

# Handle tool calls
for content in response.content:
    if content.type == "tool_use":
        # Execute tool, return result
        ...
```

### Vision API

**Image Analysis:**
```python
import base64

with open("chart.png", "rb") as img:
    image_data = base64.b64encode(img.read()).decode()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {"type": "text", "text": "Analyze this chart"}
            ]
        }
    ]
)
```

### PDF & Document APIs

**PDF Processing:**
```python
# Send PDF for analysis
with open("report.pdf", "rb") as pdf:
    pdf_data = base64.b64encode(pdf.read()).decode()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {"type": "text", "text": "Summarize key findings"}
            ]
        }
    ]
)
```

### Prompt Caching

**Reduce costs for repeated context:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert coder...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[...]
)

# Subsequent requests with same system prompt = 90% cheaper
```

### Batches API

**Process requests asynchronously:**
```python
# Create batch
batch = client.batches.create(
    requests=[
        {
            "custom_id": "req-1",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Task 1"}]
            }
        },
        # ... up to 10,000 requests
    ]
)

# Check status
status = client.batches.retrieve(batch.id)

# Get results when complete
results = client.batches.results(batch.id)
```

### Enterprise Integrations

**AWS Bedrock:**
```python
import boto3

bedrock = boto3.client('bedrock-runtime')

response = bedrock.invoke_model(
    modelId='anthropic.claude-4-5-sonnet-20250929-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Hello"}]
    })
)
```

**Google Vertex AI:**
```python
from anthropic import AnthropicVertex

client = AnthropicVertex(
    project_id="your-project",
    region="us-central1"
)

response = client.messages.create(
    model="claude-sonnet-4-5@20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

**OpenAI Compatibility:**
```python
# Use OpenAI SDK with Claude
from openai import OpenAI

client = OpenAI(
    base_url="https://api.anthropic.com/v1",
    api_key="your-anthropic-key"
)

# Standard OpenAI calls route to Claude
```

---

## Best Practices

### Understanding Static vs Dynamic Context

**The Core Principle:**
Modern agent efficiency depends on balancing static (always-included) and dynamic (on-demand) context.

**Static Context Strategy (CLAUDE.md, Rules):**
- **Keep Minimal**: Include only essential, frequently-needed guidance
- **High Quality**: Every line should prevent actual errors you've seen
- **Evolve Iteratively**: When agent makes mistakes, add fixes to rules
- **Example Evolution**:
  - Agent forgets to tag issues in PRs → Add rule: "Always tag related issues"
  - Agent uses wrong test framework → Add rule: "Use pytest, not unittest"
- **Target**: Aim for <50% of context window used by static content

**Dynamic Context Strategy (Skills, MCP):**
- **Use for Extensions**: Non-essential capabilities that aren't always needed
- **Load On-Demand**: Let agent discover and activate when relevant
- **Bundle Smart**: Combine related tools in single skill to minimize overhead
- **OAuth/OOTH**: Secure third-party integrations through MCP

### For Developers

**1. Project Setup:**
```bash
# Initialize Claude-ready project
git init my-project
cd my-project

# Create project memory (Static Context)
cat > CLAUDE.md << EOF
# My Project

This is a [tech stack] application that [purpose].

## Code Style
- [conventions]

## Test Requirements
- [coverage goals]

## Known Fixes
- Always run migrations before deploying
- Use environment-specific config files
EOF

# Add useful commands
mkdir -p .claude/commands
cat > .claude/commands/test.md << EOF
---
description: Run tests with coverage
---
Run pytest with coverage report. Fail if below 80%.
EOF

# Configure tools
cat > settings.json << EOF
{
  "allowedTools": ["Read", "Edit", "Write", "Bash", "WebSearch"],
  "respectGitignore": true
}
EOF
```

**2. Development Workflow:**
```bash
# Start session with context
claude --model sonnet

# Use Ralph for mechanical tasks
/ralph-loop "Add logging to all API endpoints" --max-iterations 25

# Review changes before commit
git diff
git add -p
git commit -m "Added logging (Claude Code)"

# Use worktrees for experiments
git worktree add ../experiment-branch experiment
cd ../experiment-branch
claude -p "Try alternative approach to caching"
```

**3. Cost Optimization:**
- Use **Haiku** for drafts and simple tasks
- Enable **prompt caching** for large system contexts
- Batch similar requests with **Batches API**
- Set reasonable `max_tokens` limits
- Use `permission-mode: plan` to review before expensive operations

**4. Quality Assurance:**
```json
// Enforce standards with hooks (Deterministic Actions)
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit.*\\.(py|js|ts)$",
        "hooks": [
          {"type": "command", "command": "pre-commit run --files $FILE"}
        ]
      }
    ]
  }
}
```

### For Architects

**1. Multi-Agent Design:**
```
Lead Agent (Opus)
├── Backend Agent (Sonnet) → API, Database
├── Frontend Agent (Sonnet) → UI, Components
├── Testing Agent (Haiku) → Unit/Integration tests
└── DevOps Agent (Sonnet) → CI/CD, Infrastructure
```

**2. Skill Libraries:**
```
.claude/skills/
├── api-design/         # RESTful API patterns
├── database-migration/ # Safe schema changes
├── security-audit/     # Vulnerability scanning
├── performance-test/   # Load testing
└── architecture-doc/   # Diagrams, ADRs
```

**3. Team Standards:**
```markdown
# CLAUDE.md (shared via git - Static Context)

## Architecture Principles
- Microservices with clear boundaries
- Event-driven communication via Kafka
- DDD for domain modeling

## Technology Stack
- Backend: Python 3.11, FastAPI, SQLAlchemy
- Frontend: React 18, TypeScript, Tailwind
- Infra: Docker, Kubernetes, Terraform

## Rules Evolution
When Claude makes errors:
1. Document the error in this file
2. Add specific correction rule
3. Share update with team via PR

## Review Checklist
Before merging Claude Code changes:
- [ ] Tests pass (>80% coverage)
- [ ] No security vulnerabilities
- [ ] API docs updated
- [ ] Performance benchmarks run
```

### For Vibe Coders

**Vibe Coding** = Rapid prototyping with AI, focusing on velocity over perfection.

**1. Quick Starts:**
```bash
# Instant prototypes
claude -p "Build a todo app with React and local storage"
claude -p "Create API server with user auth in FastAPI"
claude -p "Make a data viz dashboard with D3.js"
```

**2. Iteration Speed:**
```bash
# Use acceptEdits mode for flow state
claude --permission-mode acceptEdits

# Ralph loop for "keep improving"
/ralph-loop "Make this landing page look amazing" --max-iterations 15
```

**3. Learning by Doing:**
```bash
# Explore unfamiliar tech
claude -p "Explain and show example of React Server Components"
claude -p "What's the difference between var/let/const? Show code"

# Build while learning
claude -p "Build a GraphQL server and explain each part as you go"
```

**4. Polish on Demand:**
```bash
# Start rough, refine later
claude -p "Quick and dirty solution to [problem]"
# ... later ...
claude -p "Refactor previous code for production quality"
```

### Context Management Best Practices

**1. Static Context (Rules/CLAUDE.md):**
- Start small: 10-20 lines maximum
- Add only after seeing repeated errors
- Examples:
  - "Always use TypeScript strict mode"
  - "Run database migrations in transactions"
  - "Tag Jira issues in commit messages"
- Monitor context usage: `claude --show-context-size`

**2. Dynamic Context (Skills/MCP):**
- Default to official skills when available
- Create custom skills for team-specific workflows
- Use `context: fork` for parallel/experimental tasks
- Optimize tool loading: one skill with 10 tools > 10 separate skills

**3. Modes and Sub-Agents:**
- Default to out-of-box agents (explore, plan)
- Customize only for complex, repeated workflows
- Document mode purposes clearly
- Use UI reminders to guide agent behavior

### Security Best Practices

**1. API Key Management:**
```bash
# NEVER commit API keys
echo "ANTHROPIC_API_KEY=sk-..." >> .env
echo ".env" >> .gitignore

# Use environment variables
export ANTHROPIC_API_KEY=$(cat ~/.anthropic_key)
```

**2. Sandbox Usage:**
```bash
# Always use sandboxed environments for untrusted code
claude --sandbox

# Limit tool access
{
  "allowedTools": ["Read", "Edit"],  // No Bash!
  "respectGitignore": true
}
```

**3. Code Review:**
```bash
# Review all Bash commands
claude --permission-mode normal  # Approve each command

# Use hooks for security scanning (Deterministic Actions)
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "security-scan.sh"}]
      }
    ]
  }
}
```

**4. Data Privacy:**
- Don't send PII to API without consent
- Use local models (via Bedrock/Vertex) for sensitive data
- Scrub logs of API keys and secrets
- Enable organization SSO for team accounts

### Performance Optimization

**1. Context Management:**
```python
# Use message history efficiently
messages = [
    {"role": "user", "content": "Task 1"},
    {"role": "assistant", "content": "Result 1"},
    # Only keep last N messages
][-10:]  # Last 10 messages only
```

**2. Streaming for Responsiveness:**
```python
# Don't wait for full response
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        display_to_user(text)  # Instant feedback
```

**3. Parallel Execution:**
```python
import asyncio

async def process_batch(items):
    tasks = [query_claude(item) for item in items]
    return await asyncio.gather(*tasks)

# Process 10 items concurrently
results = await process_batch(items)
```

**4. Caching Strategy:**
```python
# Cache expensive system prompts
system_prompt = {
    "type": "text",
    "text": large_codebase_context,
    "cache_control": {"type": "ephemeral"}
}

# Reuse across requests (90% cost reduction)
```

### Iterative Rules Evolution (Key Practice)

**The Cycle:**
1. **Observe**: Agent makes a mistake (e.g., forgets test coverage)
2. **Document**: Add to CLAUDE.md: "Always include >80% test coverage"
3. **Validate**: Next task uses new rule, error prevented
4. **Refine**: After 5-10 tasks, review rules for effectiveness
5. **Prune**: Remove rules that aren't preventing errors

**Example Evolution:**
```markdown
# CLAUDE.md - Version 1 (Week 1)
## Code Style
- Use Black formatting

# CLAUDE.md - Version 2 (Week 2 - after PR issues)
## Code Style
- Use Black formatting
- Always tag related Jira issues in commits

# CLAUDE.md - Version 3 (Week 4 - after production bug)
## Code Style
- Use Black formatting
- Always tag related Jira issues in commits
- Run integration tests before marking PR ready
```

---

## Quick Reference

### Essential Commands

```bash
# Claude Code basics
claude                          # Start interactive session
claude -p "prompt"              # One-shot command
claude --model opus             # Use specific model
claude --resume session-name    # Resume saved session

# Session management
/save-session name              # Save current session
/sessions                       # List all sessions
/teleport                       # Move to web/CLI

# Tools & plugins
/tools                          # List available tools
/plugin install name            # Install plugin
/skills                         # List loaded skills
/hooks                          # Configure hooks

# Slash commands
/optimize file.js               # Run custom command
/ralph-loop "task"              # Autonomous iteration
/task researcher "topic"        # Invoke sub-agent

# Settings
/permission-mode acceptEdits    # Auto-approve edits
/thinking                       # Show reasoning
/help                           # Full command list
```

### File Structure Reference

```
project-root/
├── .claude/
│   ├── commands/           # Project slash commands
│   │   ├── deploy.md
│   │   └── test.md
│   ├── skills/             # Project-specific skills
│   │   └── my-skill/
│   │       └── skill.md
│   ├── agents/             # Custom sub-agents
│   │   └── researcher.json
│   └── hooks/              # Lifecycle hooks
│       └── pre-commit.sh
├── .claude.json            # MCP servers, global config
├── CLAUDE.md               # Project context & memory (Static Context)
├── settings.json           # Tool permissions, hooks
└── .env                    # Environment variables (gitignored!)
```

### Context Type Decision Tree

```
Need to include something?
│
├── Used in EVERY conversation? 
│   └── Yes → Static Context (CLAUDE.md)
│       Examples: code style, project overview, common fixes
│
└── No → Dynamic Context
    │
    ├── Workflow/shortcut?
    │   └── Slash Command (.claude/commands/)
    │
    ├── Tool/integration?
    │   └── MCP Server (.claude.json)
    │
    ├── Complex capability?
    │   └── Skill (.claude/skills/)
    │
    └── Specialized task?
        └── Sub-Agent (.claude/agents/)
```

### Model Selection Cheatsheet

| Task Type | Recommended Model | Reasoning |
|-----------|------------------|-----------|
| Quick drafts | Haiku 4.5 | Fast, cheap |
| General coding | Sonnet 4.5 | Best balance |
| Complex architecture | Opus 4.5 | Highest intelligence |
| Bulk operations | Haiku 4.5 | Cost-effective |
| Production code review | Opus 4.5 | Catches subtle issues |
| API endpoint generation | Sonnet 4.5 | Proven reliability |
| Data analysis | Sonnet 4.5 | Strong reasoning |
| Creative writing | Opus 4.5 | Nuanced language |

### Pricing Calculator

```
Example: 50-iteration Ralph loop on 10K-line codebase

Input tokens per iteration: ~15,000
Output tokens per iteration: ~3,000
Total iterations: 50

With Sonnet 4.5:
Input: 750,000 tokens × $3/M = $2.25
Output: 150,000 tokens × $15/M = $2.25
Total: ~$4.50

With Opus 4.5:
Input: 750,000 tokens × $15/M = $11.25
Output: 150,000 tokens × $75/M = $11.25
Total: ~$22.50
```

---

## Resources

### Official Documentation
- **Docs**: https://docs.anthropic.com
- **API Reference**: https://docs.anthropic.com/api
- **Academy**: https://anthropic.com/learn
- **Console**: https://console.anthropic.com
- **Status**: https://status.anthropic.com

### GitHub Repositories
- **Skills**: https://github.com/anthropics/anthropic-sdk-python/tree/main/skills
- **Agent SDK**: https://github.com/anthropics/claude-code-sdk
- **MCP Servers**: https://github.com/modelcontextprotocol/servers
- **Examples**: https://github.com/anthropics/anthropic-cookbook

### Community
- **Discord**: https://discord.gg/anthropic
- **Reddit**: r/ClaudeAI
- **X/Twitter**: @AnthropicAI
- **YouTube**: Anthropic (tutorials)

### Additional Resources
- **Claude Code Mastery Guide**: https://thedecipherist.github.io/claude-code-mastery/
- **Awesome MCP Servers**: 76k+ stars on GitHub
- **MCP Servers Directory**: mcpservers.org
- **Claude Market**: Plugin and skill marketplace

### Tools & Extensions
- **VS Code Extension**: Claude Code integration
- **Chrome Extension**: Claude in browser
- **Desktop Apps**: macOS, Windows, Linux
- **Mobile**: iOS, Android apps


### Others:

- [Exploration of Anthropic Claude](https://responseawareness.substack.com/p/exploration-of-anthropics-claude)

- [The Complete Claude Code Guide for Your New Year Resolution: Code Smarter in 2026](https://ai.gopubby.com/the-complete-claude-code-guide-for-your-new-year-resolution-code-smarter-in-2026-be1782be2083)

- [Claude Code 2.1 Guide](https://www.datacamp.com/tutorial/claude-code-2-1-guide)

---

## What's Next?

### Roadmap (2026)

**Q1 2026:**
- ✅ Cowork research preview (January)
- Extended context (500K+ tokens)
- Multi-modal outputs (image generation)
- Advanced computer use

**Q2-Q4 2026 (Expected):**
- Windows/Linux Cowork support
- Real-time collaboration features
- Voice interface for Claude Code
- Enterprise agent orchestration platform
- More pre-built skills and MCP servers
- Improved cost efficiency across models

### Getting Started Path

**Week 1: Basics**
1. Install Claude Code
2. Run first interactive session
3. Create CLAUDE.md for a project (start with 5-10 lines)
4. Try 3-5 slash commands

**Week 2: Skills & Tools**
1. Install 2-3 official skills
2. Set up MCP server (GitHub or Slack)
3. Create custom slash command
4. Experiment with hooks

**Week 3: Advanced**
1. Build custom skill
2. Try Ralph loop on real task (start with 10 iterations)
3. Set up worktrees workflow
4. Configure sub-agents

**Week 4: Production**
1. Integrate into team workflow
2. Set up CI/CD hooks
3. Document team standards in CLAUDE.md
4. Train teammates on static vs dynamic context

---

## Conclusion

The Claude ecosystem in 2026 represents the culmination of years of AI agent evolution, from early hallucination-fighting rules to sophisticated dynamic context management. Understanding this history—and the core distinction between static and dynamic context—is essential for effective use.

**Key Evolutionary Insights:**
- **Static → Dynamic**: The industry moved from "include everything" to "include only what's needed"
- **Tool Calling Maturity**: Reliable tool use enabled Skills, MCP, and sub-agents
- **Open Standards**: Skills and MCP promote ecosystem growth beyond Anthropic

**Essential Framework:**
- **Static Context (CLAUDE.md)**: Minimal, high-quality, evolved iteratively
- **Dynamic Context (Skills/MCP)**: On-demand loading, avoid token bloat
- **Deterministic Actions (Hooks)**: Guaranteed execution for critical workflows
- **Autonomous Iteration (Ralph)**: Prevent premature exits, achieve completion

**Practical Approach:**
1. Start with minimal static context (10-20 lines in CLAUDE.md)
2. Add rules only after observing errors
3. Use skills for non-essential capabilities
4. Monitor context usage (<50% static target)
5. Leverage hooks for formatting, security, testing
6. Scale to Ralph loops for mechanical tasks

**Model Strategy:**
- Haiku → quick drafts, simple tasks
- Sonnet → default for development, orchestration
- Opus → complex reasoning, production code

Whether you're a developer shipping production code, an architect designing systems, or a vibe coder rapidly prototyping, the key is understanding the conceptual framework: balance static (always-on) and dynamic (on-demand) context, use deterministic hooks for guarantees, and evolve your rules based on observed agent behavior.

**Remember**: The ecosystem evolves rapidly. Check https://docs.anthropic.com for the latest, join the community for insights, and experiment often—but always with iteration limits and git safety nets.

The future of development isn't just AI-assisted; it's AI-collaborative, with humans and agents each playing to their strengths within a well-designed context management framework.

---

**Related:**- [claude-agents-vs-sub-agents-vs-projects-vs-workflow-vs-rules-vs-mcp-vs-skills](../../../Agents/skills/claude-agents-vs-sub-agents-vs-projects-vs-workflow-vs-rules-vs-mcp-vs-skills.md) — Complements this ecosystem reference with conceptual depth on each primitive (Agents, Sub-agents, Skills, MCP, Projects, Rules).- [AI-Coding-Loops](../../../Agents/development/AI-Coding-Loops.md) — Provides the autonomy-spectrum framework that contextualizes every agent primitive in the ecosystem (Ralph Loop, Code Review, Sub-agents) against appropriate use cases.- [MCP_Scalability_Issue_Solution](../../../Protocols/MCP_Scalability_Issue_Solution.md) — Deep dive on MCP scalability — the single biggest operational issue for the Claude ecosystem once you connect multiple servers.- [ai-token-optimization-tools](../../optimization/ai-token-optimization-tools.md) — Context bloat is the central problem Skills were designed to solve; this catalogue lists active tools (Lean-CTX, MCP-Compressor, RTK) addressing it.- [AI-Assisted-Development](../../../Agents/development/AI-Assisted-Development.md) — Broader framework on AI-assisted development that contextualizes Claude primitives within the SDD + UACF + Skills three-layer architecture.
