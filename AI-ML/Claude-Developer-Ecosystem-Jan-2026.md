# Complete Claude Developer Ecosystem Guide (2026)

**The Ultimate Reference for Developers, Architects, and Vibe Coders**

This comprehensive guide covers Anthropic's entire Claude ecosystem—from models and APIs to agentic workflows, developer tools, and enterprise integrations. Updated January 2026.

---

## Table of Contents

1. [Core Models & Pricing](#core-models--pricing)
2. [Claude Code - The Flagship Developer Tool](#claude-code---the-flagship-developer-tool)
3. [Agent SDK - Build Custom Agents](#agent-sdk---build-custom-agents)
4. [Projects & Workspaces](#projects--workspaces)
5. [Skills - Modular Capabilities](#skills---modular-capabilities)
6. [Sub-Agents - Parallel Task Execution](#sub-agents---parallel-task-execution)
7. [Plugins - Shareable Extensions](#plugins---shareable-extensions)
8. [Slash Commands - Custom Shortcuts](#slash-commands---custom-shortcuts)
9. [Hooks - Lifecycle Automation](#hooks---lifecycle-automation)
10. [Ralph Loop - Autonomous Iteration](#ralph-loop---autonomous-iteration)
11. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
12. [Session Management & Worktrees](#session-management--worktrees)
13. [Cowork - No-Code AI Assistant](#cowork---no-code-ai-assistant)
14. [APIs & Integrations](#apis--integrations)
15. [Best Practices](#best-practices)

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

## Claude Code - The Flagship Developer Tool

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

### Configuration Files

**CLAUDE.md** - Project memory/instructions
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

**settings.json** - Tool permissions & preferences
```json
{
  "allowedTools": ["Read", "Edit", "Write", "Bash", "WebSearch"],
  "enableThinking": true,
  "respectGitignore": true,
  "autoSave": true,
  "maxTokens": 8000
}
```

**.claude.json** - MCP servers & advanced config
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

**Skills** are reusable packages (folder with instructions + resources) that give Claude specialized capabilities. They're dynamically loaded when needed and portable across Claude Code, API, and claude.ai.

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
- **api-testing** - Postman-like testing
- **sql-query** - Database operations

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
- **Context**: Use `context: fork` for isolation
- **Dependencies**: Document in frontmatter
- **Examples**: Include 2-3 usage examples
- **Versioning**: Maintain backward compatibility

---

## Sub-Agents - Parallel Task Execution

### Overview

**Sub-agents** are specialized AI assistants that handle specific tasks in parallel or with isolated context. They enable multi-agent architectures where a lead agent delegates to workers.

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
  "maxTurns": 20
}
```

**Usage:**
```bash
# Invoke custom agent
/task researcher "Research quantum computing trends"

# Parallel execution
/task researcher "Study GraphQL vs REST" &
/task researcher "Analyze microservices patterns" &
wait
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
```

**3. Research Synthesis:**
```markdown
---
# agents/synthesis.json
{
  "name": "synthesis",
  "systemPrompt": "Combine research from multiple sources into coherent report",
  "allowedTools": ["Read", "Write"]
}
---
```

### Sub-Agent Context Management

**Isolated Context:**
```markdown
---
context: fork  # in skill frontmatter
---
```
- No main agent pollution
- Safe for experimental logic
- Parallel execution without conflicts

**Shared Context:**
```markdown
---
context: shared
---
```
- Access to main conversation
- Builds on prior work
- Sequential dependencies

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

**Slash commands** are custom shortcuts for frequently-used prompts, stored as Markdown files that Claude Code executes.

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

**Hooks** are event-driven automations that run at specific points in Claude Code's workflow. They enable custom logic for validation, formatting, notifications, and more.

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

### Hook Matchers

**Tool Matchers:**
- `Edit` - Any file edit
- `Bash` - Any bash command
- `Edit.*\\.js$` - JavaScript files
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

---

## Ralph Loop - Autonomous Iteration

### Overview

**Ralph Wiggum** (named after the Simpsons character) is a development methodology based on continuous AI agent loops. It allows Claude to iteratively improve work until truly complete, preventing premature exits.

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

**MCP** is an open protocol (think "USB-C for AI") that standardizes how AI applications connect to external tools and data sources. It enables Claude to access databases, APIs, filesystems, and enterprise tools through a uniform interface.

### Architecture

```
┌─────────────────┐
│  Host (Claude)  │
│                 │
│  ┌───────────┐  │
│  │MCP Client│  │
│  └─────┬─────┘  │
└────────┼────────┘
         │
         │ MCP Protocol
         │
    ┌────┴────┬────────┬─────────┐
    │         │        │         │
┌───┴──┐  ┌──┴───┐ ┌──┴───┐ ┌───┴────┐
│GitHub│  │Slack │ │Drive │ │Postgres│
└──────┘  └──────┘ └──────┘ └────────┘
  MCP       MCP      MCP       MCP
 Server    Server   Server    Server
```

### Official MCP Servers (100M+ monthly downloads)

**Development:**
- **github** - Repository operations, PR management, issues
- **gitlab** - GitLab integration
- **postgres** - Database queries and schema operations
- **sqlite** - Local database access
- **filesystem** - Read/write local files

**Productivity:**
- **google-drive** - Drive file operations
- **google-calendar** - Calendar management
- **slack** - Channel messages, user lookup
- **notion** - Workspace queries

**Utilities:**
- **fetch** - HTTP requests to APIs
- **puppeteer** - Browser automation
- **sentry** - Error tracking integration
- **memory** - Persistent key-value storage

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

### MCP Best Practices

- **Security**: Validate environment variables, limit file access scopes
- **Error Handling**: Graceful failures with clear messages
- **Documentation**: Describe tools clearly for AI understanding
- **Rate Limiting**: Respect API limits of integrated services
- **Caching**: Cache expensive operations when possible

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

### For Developers

**1. Project Setup:**
```bash
# Initialize Claude-ready project
git init my-project
cd my-project

# Create project memory
cat > CLAUDE.md << EOF
# My Project

This is a [tech stack] application that [purpose].

## Code Style
- [conventions]

## Test Requirements
- [coverage goals]
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
// Enforce standards with hooks
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
# CLAUDE.md (shared via git)

## Architecture Principles
- Microservices with clear boundaries
- Event-driven communication via Kafka
- DDD for domain modeling

## Technology Stack
- Backend: Python 3.11, FastAPI, SQLAlchemy
- Frontend: React 18, TypeScript, Tailwind
- Infra: Docker, Kubernetes, Terraform

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

# Use hooks for security scanning
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
├── CLAUDE.md               # Project context & memory
├── settings.json           # Tool permissions, hooks
└── .env                    # Environment variables (gitignored!)
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

### Tools & Extensions
- **VS Code Extension**: Claude Code integration
- **Chrome Extension**: Claude in browser
- **Desktop Apps**: macOS, Windows, Linux
- **Mobile**: iOS, Android apps

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
3. Create CLAUDE.md for a project
4. Try 3-5 slash commands

**Week 2: Skills & Tools**
1. Install 2-3 official skills
2. Set up MCP server (GitHub or Slack)
3. Create custom slash command
4. Experiment with hooks

**Week 3: Advanced**
1. Build custom skill
2. Try Ralph loop on real task
3. Set up worktrees workflow
4. Configure sub-agents

**Week 4: Production**
1. Integrate into team workflow
2. Set up CI/CD hooks
3. Document team standards in CLAUDE.md
4. Train teammates

---

## Conclusion

The Claude ecosystem in 2026 is a comprehensive platform for agentic AI development. From the foundational models (Haiku, Sonnet, Opus) to developer tools (Claude Code, Agent SDK), extensibility systems (Skills, Plugins, MCP), and automation patterns (Sub-Agents, Ralph Loop, Hooks), it provides everything needed to build sophisticated AI-powered workflows.

**Key Takeaways:**
- **Models**: Use the right model for the task (Haiku → Sonnet → Opus)
- **Claude Code**: Your primary interface for agentic coding
- **Skills**: Modular capabilities, portable across tools
- **MCP**: Universal protocol for tool integration
- **Ralph Loop**: Autonomous iteration for completion
- **Sub-Agents**: Parallel task execution
- **Hooks**: Lifecycle automation
- **Projects**: Context management at scale

Whether you're a developer shipping production code, an architect designing systems, or a vibe coder rapidly prototyping, Claude's ecosystem has the tools you need. Start simple, experiment often, and leverage the community's growing library of skills, plugins, and integrations.

**Remember**: The ecosystem evolves rapidly. Check https://docs.anthropic.com for the latest updates, join the community for tips, and don't hesitate to experiment—that's where the magic happens.
