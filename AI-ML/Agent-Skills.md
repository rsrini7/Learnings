***

# Agent Skills — A Standard for Packaging Agent Workflows

## Overview

**Agent Skills** is a new standard introduced by Anthropic for encapsulating instructions, scripts, resources, and assets into a single, discoverable, and portable format. It provides a way to integrate domain-specific or workflow-specific knowledge directly into capable agents without the need for repetitive prompting. This approach reduces token usage, enhances reusability, and enables sharing across teams and compatible agent environments.

Agent Skills extend the idea of *code understanding* by bundling everything related to a given capability into an actionable, context-rich unit.

***

## Definition

Agent Skills compartmentalize complex or domain-specific workflows, tools, and resources into an organized, discoverable package.
Each skill outlines all the information required for a specific task — for example, **handling PDFs** or **generating reports** — along with any supporting scripts, documentation, templates, and dependencies.

This structure allows an agent to load, interpret, and execute complex operations with minimal additional prompting.

***

## Compatible Agents and Environments

Agent Skills are designed for use with **file system-based agents**, such as:

- **Claude Code**
- **Cursor Agent**
- **OpenAI CodeX**
- **Deep Agents** (LangChain)
- **Open Code** (open-source)

These agents operate in environments resembling a terminal interface. They can run bash commands, execute Python scripts, and interact with a file system — enabling them to read, write, and modify files or data directly within structured directories.

***

## Benefits of File System-Based Agents

File system-based agents gain several advantages from this approach:

- **Expanded Task Capability:** Access to general tools and open environments allows agents to handle a wider range of operations beyond strictly defined function calls.
- **Dynamic Context Loading:** The file system acts as a pseudo-memory layer, letting agents selectively load relevant information without overloading their context window.
- **Workflow Reusability:** Once authored, skills can be shared and reused across different agents and projects with minimal adaptation.

***

## Relationship to agents.md Standard

Agent Skills build upon concepts introduced by the **agents.md** standard — a markdown specification that outlines context and preferences for a coding agent within a repository. While *agents.md* serves as a README file intended for agents, *Agent Skills* take this further by bundling executable context, workflows, and assets directly.

***

## Comparison: Agent Skills, Function Calling, and Model Context Protocol (MCP)

| Aspect | Function Calling | Model Context Protocol (MCP) | Agent Skills |
| :-- | :-- | :-- | :-- |
| **Purpose** | Enables models to call APIs or tools via a schema. | Standardizes tool execution and formatting via servers. | Packages workflows, context, and files into actionable units. |
| **Scope** | Defines schema and arguments for a single call. | Manages interoperability across tool ecosystems. | Integrates all components for a complete domain or task. |
| **Complementary Role** | Works well for specific API interactions. | Ensures consistent tool handling. | Provides reusable, domain-aware workflows leveraging both other standards. |

Agent Skills complement, rather than replace, existing protocols — packaging function calls and MCP tools into workflow-specific contexts.

***

## Creating an Agent Skill

An Agent Skill is typically a **lightly formatted markdown file** accompanied by a **directory structure** containing associated files. The primary components are:

- **Front Matter:** Metadata such as name, description, and category.
- **Body:** The main content describing purpose, usage scenarios, scripts, and examples.

Here’s a **clear, practical sample Agent Skill folder structure**, following the conventions discussed and suitable for **file system–based agents**.

---

## **Sample Agent Skill Folder Structure**

```text
agent-skills/
└── processing-pdfs/
    ├── skill.md
    ├── README.md
    ├── scripts/
    │   ├── extract_text.py
    │   ├── split_pages.py
    │   ├── summarize_pdf.py
    │   └── convert_to_markdown.py
    ├── templates/
    │   ├── report_template.md
    │   └── summary_template.md
    ├── assets/
    │   ├── example_input.pdf
    │   └── example_output.md
    ├── references/
    │   ├── pdf_spec_notes.md
    │   └── edge_cases.md
    └── tests/
        ├── test_extract_text.py
        └── test_split_pages.py
```

---

## **What Each Part Does**

### **`processing-pdfs/`**

* The **skill name** (use gerund form).
* One folder = one well-defined workflow capability.

---

### **`skill.md` (Core Skill File)**

* The **entry point** agents read first.
* Contains:

  * Front matter (name, description, requirements)
  * What the skill does
  * When to use it
  * How to invoke scripts
  * Expected inputs/outputs

Example sections:

```md
---
name: processing PDFs
description: Extracting, transforming, and summarizing PDF documents
tools: python, bash
---

## When to Use
- When working with scanned or text PDFs
- When summaries or markdown output are required

## How It Works
- Uses scripts in `/scripts`
- Outputs markdown or text files
```

---

### **`README.md` (Optional)**

* Human-focused documentation.
* Useful for onboarding teammates.
* Not required for agents, but helpful.

---

### **`scripts/`**

* **Executable logic** agents actually run.
* Each script should:

  * Do one thing well
  * Be callable from CLI
  * Have clear inputs/outputs

Examples:

* `extract_text.py` → PDF → text
* `summarize_pdf.py` → text → summary

---

### **`templates/`**

* Reusable output formats.
* Keeps generation consistent.
* Examples:

  * Report structure
  * Executive summary format

---

### **`assets/`**

* Sample inputs and outputs.
* Helps agents:

  * Understand expected formats
  * Validate behavior
* Also useful for demos and testing.

---

### **`references/`**

* Supporting knowledge:

  * Edge cases
  * Specs
  * Gotchas
* Loaded only when needed → saves context window.

---

### **`tests/` (Optional but Recommended)**

* Automated validation.
* Enables:

  * Confidence in execution
  * Regression prevention
* Especially useful in shared/team skills.

---

## **Key Design Principles**

* One skill = one responsibility
* Scripts are small and composable
* Documentation lives **with execution**
* File system = memory + tooling + context

***

## Best Practices for Authoring Skills

To ensure consistency, maintainability, and usability:

- Keep the **content concise** and front-load crucial information.
- Use **gerund form** for naming (e.g., *“processing PDFs”*).
- Write in the **third person** for objective clarity.
- Maintain **consistent terminology** within and across skills.
- Keep each skill file **under 500 lines** to promote readability.
- Include examples, usage instructions, and references when applicable.

***

## Example: *Apple Notes* Skill

An example skill, **Apple Notes**, demonstrates how an agent can interact with the Apple Notes application to perform common operations (Create, Read, Update, Delete).

The skill includes:

- **Overview and scenarios** (“when to use” guidance).
- **Four scripts** for performing note management actions (`create`, `delete`, `list`, `read`).
- A markdown definition describing metadata and structure.

When used in an environment such as Claude Code, the agent can apply this skill directly to manage notes within Apple Notes via natural commands.

***

## Key Benefits and Applications

Agent Skills represent a meaningful step toward **structured, reusable, and intelligent agent design**.
They promote:

- **Personalized agent behavior** with minimal context switching.
- **Rigorous workflow documentation** aligned with best software engineering practices.
- **Seamless collaboration** — allowing domain-specific logic to be easily shared or versioned like code.
- **Enhanced autonomy** — enabling agents to execute complex tasks without constant re-prompting or fine-tuning.

Agent Skills encourage both human creators and AI tools to think modularly, fostering a future where task knowledge, processes, and automations are **packaged, portable, and executable** across intelligent systems.

***
