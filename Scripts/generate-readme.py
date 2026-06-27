#!/usr/bin/env python3
"""Generate README.md with all file links"""

import os
from pathlib import Path

def get_md_files(directory):
    """Get all markdown files in directory"""
    files = []
    if os.path.exists(directory):
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
    if title[0].isdigit() and len(title) > 2 and title[1] in '-_ ':
        title = title[2:].strip()
    return title

def main():
    base_dir = Path('.')
    
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
    
    # Agents
    agents = get_md_files('AI-ML/Agents')
    if agents:
        content += "### 🤖 Agents & Autonomy\n"
        for f in agents:
            title = format_title(f)
            content += f"- [{title}](AI-ML/Agents/{f})\n"
        content += "\n"
    
    # LLMs
    llms = get_md_files('AI-ML/LLMs')
    if llms:
        content += "### 🧬 LLMs & Models\n"
        for f in llms:
            title = format_title(f)
            content += f"- [{title}](AI-ML/LLMs/{f})\n"
        content += "\n"
    
    # RAG
    rag = get_md_files('AI-ML/RAG')
    if rag:
        content += "### 📚 RAG (Retrieval Augmented Generation)\n"
        for f in rag:
            title = format_title(f)
            content += f"- [{title}](AI-ML/RAG/{f})\n"
        content += "\n"
    
    # Protocols
    protocols = get_md_files('AI-ML/Protocols')
    if protocols:
        content += "### 🔗 Protocols\n"
        for f in protocols:
            title = format_title(f)
            content += f"- [{title}](AI-ML/Protocols/{f})\n"
        content += "\n"
    
    # Fine-Tuning
    ft = get_md_files('AI-ML/Fine-Tuning')
    if ft:
        content += "### 🎯 Fine-Tuning\n"
        for f in ft:
            title = format_title(f)
            content += f"- [{title}](AI-ML/Fine-Tuning/{f})\n"
        content += "\n"
    
    # Comparisons
    comps = get_md_files('AI-ML/Comparisons')
    if comps:
        content += "### ⚖️ Comparisons\n"
        for f in comps:
            title = format_title(f)
            content += f"- [{title}](AI-ML/Comparisons/{f})\n"
        content += "\n"
    
    content += "---\n\n"
    
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
                content += f"- [{t}](Engineering/{folder}/{f})\n"
            content += "\n"
    
    content += "---\n\n"
    
    # Blockchain
    blockchain = get_md_files('Blockchain')
    if blockchain:
        content += "## ⛓️ Blockchain & DLT\n"
        for f in blockchain:
            title = format_title(f)
            content += f"- [{title}](Blockchain/{f})\n"
        content += "\n---\n\n"
    
    # Quantum Computing
    quantum = get_md_files('Quantum-Computing')
    if quantum:
        content += "## ⚛️ Quantum Computing\n"
        for f in quantum:
            title = format_title(f)
            content += f"- [{title}](Quantum-Computing/{f})\n"
        content += "\n---\n\n"
    
    # Papers
    papers = get_md_files('Papers')
    if papers:
        content += "## 📄 Research Papers\n"
        for f in papers:
            title = format_title(f)
            content += f"- [{title}](Papers/{f})\n"
        content += "\n---\n\n"
    
    # DevSetup
    devsetup = get_md_files('DevSetup')
    if devsetup:
        content += "## 🛠️ Development Setup\n"
        for f in devsetup:
            title = format_title(f)
            content += f"- [{title}](DevSetup/{f})\n"
        content += "\n---\n\n"
    
    # Content
    content += "## ✍️ Content Creation\n\n"
    
    prompts = get_md_files('Content/Prompts')
    if prompts:
        content += "### 💡 Prompts\n"
        for f in prompts:
            title = format_title(f)
            content += f"- [{title}](Content/Prompts/{f})\n"
        content += "\n"
    
    linkedin = get_md_files('Content/LinkedIn')
    if linkedin:
        content += "### 💼 LinkedIn\n"
        for f in linkedin:
            title = format_title(f)
            content += f"- [{title}](Content/LinkedIn/{f})\n"
        content += "\n"
    
    content += "---\n\n"
    
    # News Section
    content += "## 📰 News & Updates\n\n"
    
    security = get_md_files('News/Security')
    if security:
        content += "### 🛡️ Security & Vulnerabilities\n"
        for f in security:
            title = format_title(f)
            content += f"- [{title}](News/Security/{f})\n"
        content += "\n"
    
    outages = get_md_files('News/Outages')
    if outages:
        content += "### 🚨 Infrastructure & Outages\n"
        for f in outages:
            title = format_title(f)
            content += f"- [{title}](News/Outages/{f})\n"
        content += "\n"
    
    weekly = get_md_files('News/Weekly-Updates')
    if weekly:
        content += "### 📅 Weekly Updates\n"
        for f in weekly:
            title = format_title(f)
            content += f"- [{title}](News/Weekly-Updates/{f})\n"
        content += "\n"
    
    content += "---\n\n"
    
    # References
    refs = get_md_files('References')
    if refs:
        content += "## 📚 References\n"
        for f in refs:
            title = format_title(f)
            content += f"- [{title}](References/{f})\n"
        content += "\n---\n\n"
    
    # Scripts
    content += "## 🔧 Scripts\n\n"
    content += "- [Link Checker](Scripts/check-links.sh) - Scan markdown files for broken links\n\n"
    content += "---\n\n"
    
    content += "> **Last updated:** June 2026\n"
    
    # Write README
    with open('README.md', 'w') as f:
        f.write(content)
    
    print("✅ README.md generated successfully!")
    
    # Print summary
    total_files = 0
    for section in ['AI-ML/Agents', 'AI-ML/LLMs', 'AI-ML/RAG', 'AI-ML/Protocols', 
                     'AI-ML/Fine-Tuning', 'AI-ML/Comparisons', 'Engineering/Architecture',
                     'Engineering/JVM', 'Engineering/Databases', 'Engineering/Middleware',
                     'Engineering/Cloud', 'Engineering/Languages', 'Blockchain',
                     'Quantum-Computing', 'Papers', 'DevSetup', 'Content/Prompts',
                     'Content/LinkedIn', 'News/Security', 'News/Outages', 
                     'News/Weekly-Updates', 'References']:
        files = get_md_files(section)
        total_files += len(files)
    
    print(f"📊 Total files linked: {total_files}")

if __name__ == '__main__':
    main()
