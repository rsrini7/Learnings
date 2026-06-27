#!/usr/bin/env python3
"""Generate README.md with all file links"""

import os
from pathlib import Path
from urllib.parse import quote

def get_md_files(directory, recursive=False):
    """Get all markdown files in directory"""
    files = []
    if os.path.exists(directory):
        if recursive:
            for root, dirs, filenames in os.walk(directory):
                for f in sorted(filenames):
                    if f.endswith('.md'):
                        rel_path = os.path.relpath(os.path.join(root, f), directory)
                        files.append(rel_path)
        else:
            for f in sorted(os.listdir(directory)):
                if f.endswith('.md'):
                    files.append(f)
    return files

def format_title(filename):
    """Convert filename to readable title"""
    title = filename.replace('.md', '')
    title = title.replace('-', ' ')
    title = title.replace('_', ' ')
    # Remove leading numbers with dash
    if title and title[0].isdigit() and len(title) > 2 and title[1] in '-_ ':
        title = title[2:].strip()
    return title

def make_link(title, path):
    """Create markdown link with URL-encoded path"""
    encoded_path = quote(path, safe='/')
    return f"- [{title}]({encoded_path})\n"

def main():
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
│   ├── Protocols/               # MCP, A2A, UCP
│   ├── Fine-Tuning/             # PEFT, training guides
│   ├── Comparisons/             # Model & tool comparisons
│   ├── Algorithms/              # Recommendation algorithms
│   └── Programming/             # DSPy, BAML
│
├── Engineering/                 # Software Engineering
│   ├── Architecture/            # System design, scaling
│   ├── JVM/                     # Java, Spring, debugging
│   ├── Databases/               # Graph DB, PostgreSQL
│   ├── Middleware/               # Kafka, workflows
│   ├── Cloud/                   # AWS, cloud services
│   └── Languages/               # Rust, Go, WASM
│
├── Blockchain/                  # Blockchain & DLT
├── Quantum-Computing/           # Quantum computing
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

    # AI-ML Section
    content += "## 🧠 AI & Machine Learning\n\n"
    
    # Agents with subcategories
    agent_subdirs = {
        'openclaw': '🤖 OpenClaw / Moltbot / Clawdbot',
        'nanobot': '🔬 NanoBot',
        'skills': '🎯 Agent Skills & Claude',
        'frameworks': '🏗️ Agent Frameworks',
        'development': '💻 AI-Assisted Development',
        'Programming': '📝 Programming AI (DSPy, BAML)',
        'Network': '🌐 Network & Self-Hosting'
    }
    
    content += "### 🤖 Agents & Autonomy\n\n"
    for subdir, subtitle in agent_subdirs.items():
        files = get_md_files(f'AI-ML/Agents/{subdir}')
        if files:
            content += f"#### {subtitle}\n"
            for f in files:
                title = format_title(f)
                content += make_link(title, f"AI-ML/Agents/{subdir}/{f}")
            content += "\n"
    
    # Spring Boot Migration
    spring_files = get_md_files('AI-ML/Agents/Spring-Boot-4-Migration', recursive=True)
    if spring_files:
        content += "#### 🍃 Spring Boot 4 Migration\n"
        for f in spring_files[:3]:  # Show top 3 only
            title = format_title(f)
            content += make_link(title, f"AI-ML/Agents/Spring-Boot-4-Migration/{f}")
        content += "\n"
    
    # LLMs with subcategories
    llm_subdirs = {
        'architecture': '🏛️ Architecture & Inference',
        'training': '🎓 Training & Learning',
        'attention': '👁️ Attention & Neurons',
        'optimization': '⚡ Optimization & Cost',
        'economy': '📈 AI Economy & Trends',
        'reference': '📚 Reference & Glossary'
    }
    
    content += "\n### 🧬 LLMs & Models\n\n"
    for subdir, subtitle in llm_subdirs.items():
        files = get_md_files(f'AI-ML/LLMs/{subdir}')
        if files:
            content += f"#### {subtitle}\n"
            for f in files:
                title = format_title(f)
                content += make_link(title, f"AI-ML/LLMs/{subdir}/{f}")
            content += "\n"
    
    # Models with subcategories
    content += "#### 📦 Models\n\n"
    model_subdirs = {
        'anthropic': '🤖 Anthropic / Claude',
        'other': '🌐 Other Models (Gemma, Qwen, NVIDIA)'
    }
    for subdir, subtitle in model_subdirs.items():
        files = get_md_files(f'AI-ML/LLMs/models/{subdir}')
        if files:
            content += f"##### {subtitle}\n"
            for f in files:
                title = format_title(f)
                content += make_link(title, f"AI-ML/LLMs/models/{subdir}/{f}")
            content += "\n"
    
    # RAG
    rag = get_md_files('AI-ML/RAG')
    if rag:
        content += "\n### 📚 RAG (Retrieval Augmented Generation)\n"
        for f in rag:
            title = format_title(f)
            content += make_link(title, f"AI-ML/RAG/{f}")
        content += "\n"
    
    # Protocols
    protocols = get_md_files('AI-ML/Protocols')
    if protocols:
        content += "\n### 🔗 Protocols\n"
        for f in protocols:
            title = format_title(f)
            content += make_link(title, f"AI-ML/Protocols/{f}")
        content += "\n"
    
    # Fine-Tuning
    ft = get_md_files('AI-ML/Fine-Tuning')
    if ft:
        content += "\n### 🎯 Fine-Tuning\n"
        for f in ft:
            title = format_title(f)
            content += make_link(title, f"AI-ML/Fine-Tuning/{f}")
        content += "\n"
    
    # Comparisons
    comps = get_md_files('AI-ML/Comparisons')
    if comps:
        content += "\n### ⚖️ Comparisons\n"
        for f in comps:
            title = format_title(f)
            content += make_link(title, f"AI-ML/Comparisons/{f}")
        content += "\n"
    
    content += "\n---\n\n"
    
    # Engineering Section
    content += "## ☁️ Engineering\n\n"
    
    eng_sections = {
        'Architecture': '🏗️ Architecture',
        'JVM': '☕ JVM',
        'Databases': '💾 Databases',
        'Middleware': '📞 Middleware',
        'Cloud': '☁️ Cloud',
        'Languages': '💻 Languages'
    }
    
    for folder, title in eng_sections.items():
        files = get_md_files(f'Engineering/{folder}')
        if files:
            content += f"### {title}\n"
            for f in files:
                t = format_title(f)
                content += make_link(t, f"Engineering/{folder}/{f}")
            content += "\n"
    
    content += "---\n\n"
    
    # Blockchain with subcategories
    blockchain_subdirs = {
        'ethereum': '⟠ Ethereum & Smart Contracts',
        'crypto': '💰 Crypto & Tokens',
        'enterprise': '🏢 Enterprise & Banking',
        'development': '🔧 Development & Learning',
        'reference': '📚 Reference & Categories'
    }
    
    content += "## ⛓️ Blockchain & DLT\n\n"
    for subdir, subtitle in blockchain_subdirs.items():
        files = get_md_files(f'Blockchain/{subdir}')
        if files:
            content += f"### {subtitle}\n"
            for f in files:
                title = format_title(f)
                content += make_link(title, f"Blockchain/{subdir}/{f}")
            content += "\n"
    content += "---\n\n"
    
    # Quantum Computing
    quantum = get_md_files('Quantum-Computing')
    if quantum:
        content += "## ⚛️ Quantum Computing\n"
        for f in quantum:
            title = format_title(f)
            content += make_link(title, f"Quantum-Computing/{f}")
        content += "\n---\n\n"
    
    # Papers with subcategories
    papers_subdirs = {
        'deepseek': '🔍 DeepSeek Research',
        'reasoning': '🧠 Reasoning & LLMs',
        'vision': '👁️ Vision & Multimodal',
        'scaling': '📈 Scaling & Architecture',
        'meta': '📋 Meta & Academic Tools'
    }
    
    content += "## 📄 Research Papers\n\n"
    for subdir, subtitle in papers_subdirs.items():
        files = get_md_files(f'Papers/{subdir}')
        if files:
            content += f"### {subtitle}\n"
            for f in files:
                title = format_title(f)
                content += make_link(title, f"Papers/{subdir}/{f}")
            content += "\n"
    
    # VL-JEPA subfolder
    vl_jepa = get_md_files('Papers/VL-JEPA')
    if vl_jepa:
        content += "### 🎥 VL-JEPA\n"
        for f in vl_jepa:
            title = format_title(f)
            content += make_link(title, f"Papers/VL-JEPA/{f}")
        content += "\n"
    
    # Comparisons subfolder
    comparisons = get_md_files('Papers/comparisons')
    if comparisons:
        content += "### ⚖️ Paper Comparisons\n"
        for f in comparisons:
            title = format_title(f)
            content += make_link(title, f"Papers/comparisons/{f}")
        content += "\n"
    content += "---\n\n"
    
    # DevSetup
    devsetup = get_md_files('DevSetup')
    if devsetup:
        content += "## 🛠️ Development Setup\n"
        for f in devsetup:
            title = format_title(f)
            content += make_link(title, f"DevSetup/{f}")
        content += "\n---\n\n"
    
    # Content
    content += "## ✍️ Content Creation\n\n"
    
    # Prompts with subcategories
    prompt_subdirs = {
        'coding': '💻 Coding & Development',
        'social-media': '📱 Social Media',
        'visual': '🎨 Visual & Image Generation',
        'research': '🔬 Research & Learning',
        'youtube': '📺 YouTube',
        'prompt-engineering': '🔧 Prompt Engineering',
        'misc': '📋 Miscellaneous'
    }
    
    content += "### 💡 Prompts\n\n"
    for subdir, subtitle in prompt_subdirs.items():
        files = get_md_files(f'Content/Prompts/{subdir}')
        if files:
            content += f"#### {subtitle}\n"
            for f in files:
                title = format_title(f)
                content += make_link(title, f"Content/Prompts/{subdir}/{f}")
            content += "\n"
    
    # Root level prompts (if any)
    root_prompts = [f for f in get_md_files('Content/Prompts') if f.endswith('.md')]
    if root_prompts:
        content += "#### 📁 Other\n"
        for f in root_prompts:
            title = format_title(f)
            content += make_link(title, f"Content/Prompts/{f}")
        content += "\n"
    
    linkedin = get_md_files('Content/LinkedIn')
    if linkedin:
        content += "\n### 💼 LinkedIn\n"
        for f in linkedin:
            title = format_title(f)
            content += make_link(title, f"Content/LinkedIn/{f}")
        content += "\n"
    
    content += "---\n\n"
    
    # News Section
    content += "## 📰 News & Updates\n\n"
    
    security = get_md_files('News/Security')
    if security:
        content += "### 🛡️ Security & Vulnerabilities\n"
        for f in security:
            title = format_title(f)
            content += make_link(title, f"News/Security/{f}")
        content += "\n"
    
    outages = get_md_files('News/Outages')
    if outages:
        content += "### 🚨 Infrastructure & Outages\n"
        for f in outages:
            title = format_title(f)
            content += make_link(title, f"News/Outages/{f}")
        content += "\n"
    
    weekly = get_md_files('News/Weekly-Updates')
    if weekly:
        content += "### 📅 Weekly Updates\n"
        for f in weekly:
            title = format_title(f)
            content += make_link(title, f"News/Weekly-Updates/{f}")
        content += "\n"
    
    content += "---\n\n"
    
    # References
    refs = get_md_files('References')
    if refs:
        content += "## 📚 References\n"
        for f in refs:
            title = format_title(f)
            content += make_link(title, f"References/{f}")
        content += "\n---\n\n"
    
    # Scripts
    content += "## 🔧 Scripts\n\n"
    content += "- [GitHub Repos & Links](Scripts/github-repos.py) - Manage repos and check/fix links\n"
    content += "- [README Generator](Scripts/generate-readme.py) - Auto-generate this README\n\n"
    content += "---\n\n"
    
    content += "> **Last updated:** June 2026\n"
    
    # Write README with UTF-8 encoding
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README.md generated successfully!")

if __name__ == '__main__':
    main()
