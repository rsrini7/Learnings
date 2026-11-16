#!/usr/bin/env python3
"""Generate Root README.md, Complete INDEX.md, and Nine Domain Hub README.md files.

Design goals:
- Single inventory discovery: scan repository once, verify every article is accounted for.
- Root README.md: high-level dashboard, domain navigation table, curated starting points,
  and repository structure tree.
- INDEX.md: complete, fully expanded single-page archive for browsing and Ctrl+F text search.
- Domain Hub READMEs: 9 dedicated landing pages (AI-ML, Engineering, Blockchain, QuantumComputing,
  Papers, DevSetup, Content, News, References) with local scope descriptions and full article listings.
- Per-domain fallback: any newly added article in a domain or domain root is automatically
  captured and indexed under a fallback section if omitted by curated subsections.
- Strict in-memory validation: coverage is verified BEFORE writing to disk; no files are modified
  if validation fails.
- Every discovered article must appear in INDEX.md; articles within configured domains must
  also appear in their domain hubs.
"""

import os
from urllib.parse import quote

# Folders relative to repo root whose .md files are managed elsewhere
# or internal trees intentionally excluded from content indexing.
EXCLUDE_DIRS = (
    '.git',
    'News/TrendingGithubRepos',
    'AI-ML/Agents/Spring-Boot-4-Migration/backups',
    '.springboot-4-docs',
)

# Files (basenames) that are navigation/meta documents, never content articles.
EXCLUDE_BASENAMES = {'README.md', 'index.md', 'INDEX.md', 'AGENTS.md'}


def is_excluded(rel_path):
    return any(ex in rel_path for ex in EXCLUDE_DIRS)


def get_md_files(directory, recursive=True):
    """Return sorted markdown files in directory (relative to `directory`)."""
    files = []
    if not os.path.isdir(directory):
        return files
    if recursive:
        for root, dirs, filenames in os.walk(directory):
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
    """Fallback readable title for a subdirectory."""
    return name.replace('-', ' ').replace('_', ' ').title()


def make_file_link(full_repo_path, rel_to='.', emitted=None):
    """Create a markdown link with URL-encoded relative path; track emitted path."""
    if emitted is not None:
        emitted.add(full_repo_path)
    rel_path = os.path.relpath(full_repo_path, rel_to)
    encoded = quote(rel_path, safe='/')
    title = format_title(full_repo_path)
    return f"- [{title}]({encoded})\n"


def emit_subdirs(base, curated, heading_level, rel_to='.', emitted=None, limit=None):
    """Emit one block per subdirectory under `base`, auto-discovering folders."""
    content = ""
    hashes = "#" * heading_level
    discovered = list_subdirs(base)
    ordered = [s for s in curated if s in discovered] + [s for s in discovered if s not in curated]
    for sub in ordered:
        subtitle = curated.get(sub, format_subdir_title(sub))
        files = get_md_files(os.path.join(base, sub), recursive=True)
        if not files:
            continue
        content += f"{hashes} {subtitle}\n"
        show = files[:limit] if limit else files
        for f in show:
            full_repo = os.path.normpath(os.path.join(base, sub, f))
            content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
        content += "\n"
    return content


def emit_flat(base, heading, heading_level, rel_to='.', emitted=None):
    """Emit all md files (recursive) under a single folder as one section."""
    files = get_md_files(base, recursive=True)
    if not files:
        return ""
    hashes = "#" * heading_level
    content = f"{hashes} {heading}\n"
    for f in files:
        full_repo = os.path.normpath(os.path.join(base, f))
        content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
    content += "\n"
    return content


# ==============================================================================
# Domain Content Builders
# ==============================================================================

def build_aiml_content(rel_to='.', emitted=None, h_offset=0):
    content = ""

    # Root-level articles in AI-ML/
    root_files = get_md_files('AI-ML', recursive=False)
    if root_files:
        content += f"{'#' * (3 + h_offset)} 📁 General AI-ML Articles\n"
        for f in root_files:
            content += make_file_link(f"AI-ML/{f}", rel_to=rel_to, emitted=emitted)
        content += "\n"

    # Agents
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
    content += f"{'#' * (3 + h_offset)} 🤖 Agents & Autonomy\n\n"
    for sub in ([s for s in agent_subdirs if s in list_subdirs('AI-ML/Agents')] +
                [s for s in list_subdirs('AI-ML/Agents') if s not in agent_subdirs]):
        subtitle = agent_subdirs.get(sub, format_subdir_title(sub))
        limit = 3 if sub == 'Spring-Boot-4-Migration' else None
        files = get_md_files(f'AI-ML/Agents/{sub}', recursive=True)
        if not files:
            continue
        content += f"{'#' * (4 + h_offset)} {subtitle}\n"
        for f in (files[:limit] if limit else files):
            full_repo = f"AI-ML/Agents/{sub}/{f}"
            content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
        content += "\n"

    # LLMs
    llm_subdirs = {
        'architecture': '🏛️ Architecture & Inference',
        'training': '🎓 Training & Learning',
        'attention': '👁️ Attention & Neurons',
        'optimization': '⚡ Optimization & Cost',
        'economy': '📈 AI Economy & Trends',
        'reference': '📚 Reference & Glossary',
    }
    content += f"\n{'#' * (3 + h_offset)} 🧬 LLMs & Models\n\n"
    llm_discovered = [s for s in list_subdirs('AI-ML/LLMs') if s != 'models']
    for sub in ([s for s in llm_subdirs if s in llm_discovered] +
                [s for s in llm_discovered if s not in llm_subdirs]):
        subtitle = llm_subdirs.get(sub, format_subdir_title(sub))
        files = get_md_files(f'AI-ML/LLMs/{sub}', recursive=True)
        if not files:
            continue
        content += f"{'#' * (4 + h_offset)} {subtitle}\n"
        for f in files:
            full_repo = f"AI-ML/LLMs/{sub}/{f}"
            content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
        content += "\n"

    # Models
    if os.path.isdir('AI-ML/LLMs/models'):
        content += f"{'#' * (4 + h_offset)} 📦 Models\n\n"
        model_subdirs = {
            'anthropic': '🤖 Anthropic / Claude',
            'other': '🌐 Other Models (Gemma, Qwen, NVIDIA)',
        }
        content += emit_subdirs('AI-ML/LLMs/models', model_subdirs,
                                heading_level=5 + h_offset, rel_to=rel_to, emitted=emitted)

    # Flat AI-ML Sections
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
        content += "\n" + emit_flat(base, heading, heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)

    # Uncovered subfolders fallback
    covered_aiml = {'Agents', 'LLMs', 'RAG', 'Hardware', 'Protocols',
                    'Fine-Tuning', 'Comparisons', 'Tabular-ML', 'Algorithms',
                    'assets', 'docs'}
    for sub in list_subdirs('AI-ML'):
        if sub in covered_aiml:
            continue
        block = emit_flat(f'AI-ML/{sub}', f'📁 {format_subdir_title(sub)}',
                          heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
        if block:
            content += "\n" + block
    return content


def build_engineering_content(rel_to='.', emitted=None, h_offset=0):
    content = ""

    # Root-level articles in Engineering/
    root_files = get_md_files('Engineering', recursive=False)
    if root_files:
        content += f"{'#' * (3 + h_offset)} 📁 General Engineering Articles\n"
        for f in root_files:
            content += make_file_link(f"Engineering/{f}", rel_to=rel_to, emitted=emitted)
        content += "\n"

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
        content += emit_flat(f'Engineering/{folder}', title,
                             heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
    return content


def build_blockchain_content(rel_to='.', emitted=None, h_offset=0):
    content = ""

    # Root-level articles in Blockchain/
    root_files = get_md_files('Blockchain', recursive=False)
    if root_files:
        content += f"{'#' * (3 + h_offset)} 📁 General Blockchain Articles\n"
        for f in root_files:
            content += make_file_link(f"Blockchain/{f}", rel_to=rel_to, emitted=emitted)
        content += "\n"

    blockchain_subdirs = {
        'ethereum': '⟠ Ethereum & Smart Contracts',
        'crypto': '💰 Crypto & Tokens',
        'enterprise': '🏢 Enterprise & Banking',
        'development': '🔧 Development & Learning',
        'reference': '📚 Reference & Categories',
    }
    content += emit_subdirs('Blockchain', blockchain_subdirs,
                            heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
    return content


def build_quantum_content(rel_to='.', emitted=None, h_offset=0):
    files = get_md_files('QuantumComputing', recursive=True)
    content = ""
    for f in files:
        full_repo = f"QuantumComputing/{f}"
        content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
    content += "\n"
    return content


def build_papers_content(rel_to='.', emitted=None, h_offset=0):
    papers_subdirs = {
        'deepseek': '🔍 DeepSeek Research',
        'reasoning': '🧠 Reasoning & LLMs',
        'vision': '👁️ Vision & Multimodal',
        'scaling': '📈 Scaling & Architecture',
        'meta': '📋 Meta & Academic Tools',
        'VL-JEPA': '🎥 VL-JEPA',
        'comparisons': '⚖️ Paper Comparisons',
    }
    content = emit_subdirs('Papers', papers_subdirs,
                           heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
    root_papers = get_md_files('Papers', recursive=False)
    if root_papers:
        content += f"{'#' * (3 + h_offset)} 📁 General Papers\n"
        for f in root_papers:
            full_repo = f"Papers/{f}"
            content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
        content += "\n"
    return content


def build_devsetup_content(rel_to='.', emitted=None, h_offset=0):
    content = ""
    root_files = get_md_files('DevSetup', recursive=False)
    if root_files:
        content += f"{'#' * (3 + h_offset)} 🖥️ Core Setup Guides\n"
        for f in root_files:
            full_repo = f"DevSetup/{f}"
            content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
        content += "\n"
    devsetup_subs = {'headroom': '⚡ Headroom & Multi-Agent Token Optimization'}
    content += emit_subdirs('DevSetup', devsetup_subs,
                            heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
    return content


def build_content_content(rel_to='.', emitted=None, h_offset=0):
    content = ""
    prompt_subdirs = {
        'coding': '💻 Coding & Development',
        'social-media': '📱 Social Media',
        'visual': '🎨 Visual & Image Generation',
        'research': '🔬 Research & Learning',
        'youtube': '📺 YouTube',
        'prompt-engineering': '🔧 Prompt Engineering',
        'misc': '📋 Miscellaneous',
    }
    content += f"{'#' * (3 + h_offset)} 💡 Prompts\n\n"
    content += emit_subdirs('Content/Prompts', prompt_subdirs,
                            heading_level=4 + h_offset, rel_to=rel_to, emitted=emitted)
    root_prompts = get_md_files('Content/Prompts', recursive=False)
    if root_prompts:
        content += f"{'#' * (4 + h_offset)} 📁 Other Prompts\n"
        for f in root_prompts:
            full_repo = f"Content/Prompts/{f}"
            content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
        content += "\n"
    content += emit_flat('Content/LinkedIn', '💼 LinkedIn',
                         heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
    for sub in list_subdirs('Content'):
        if sub in ('Prompts', 'LinkedIn'):
            continue
        content += emit_flat(f'Content/{sub}', f'📁 {format_subdir_title(sub)}',
                             heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
    return content


def build_news_content(rel_to='.', emitted=None, h_offset=0):
    content = ""

    # Root-level articles in News/
    root_files = get_md_files('News', recursive=False)
    if root_files:
        content += f"{'#' * (3 + h_offset)} 📁 General News & Updates\n"
        for f in root_files:
            content += make_file_link(f"News/{f}", rel_to=rel_to, emitted=emitted)
        content += "\n"

    news_subdirs = {
        'Security': '🛡️ Security & Vulnerabilities',
        'Outages': '🚨 Infrastructure & Outages',
        'Weekly-Updates': '📅 Weekly Updates',
    }
    news_discovered = [s for s in list_subdirs('News') if not is_excluded(f'News/{s}')]
    for sub in ([s for s in news_subdirs if s in news_discovered] +
                [s for s in news_discovered if s not in news_subdirs]):
        title = news_subdirs.get(sub, f'📁 {format_subdir_title(sub)}')
        content += emit_flat(f'News/{sub}', title,
                             heading_level=3 + h_offset, rel_to=rel_to, emitted=emitted)
    return content


def build_references_content(rel_to='.', emitted=None, h_offset=0):
    files = get_md_files('References', recursive=True)
    content = ""
    for f in files:
        full_repo = f"References/{f}"
        content += make_file_link(full_repo, rel_to=rel_to, emitted=emitted)
    content += "\n"
    return content


# ==============================================================================
# Domain Hub Metadata Configuration
# ==============================================================================

DOMAINS = [
    {
        'id': 'AI-ML',
        'name': 'AI & Machine Learning',
        'icon': '🧠',
        'hub_file': 'AI-ML/README.md',
        'builder': build_aiml_content,
        'summary': 'Autonomous agents, scalar autograd (microGPT), KV caching, prompt tokenomics, multimodal RAG, and MCP protocols.',
        'desc': (
            'In-depth research, architectural breakdowns, and hands-on implementations across the AI/ML landscape: '
            'autonomous agent architectures (OpenClaw/Moltbot, NanoBot), scalar autograd engines (`microGPT`), '
            'LLM attention mechanics, KV cache storage tiering, prompt cache tokenomics, multimodal RAG pipelines, '
            'Model Context Protocol (MCP), and accelerator silicon.'
        ),
    },
    {
        'id': 'Engineering',
        'name': 'Software Engineering',
        'icon': '☁️',
        'hub_file': 'Engineering/README.md',
        'builder': build_engineering_content,
        'summary': 'High-scale systems (1M RPS), HTTP QUERY (RFC 10008), JVM internals (Babylon & Panama), and Kafka 4.0 KRaft.',
        'desc': (
            'Deep dives into high-throughput backend systems, modern runtime internals, distributed middleware, and '
            'systems architecture: million-RPS request pipelines, safe query methods (RFC 10008), OpenJDK Project Babylon '
            '(Code Reflection), Project Panama (FFM API), carrier thread mechanics, Apache Kafka 4.0 KRaft consensus migration, '
            'and polyglot runtime benchmarks (Go SIMD, Rust WASM).'
        ),
    },
    {
        'id': 'Blockchain',
        'name': 'Blockchain & DLT',
        'icon': '⛓️',
        'hub_file': 'Blockchain/README.md',
        'builder': build_blockchain_content,
        'summary': 'Ethereum L1/L2, RWA tokenization rails (ERC-20/721/1400), Hardhat testnets, and macro crypto cycles.',
        'desc': (
            'Technical investigations and architectural whitepapers for distributed ledger systems, smart contract '
            'development, and programmable finance: Ethereum EVM state mechanics, local Hardhat Dockerized testnets, '
            'real-world asset (RWA) tokenization (ERC-20, ERC-721, ERC-1400), institutional banking rails, and '
            'cryptographic settlement models.'
        ),
    },
    {
        'id': 'QuantumComputing',
        'name': 'Quantum Computing',
        'icon': '⚛️',
        'hub_file': 'QuantumComputing/README.md',
        'builder': build_quantum_content,
        'summary': 'Qubit state mechanics, Bloch sphere geometry, Google Willow benchmarks, and post-quantum cryptography.',
        'desc': (
            'Foundational mathematics, state mechanics, and system architectures in quantum information science: '
            'qubit state vectors, superposition, Bloch sphere geometric representations, unitary quantum gates, '
            'Google Willow quantum processor benchmarks, and post-quantum cryptographic (PQC) threats to ECDSA.'
        ),
    },
    {
        'id': 'Papers',
        'name': 'Research Papers',
        'icon': '📄',
        'hub_file': 'Papers/README.md',
        'builder': build_papers_content,
        'summary': 'DeepSeek-V3/R1 co-design (MLA, DualPipe), recursive reasoning models, and VL-JEPA vision.',
        'desc': (
            'Detailed technical breakdowns and critical evaluations of seminal machine learning and systems research '
            'papers: DeepSeek-V3 and DeepSeek-R1 hardware/software co-design (MLA, DualPipe, MoE), recursive language models, '
            'vision-language predictive architectures (VL-JEPA), Google Nested Learning, and Meta Sparse Memory.'
        ),
    },
    {
        'id': 'DevSetup',
        'name': 'Development Setup',
        'icon': '🛠️',
        'hub_file': 'DevSetup/README.md',
        'builder': build_devsetup_content,
        'summary': 'Workstation environments, local model runners (llama.cpp), and Headroom / RTK multi-agent caching.',
        'desc': (
            'Practical setup playbooks, local developer runtime harnesses, and multi-agent token economics: '
            'macOS Apple Silicon workstation configuration, OpenRouter API workflows, local llama.cpp environments, '
            'and Headroom / RTK multi-agent token caching and compression proxies.'
        ),
    },
    {
        'id': 'Content',
        'name': 'Content Creation',
        'icon': '✍️',
        'hub_file': 'Content/README.md',
        'builder': build_content_content,
        'summary': 'Systematic LLM prompts for software development, technical diagramming, and concise writing.',
        'desc': (
            'Systematically categorized prompt templates, technical communication frameworks, and visual engineering '
            'formats: coding exploration prompts, multi-panel infographic prompts, social media distillation workflows, '
            'and structured technical writing roadmaps.'
        ),
    },
    {
        'id': 'News',
        'name': 'News & Updates',
        'icon': '📰',
        'hub_file': 'News/README.md',
        'builder': build_news_content,
        'summary': 'In-depth security advisories (CVEs/RCEs), major cloud outage postmortems, and weekly industry briefings.',
        'desc': (
            'Exhaustive root-cause security advisories, major cloud outage postmortems, and technology briefings: '
            'critical CVE whitepapers (RCEs, UAFs, supply chain compromises), PKI trust anchor analysis, cloud infrastructure '
            'failures (AWS, Cloudflare, Supabase), and weekly tech ecosystem updates.'
        ),
    },
    {
        'id': 'References',
        'name': 'References & Guides',
        'icon': '📚',
        'hub_file': 'References/README.md',
        'builder': build_references_content,
        'summary': 'Gang of Four (GoF) design patterns, Passkeys / WebAuthn authentication, and paper discovery guides.',
        'desc': (
            'Enduring software engineering design patterns, modern identity protocols, and academic literature discovery: '
            'Gang of Four (GoF) object-oriented design patterns, Passkeys and WebAuthn credential flows, and research '
            'paper retrieval workflows.'
        ),
    },
]


# ==============================================================================
# Domain Renderer Wrapper with Per-Domain Fallback
# ==============================================================================

def render_domain_section(d, inventory, rel_to='.', emitted=None, h_offset=0):
    """Render a domain section and automatically catch any unhandled inventory entries."""
    dom_id = d['id']
    dom_inventory = [f for f in inventory if f.startswith(dom_id + '/') or f == dom_id]

    dom_emitted = set()
    content = d['builder'](rel_to=rel_to, emitted=dom_emitted, h_offset=h_offset)

    # Per-domain fallback: catch any inventory entries belonging to this domain omitted by subsections
    unhandled = [f for f in dom_inventory if f not in dom_emitted]
    if unhandled:
        content += f"\n{'#' * (3 + h_offset)} 🗂️ Additional {d['name']} Articles (auto-added)\n\n"
        for f in sorted(unhandled):
            content += make_file_link(f, rel_to=rel_to, emitted=dom_emitted)
        content += "\n"

    if emitted is not None:
        emitted.update(dom_emitted)

    return content, dom_emitted


# ==============================================================================
# Generator Functions (In-Memory Rendering)
# ==============================================================================

def discover_inventory():
    """Discover all content markdown files on disk, excluding navigation/internal dirs."""
    all_files = set()
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d)) and not d.startswith('.')]
        for f in files:
            if not f.endswith('.md') or f in EXCLUDE_BASENAMES:
                continue
            full = os.path.join(root, f)
            if is_excluded(full):
                continue
            all_files.add(os.path.relpath(full, '.'))
    return sorted(all_files)


def render_index_md(inventory):
    """Render INDEX.md in-memory with complete single-page archive of all articles."""
    emitted = set()
    content = """# 📖 Complete Repository Index

*Curated and maintained by Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*

[← Back to Root Hub](README.md)

A complete, fully expanded single-page index of all technical articles and research notes across all engineering domains. Use this page for quick browsing, topical exploration, or full-text browser search (`Ctrl+F` / `Cmd+F`).

---

<a id="quick-jump"></a>

## 📑 Quick Jump by Domain

"""
    # Quick Jump Links with article counts
    domain_counts = {}
    for d in DOMAINS:
        dom_files = [f for f in inventory if f.startswith(d['id'] + '/')]
        domain_counts[d['id']] = len(dom_files)
        anchor = d['id'].lower()
        content += f"- [{d['icon']} {d['name']}](#{anchor}) ({len(dom_files)} articles)\n"
    content += "\n---\n\n"

    # Emit each domain in order
    for d in DOMAINS:
        anchor_id = d['id'].lower()
        content += f"<a id=\"{anchor_id}\"></a>\n\n"
        content += f"## {d['icon']} {d['name']}\n\n"
        content += f"*{d['desc']}*\n\n"
        content += f"[📂 Open Dedicated Domain Hub ({d['hub_file']})]({d['hub_file']})\n\n"
        dom_body, _ = render_domain_section(d, inventory, rel_to='.', emitted=emitted, h_offset=0)
        content += dom_body
        content += "\n[↑ Back to Quick Jump](#quick-jump) · [← Back to Root Hub](README.md)\n\n---\n\n"

    # Global fallback: any inventory files outside the 9 configured domains
    known_domains = {d['id'] for d in DOMAINS}
    unhandled_global = [f for f in inventory if f.split('/')[0] not in known_domains]
    if unhandled_global:
        content += "## 🗂️ Additional Articles (auto-added)\n\n"
        content += "_These articles were not matched by a known domain hub._\n\n"
        for f in sorted(unhandled_global):
            content += make_file_link(f, rel_to='.', emitted=emitted)
        content += "\n---\n\n"

    content += "> **Last updated:** November 2026\n"
    return content, emitted


def render_domain_hubs(inventory):
    """Render dedicated README.md files for each domain in-memory."""
    hubs = {}
    emitted_total = set()

    for d in DOMAINS:
        hub_path = d['hub_file']
        dom_id = d['id']

        content = f"""# {d['icon']} {d['name']} Knowledge Hub

*Curated and maintained by Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*

[← Back to Root Hub](../README.md) · [📖 Complete Repository Index](../INDEX.md)

---

## 📌 Scope & Focus

{d['desc']}

---

## 📑 Articles & Subcategories

"""
        dom_body, dom_emitted = render_domain_section(d, inventory, rel_to=dom_id, emitted=None, h_offset=-1)
        content += dom_body
        content += """---

[← Back to Root Hub](../README.md) · [📖 Complete Repository Index](../INDEX.md)
"""
        hubs[hub_path] = content
        emitted_total.update(dom_emitted)

    return hubs, emitted_total


def render_root_readme(inventory):
    """Render high-level root README.md dashboard in-memory."""
    domain_counts = {}
    for d in DOMAINS:
        dom_files = [f for f in inventory if f.startswith(d['id'] + '/')]
        domain_counts[d['id']] = len(dom_files)

    content = f"""# 🚀 Engineering & AI Knowledge Hub

*Curated and maintained by Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*

Welcome to the central repository for technical deep dives, architectural whitepapers, system design models, and empirical research notes across artificial intelligence, distributed systems, quantum computing, and modern software engineering.

---

## 🧭 Domain Hubs

Explore focused technical hubs with dedicated roadmaps, architecture diagrams, and complete categorized indexes:

| Domain | Hub | Scope / Focus | Articles |
|:---|:---|:---|:---:|
| 🧠 **AI & Machine Learning** | [AI-ML/README.md](AI-ML/README.md) | {DOMAINS[0]['summary']} | {domain_counts['AI-ML']} |
| ☁️ **Software Engineering** | [Engineering/README.md](Engineering/README.md) | {DOMAINS[1]['summary']} | {domain_counts['Engineering']} |
| ⛓️ **Blockchain & DLT** | [Blockchain/README.md](Blockchain/README.md) | {DOMAINS[2]['summary']} | {domain_counts['Blockchain']} |
| ⚛️ **Quantum Computing** | [QuantumComputing/README.md](QuantumComputing/README.md) | {DOMAINS[3]['summary']} | {domain_counts['QuantumComputing']} |
| 📄 **Research Papers** | [Papers/README.md](Papers/README.md) | {DOMAINS[4]['summary']} | {domain_counts['Papers']} |
| 🛠️ **Development Setup** | [DevSetup/README.md](DevSetup/README.md) | {DOMAINS[5]['summary']} | {domain_counts['DevSetup']} |
| ✍️ **Content Creation** | [Content/README.md](Content/README.md) | {DOMAINS[6]['summary']} | {domain_counts['Content']} |
| 📰 **News & Updates** | [News/README.md](News/README.md) | {DOMAINS[7]['summary']} | {domain_counts['News']} |
| 📚 **References & Guides** | [References/README.md](References/README.md) | {DOMAINS[8]['summary']} | {domain_counts['References']} |

> 📖 **Prefer a single-page list for searching?**  
> Open the **[Complete Repository Index (INDEX.md)](INDEX.md)** to browse or search (`Ctrl+F` / `Cmd+F`) all {len(inventory)} articles across all domains.

---

## 🌟 Curated Starting Points

Representative, high-depth architectural investigations and verified implementations to start with:

1. [microGPT: Scalar Autograd Engine & Transformer Architecture](AI-ML/LLMs/architecture/microGPT-Technical-Deep-Dive.md)  
   *Algorithmic walkthrough of pure-Python scalar autograd, multi-head causal attention, and complete 240-line GPT architecture.*
2. [OpenClaw / Moltbot: Autonomous Agent Security Analysis](AI-ML/Agents/openclaw/OpenClaw-Moltbot-Security-Analysis-2026.md)  
   *Comprehensive threat modeling, Shodan discovery data, and execution-node hardening for local-first autonomous agents.*
3. [HTTP QUERY Method (RFC 10008)](Engineering/Architecture/HTTP-QUERY-Method-RFC-10008-Nov-2026.md)  
   *IETF RFC 10008 analysis: safe request-body queries, idempotent semantic caching, and Gateway/WAF configuration.*
4. [Java Next-Gen Programming Models: Babylon & Panama](Engineering/JVM/Java-Next-Gen-Programming-Models-Babylon-Panama-Nov-2026.md)  
   *Deep dive into OpenJDK Project Babylon (Code Reflection / Code Models) and Project Panama (Foreign Function & Memory API).*
5. [Kafka 4.0: KRaft Consensus Architecture & Migration](Engineering/Middleware/Kafka-4.0-KRaft-Architecture-And-Migration-2026.md)  
   *Complete removal of ZooKeeper, Raft-based metadata quorum dynamics, and zero-downtime cluster cutover guide.*
6. [The Crypto Supercycle & Ethereum Tokenization](Blockchain/ethereum/Crypto-Supercycle-and-Ethereum.md)  
   *Real-world asset (RWA) tokenization mechanics, institutional settlement rails, and four-year cycle breakdown.*
7. [Quantum Computing Foundations & State Mechanics](QuantumComputing/Quantum-Computing-Foundations-And-State-Mechanics-2026.md)  
   *Qubit state vectors, superposition, Bloch sphere geometry, unitary quantum gates, and post-quantum threat analysis.*
8. [eMudhra Weak CA Keys & PKI Trust Infrastructure](News/Security/EMudhra-Weak-CA-Keys-And-PKI-Trust-Oct-2026.md)  
   *Cryptographic root failure analysis of public CA key generation, certificate revocation, and global browser trust.*
9. [DeepSeek-V3: Architecture & Hardware/Software Co-Design](Papers/deepseek/DeepSeek-V3-Architecture-And-Hardware-Software-CoDesign-2026.md)  
   *Multi-head Latent Attention (MLA), DeepSeekMoE auxiliary-loss-free routing, DualPipe pipelining, and FP8 mixed precision.*

---

## 📁 Repository Structure

```
Learnings/
├── AI-ML/                       # AI & Machine Learning ({domain_counts['AI-ML']} articles)
│   ├── Agents/                  # Agent frameworks, skills, MCP
│   ├── LLMs/                    # Models, architectures, inference
│   ├── RAG/                     # RAG architectures & guides
│   ├── Hardware/                # AI chips, accelerators, silicon
│   ├── Protocols/               # MCP, A2A, UCP
│   ├── Fine-Tuning/             # PEFT, training guides
│   ├── Comparisons/             # Model & tool comparisons
│   ├── Tabular-ML/              # Tabular / structured-data models
│   └── Algorithms/              # Recommendation algorithms
│
├── Engineering/                 # Software Engineering ({domain_counts['Engineering']} articles)
│   ├── Architecture/            # System design, scaling, RFCs
│   ├── JVM/                     # Java, Panama, Babylon, JDWP
│   ├── Databases/               # Graph DB, PostgreSQL
│   ├── Middleware/              # Kafka KRaft, workflows
│   ├── Cloud/                   # AWS, Hetzner, cloud services
│   └── Languages/               # Rust, Go, TypeScript, WASM
│
├── Blockchain/                  # Blockchain & DLT ({domain_counts['Blockchain']} articles)
│   ├── ethereum/                # Hardhat, EVM, L1/L2
│   ├── crypto/                  # Tokens, ISO 20022, Stablecoins
│   ├── enterprise/              # Institutional tokenization, RWAs
│   ├── development/             # Hedera, payment rails
│   └── reference/               # Ecosystem guides, taxonomies
│
├── QuantumComputing/            # Quantum computing & state mechanics ({domain_counts['QuantumComputing']} articles)
├── DevSetup/                    # Workstation & AI developer tooling ({domain_counts['DevSetup']} articles)
├── Papers/                      # Research papers & critical reviews ({domain_counts['Papers']} articles)
├── Content/                     # Structured prompts & technical writing ({domain_counts['Content']} articles)
├── News/                        # Security advisories, outages & weekly updates ({domain_counts['News']} articles)
├── References/                  # Quick references, GoF, Passkeys ({domain_counts['References']} articles)
├── Scripts/                     # Utility scripts & verification tools
└── assets/                      # Shared styling & chart libraries
```

---

## 🔧 Utility & Verification Scripts

- [GitHub Repos & Links](Scripts/github-repos.py) — Manage repo links, check broken references (`links`), and repair TOCs.
- [Markdown & Diagram Validator](Scripts/check-markdown.py) — Lints Mermaid diagrams, KaTeX math blocks, and SVG container overflows.
- [SVG Infographic Validator](Scripts/check-svg.py) — Validates SVG XML syntax, text bounds, and responsive viewBox integrity.
- [Hub & README Generator](Scripts/generate-readme.py) — Auto-generates root `README.md`, domain hub `README.md`s, and `INDEX.md`.

---

> **Last updated:** November 2026
"""
    return content


def main():
    print("🔍 Discovering repository inventory...")
    inventory = discover_inventory()
    print(f"📦 Total discovered articles: {len(inventory)}")

    # 1. Render all navigation artifacts in-memory
    print("\n📝 Rendering INDEX.md in-memory...")
    index_content, emitted_index = render_index_md(inventory)
    print(f"   Indexed: {len(emitted_index)} articles")

    print("\n🏛️ Rendering 9 Domain Hub READMEs in-memory...")
    domain_hubs, emitted_domains = render_domain_hubs(inventory)
    print(f"   Domain hubs emitted: {len(emitted_domains)} articles")

    print("\n🚀 Rendering Root README.md in-memory...")
    root_readme_content = render_root_readme(inventory)

    # 2. Strict Coverage Verification BEFORE touching any files on disk
    inv_set = set(inventory)
    known_domains = {d['id'] for d in DOMAINS}
    domain_inventory = {f for f in inv_set if f.split('/', 1)[0] in known_domains}
    missing_in_index = inv_set - emitted_index
    missing_in_domains = domain_inventory - emitted_domains

    if missing_in_index or missing_in_domains:
        print("\n❌ VALIDATION ERROR: In-memory coverage check failed before writing!")
        if missing_in_index:
            print(f"   Missing from INDEX.md ({len(missing_in_index)}):")
            for m in sorted(missing_in_index):
                print(f"      - {m}")
        if missing_in_domains:
            print(f"   Missing from Domain Hubs ({len(missing_in_domains)}):")
            for m in sorted(missing_in_domains):
                print(f"      - {m}")
        print("\n⚠️  No files on disk were modified.")
        raise SystemExit(1)

    # 3. Only write to disk AFTER 100% verification succeeds
    print("\n💾 Writing validated navigation files to disk...")

    with open('INDEX.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("   ✅ INDEX.md written")

    for hub_path, hub_content in domain_hubs.items():
        with open(hub_path, 'w', encoding='utf-8') as f:
            f.write(hub_content)
        print(f"   ✅ {hub_path} written")

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(root_readme_content)
    print("   ✅ README.md written")

    print("\n" + "=" * 60)
    print("✅ ZERO LOSS VERIFIED (Pre-write validation passed):")
    print(f"   • {len(inventory)}/{len(inventory)} articles present in INDEX.md")
    print(f"   • {len(domain_inventory)}/{len(domain_inventory)} configured-domain articles present in Domain Hubs")
    print("   • All 11 navigation files successfully updated on disk")
    print("=" * 60)


if __name__ == '__main__':
    main()
