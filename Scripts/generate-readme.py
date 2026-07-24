#!/usr/bin/env python3
"""Generate README.md with all file links.

Design goals:
- AUTO-DISCOVER subfolders so newly created folders are never missed.
- Curated titles/emojis are used when known; unknown folders get an
  auto-generated title and are still included.
- A final safety net lists ANY .md file that wasn't emitted by the
  curated sections, so nothing is ever silently dropped from the README.
"""

import os
from urllib.parse import quote

# Folders (relative to repo root) whose .md files are managed elsewhere
# or are internal doc trees we intentionally exclude from the README.
EXCLUDE_DIRS = (
    '.git',
    'News/TrendingGithubRepos',                     # managed via index.md by github-repos.py
    'AI-ML/Agents/Spring-Boot-4-Migration/backups',
    '.springboot-4-docs',                           # internal migration docs tree
)

# Files (basenames) that are never linked as content.
EXCLUDE_BASENAMES = {'README.md', 'index.md', 'AGENTS.md'}


def is_excluded(rel_path):
    return any(ex in rel_path for ex in EXCLUDE_DIRS)


def get_md_files(directory, recursive=True):
    """Return sorted markdown files in directory (recursive by default).

    Paths are returned relative to `directory`. Excluded dirs/files are skipped.
    """
    files = []
    if not os.path.isdir(directory):
        return files
    if recursive:
        for root, dirs, filenames in os.walk(directory):
            # prune excluded directories in-place
            dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d))]
            for f in sorted(filenames):
                if not f.endswith('.md') or f in EXCLUDE_BASENAMES:
                    continue
                full = os.path.join(root, f)
                if is_excluded(full):
                    continue
                files.append(os.path.relpath(full, directory))
    else:
        for f in sorted(os.listdir(directory)):
            full = os.path.join(directory, f)
            if f.endswith('.md') and f not in EXCLUDE_BASENAMES and not is_excluded(full):
                files.append(f)
    return sorted(files)


def list_subdirs(directory):
    """Return sorted immediate subdirectory names, excluding hidden/excluded."""
    if not os.path.isdir(directory):
        return []
    subs = []
    for d in sorted(os.listdir(directory)):
        full = os.path.join(directory, d)
        if os.path.isdir(full) and not d.startswith('.') and not is_excluded(full):
            subs.append(d)
    return subs


def format_title(filename):
    """Convert a filename to a readable title (base name only)."""
    title = os.path.basename(filename).replace('.md', '')
    title = title.replace('-', ' ').replace('_', ' ')
    if title and title[0].isdigit() and len(title) > 2 and title[1] in '-_ ':
        title = title[2:].strip()
    return title


def format_subdir_title(name):
    """Fallback readable title for an unknown subdirectory."""
    return name.replace('-', ' ').replace('_', ' ').title()


def make_link(title, path, emitted):
    """Create a markdown link with URL-encoded path; track emitted paths."""
    emitted.add(path)
    encoded_path = quote(path, safe='/')
    return f"- [{title}]({encoded_path})\n"


def emit_subdirs(base, curated, heading_level, emitted, limit=None):
    """Emit one block per subdirectory under `base`, auto-discovering folders.

    `curated` maps subdir name -> nice subtitle. Unknown subdirs are still
    emitted using an auto-generated title, so new folders are never missed.
    Subdir order: curated order first, then any remaining discovered subdirs.
    """
    content = ""
    hashes = "#" * heading_level
    discovered = list_subdirs(base)
    ordered = [s for s in curated if s in discovered] + \
              [s for s in discovered if s not in curated]
    for sub in ordered:
        subtitle = curated.get(sub, format_subdir_title(sub))
        files = get_md_files(os.path.join(base, sub), recursive=True)
        if not files:
            continue
        content += f"{hashes} {subtitle}\n"
        show = files[:limit] if limit else files
        for f in show:
            content += make_link(format_title(f), f"{base}/{sub}/{f}", emitted)
        content += "\n"
    return content


def emit_flat(base, heading, emitted, heading_level=3):
    """Emit all md files (recursive) under a single folder as one section."""
    files = get_md_files(base, recursive=True)
    if not files:
        return ""
    hashes = "#" * heading_level
    content = f"{hashes} {heading}\n"
    for f in files:
        content += make_link(format_title(f), f"{base}/{f}", emitted)
    content += "\n"
    return content


def main():
    emitted = set()  # track every content path we link, for the safety net

    content = """# 🚀 Knowledge Hub & Learning Logs

Welcome to my personal learning repository! This space serves as a central hub for my research, tech updates, and deep dives into various engineering domains.

---

## 📁 Repository Structure

```
Learnings/
├── AI-ML/                       # AI & Machine Learning
│   ├── Agents/                  # Agent frameworks, skills, MCP
│   ├── LLMs/                    # Models, architectures, inference
│   ├── RAG/                     # RAG architectures & guides
│   ├── Hardware/                # AI chips, accelerators, silicon
│   ├── Protocols/               # MCP, A2A, UCP
│   ├── Fine-Tuning/             # PEFT, training guides
│   ├── Comparisons/             # Model & tool comparisons
│   ├── Tabular-ML/              # Tabular / structured-data foundation models
│   ├── Algorithms/              # Recommendation algorithms
│   └── Programming/             # DSPy, BAML
│
├── Engineering/                 # Software Engineering
│   ├── Architecture/            # System design, scaling
│   ├── JVM/                     # Java, Spring, debugging
│   ├── Databases/               # Graph DB, PostgreSQL
│   ├── Middleware/              # Kafka, workflows
│   ├── Cloud/                   # AWS, cloud services
│   └── Languages/               # Rust, Go, WASM
│
├── Blockchain/                  # Blockchain & DLT
├── QuantumComputing/            # Quantum computing
├── DevSetup/                    # Development environment setup
├── Papers/                      # Research papers
├── Content/                     # Content creation
│   ├── Prompts/                 # LLM prompts library
│   └── LinkedIn/                # LinkedIn post refinements
├── News/                        # News & updates
│   ├── Security/                # CVEs, vulnerabilities
│   ├── Outages/                 # Service outages
│   └── Weekly-Updates/          # Weekly tech digests
├── References/                  # Quick references
├── Scripts/                     # Utility scripts
└── assets/                      # Shared images & PDFs
```

---

"""

    # ================= AI & Machine Learning =================
    content += "## 🧠 AI & Machine Learning\n\n"

    # --- Agents (auto-discovered subfolders) ---
    agent_subdirs = {
        'openclaw': '🤖 OpenClaw / Moltbot / Clawdbot',
        'nanobot': '🔬 NanoBot',
        'skills': '🎯 Agent Skills & Claude',
        'analysis': '📊 Agent Analysis',
        'frameworks': '🏗️ Agent Frameworks',
        'development': '💻 AI-Assisted Development',
        'Programming': '📝 Programming AI (DSPy, BAML)',
        'Network': '🌐 Network & Self-Hosting',
        'Spring-Boot-4-Migration': '🍃 Spring Boot 4 Migration',
    }
    content += "### 🤖 Agents & Autonomy\n\n"
    # Limit the very large Spring-Boot migration tree to its top-level files.
    for sub in ([s for s in agent_subdirs if s in list_subdirs('AI-ML/Agents')] +
                [s for s in list_subdirs('AI-ML/Agents') if s not in agent_subdirs]):
        subtitle = agent_subdirs.get(sub, format_subdir_title(sub))
        limit = 3 if sub == 'Spring-Boot-4-Migration' else None
        files = get_md_files(f'AI-ML/Agents/{sub}', recursive=True)
        if not files:
            continue
        content += f"#### {subtitle}\n"
        for f in (files[:limit] if limit else files):
            content += make_link(format_title(f), f"AI-ML/Agents/{sub}/{f}", emitted)
        content += "\n"

    # --- LLMs (auto-discovered subfolders, 'models' handled separately) ---
    llm_subdirs = {
        'architecture': '🏛️ Architecture & Inference',
        'training': '🎓 Training & Learning',
        'attention': '👁️ Attention & Neurons',
        'optimization': '⚡ Optimization & Cost',
        'economy': '📈 AI Economy & Trends',
        'reference': '📚 Reference & Glossary',
    }
    content += "\n### 🧬 LLMs & Models\n\n"
    llm_discovered = [s for s in list_subdirs('AI-ML/LLMs') if s != 'models']
    for sub in ([s for s in llm_subdirs if s in llm_discovered] +
                [s for s in llm_discovered if s not in llm_subdirs]):
        subtitle = llm_subdirs.get(sub, format_subdir_title(sub))
        files = get_md_files(f'AI-ML/LLMs/{sub}', recursive=True)
        if not files:
            continue
        content += f"#### {subtitle}\n"
        for f in files:
            content += make_link(format_title(f), f"AI-ML/LLMs/{sub}/{f}", emitted)
        content += "\n"

    # --- Models (auto-discovered vendor subfolders) ---
    if os.path.isdir('AI-ML/LLMs/models'):
        content += "#### 📦 Models\n\n"
        model_subdirs = {
            'anthropic': '🤖 Anthropic / Claude',
            'other': '🌐 Other Models (Gemma, Qwen, NVIDIA)',
        }
        content += emit_subdirs('AI-ML/LLMs/models', model_subdirs,
                                heading_level=5, emitted=emitted)

    # --- Flat AI-ML sections (auto-catch files, incl. nested) ---
    aiml_flat = [
        ('AI-ML/RAG', '📚 RAG (Retrieval Augmented Generation)'),
        ('AI-ML/Hardware', '🧱 AI Hardware'),
        ('AI-ML/Protocols', '🔗 Protocols'),
        ('AI-ML/Fine-Tuning', '🎯 Fine-Tuning'),
        ('AI-ML/Comparisons', '⚖️ Comparisons'),
        ('AI-ML/Tabular-ML', '📊 Tabular ML'),
        ('AI-ML/Algorithms', '🧮 Algorithms'),
    ]
    for base, heading in aiml_flat:
        content += "\n" + emit_flat(base, heading, emitted)

    # Any other AI-ML top-level folder not covered above (safety within AI-ML)
    covered_aiml = {'Agents', 'LLMs', 'RAG', 'Hardware', 'Protocols',
                    'Fine-Tuning', 'Comparisons', 'Tabular-ML', 'Algorithms',
                    'assets', 'docs'}
    for sub in list_subdirs('AI-ML'):
        if sub in covered_aiml:
            continue
        block = emit_flat(f'AI-ML/{sub}', f'📁 {format_subdir_title(sub)}', emitted)
        if block:
            content += "\n" + block

    content += "\n---\n\n"

    # ================= Engineering =================
    content += "## ☁️ Engineering\n\n"
    eng_sections = {
        'Architecture': '🏗️ Architecture',
        'JVM': '☕ JVM',
        'Databases': '💾 Databases',
        'Middleware': '📞 Middleware',
        'Cloud': '☁️ Cloud',
        'Languages': '💻 Languages',
    }
    eng_discovered = list_subdirs('Engineering')
    for folder in ([f for f in eng_sections if f in eng_discovered] +
                   [f for f in eng_discovered if f not in eng_sections]):
        title = eng_sections.get(folder, f'📁 {format_subdir_title(folder)}')
        content += emit_flat(f'Engineering/{folder}', title, emitted)
    content += "---\n\n"

    # ================= Blockchain =================
    content += "## ⛓️ Blockchain & DLT\n\n"
    blockchain_subdirs = {
        'ethereum': '⟠ Ethereum & Smart Contracts',
        'crypto': '💰 Crypto & Tokens',
        'enterprise': '🏢 Enterprise & Banking',
        'development': '🔧 Development & Learning',
        'reference': '📚 Reference & Categories',
    }
    content += emit_subdirs('Blockchain', blockchain_subdirs,
                            heading_level=3, emitted=emitted)
    content += "---\n\n"

    # ================= Quantum Computing =================
    q = emit_flat('QuantumComputing', '⚛️ Quantum Computing', emitted, heading_level=2)
    if q:
        content += q + "---\n\n"

    # ================= Papers =================
    content += "## 📄 Research Papers\n\n"
    papers_subdirs = {
        'deepseek': '🔍 DeepSeek Research',
        'reasoning': '🧠 Reasoning & LLMs',
        'vision': '👁️ Vision & Multimodal',
        'scaling': '📈 Scaling & Architecture',
        'meta': '📋 Meta & Academic Tools',
        'VL-JEPA': '🎥 VL-JEPA',
        'comparisons': '⚖️ Paper Comparisons',
    }
    content += emit_subdirs('Papers', papers_subdirs,
                            heading_level=3, emitted=emitted)
    # Papers root-level files
    for f in get_md_files('Papers', recursive=False):
        content += make_link(format_title(f), f"Papers/{f}", emitted)
    content += "---\n\n"

    # ================= DevSetup =================
    d = emit_flat('DevSetup', '🛠️ Development Setup', emitted, heading_level=2)
    if d:
        content += d + "---\n\n"

    # ================= Content =================
    content += "## ✍️ Content Creation\n\n"
    prompt_subdirs = {
        'coding': '💻 Coding & Development',
        'social-media': '📱 Social Media',
        'visual': '🎨 Visual & Image Generation',
        'research': '🔬 Research & Learning',
        'youtube': '📺 YouTube',
        'prompt-engineering': '🔧 Prompt Engineering',
        'misc': '📋 Miscellaneous',
    }
    content += "### 💡 Prompts\n\n"
    content += emit_subdirs('Content/Prompts', prompt_subdirs,
                            heading_level=4, emitted=emitted)
    # Root-level prompts
    root_prompts = get_md_files('Content/Prompts', recursive=False)
    if root_prompts:
        content += "#### 📁 Other\n"
        for f in root_prompts:
            content += make_link(format_title(f), f"Content/Prompts/{f}", emitted)
        content += "\n"
    # LinkedIn + any other Content subfolders
    content += emit_flat('Content/LinkedIn', '💼 LinkedIn', emitted)
    for sub in list_subdirs('Content'):
        if sub in ('Prompts', 'LinkedIn'):
            continue
        content += emit_flat(f'Content/{sub}', f'📁 {format_subdir_title(sub)}', emitted)
    content += "---\n\n"

    # ================= News =================
    content += "## 📰 News & Updates\n\n"
    news_subdirs = {
        'Security': '🛡️ Security & Vulnerabilities',
        'Outages': '🚨 Infrastructure & Outages',
        'Weekly-Updates': '📅 Weekly Updates',
    }
    news_discovered = [s for s in list_subdirs('News')
                       if not is_excluded(f'News/{s}')]
    for sub in ([s for s in news_subdirs if s in news_discovered] +
                [s for s in news_discovered if s not in news_subdirs]):
        title = news_subdirs.get(sub, f'📁 {format_subdir_title(sub)}')
        content += emit_flat(f'News/{sub}', title, emitted)
    content += "---\n\n"

    # ================= References =================
    r = emit_flat('References', '📚 References', emitted, heading_level=2)
    if r:
        content += r + "---\n\n"

    # ================= Any other top-level folder (global safety) =================
    top_covered = {'AI-ML', 'Engineering', 'Blockchain', 'QuantumComputing',
                   'Papers', 'DevSetup', 'Content', 'News', 'References',
                   'Scripts', 'assets'}
    extra = ""
    for sub in list_subdirs('.'):
        if sub in top_covered:
            continue
        extra += emit_flat(sub, f'📁 {format_subdir_title(sub)}', emitted)
    if extra:
        content += "## 📁 Other\n\n" + extra + "---\n\n"

    # ================= Scripts =================
    content += "## 🔧 Scripts\n\n"
    # Primary, described scripts first.
    content += "- [GitHub Repos & Links](Scripts/github-repos.py) - Manage repos and check/fix links\n"
    content += "- [README Generator](Scripts/generate-readme.py) - Auto-generate this README\n"
    # Auto-discover any other scripts so new ones are never missed.
    described = {'github-repos.py', 'generate-readme.py'}
    extra_scripts = sorted(
        f for f in os.listdir('Scripts')
        if (f.endswith('.py') or f.endswith('.sh')) and f not in described
    )
    for s in extra_scripts:
        title = s[:-3].replace('-', ' ').title()
        content += f"- [{title}](Scripts/{s})\n"
    content += "\n---\n\n"

    # ================= Safety net: catch anything missed =================
    all_md = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs
                   if not is_excluded(os.path.join(root, d)) and not d.startswith('.')]
        for f in files:
            if not f.endswith('.md') or f in EXCLUDE_BASENAMES:
                continue
            full = os.path.join(root, f)
            if is_excluded(full):
                continue
            all_md.append(os.path.relpath(full, '.'))
    missed = sorted(p for p in all_md if p not in emitted)
    if missed:
        content += "## 🗂️ Uncategorized (auto-added)\n\n"
        content += "_These files were not matched by a curated section. "
        content += "Consider adding a proper section in `Scripts/generate-readme.py`._\n\n"
        for p in missed:
            content += make_link(format_title(p), p, emitted)
        content += "\n---\n\n"
        print(f"⚠️  {len(missed)} file(s) landed in Uncategorized:")
        for p in missed:
            print("   -", p)

    content += "> **Last updated:** June 2026\n"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ README.md generated successfully!")
    if not missed:
        print("✅ All markdown files are covered by curated sections.")


if __name__ == '__main__':
    main()
