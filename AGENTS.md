# 🤖 Agents Guide: Repository Conventions

> Quick reference for organizing files and verifying links in this repository.

---

## 📁 File Naming Convention

Use **Title-Case-With-Hyphens** for all markdown files:

```
✅ Hiring-Agent-Deep-Dive.md
✅ Autonomous-AI-Agents.md
❌ hiring-agent-deep-dive.md
❌ Hiring_Agent_Deep_Dive.md
```

---

## 🔄 Moving/Organizing Files Checklist

When moving or adding a new markdown file:

```bash
# 1. Move file(s) to destination folder
mv path/to/file.md destination/folder/

# 2. Rename to match naming convention
mv destination/folder/old-name.md destination/folder/New-Name.md

# 3. Move associated images to same folder
mv path/to/*.png destination/folder/

# 4. Update README.md under appropriate section
# Add: - [Display Name](destination/folder/New-Name.md)

# 5. Add Related section at bottom of file (see format below)

# 6. Verify all links
python3 Scripts/github-repos.py links

# 7. Fix broken links if needed
python3 Scripts/github-repos.py links --fix
```

---

## 📎 Related Section Format

Add at the bottom of each document:

```markdown
---

## Related

- [Related Document Title](../relative/path/to/file.md) — Brief description of relevance.
- [Another Document](../path/to/file.md) — How it relates to current document.
```

---

## 🔗 Link Verification

Always run after reorganizing files:

```bash
# Check for broken links
python3 Scripts/github-repos.py links

# Auto-fix broken links
python3 Scripts/github-repos.py links --fix
```

---

## 📂 Repository Structure

```
Learnings/
├── AI-ML/                       # AI & Machine Learning
│   ├── Agents/                  # Agent frameworks, analysis
│   ├── LLMs/                    # Models, architectures
│   ├── RAG/                     # RAG architectures
│   ├── Hardware/                # AI chips
│   ├── Protocols/               # MCP, A2A, UCP
│   ├── Fine-Tuning/             # Training guides
│   └── Comparisons/             # Model comparisons
├── Engineering/                 # Software Engineering
├── Blockchain/                  # Blockchain & DLT
├── News/                        # News & updates
├── Papers/                      # Research papers
├── Scripts/                     # Utility scripts
└── assets/                      # Shared images
```

---

## ⚠️ Common Mistakes to Avoid

1. **Forgetting to update README** — Always add link to appropriate section
2. **Wrong file naming** — Use Title-Case-With-Hyphens, not lowercase
3. **Missing Related section** — Every doc should link to related content
4. **Not verifying links** — Always run `links` check after moving files
5. **Orphaned images** — Move PNGs with their markdown file to same folder

---

> **Last updated:** July 2026
