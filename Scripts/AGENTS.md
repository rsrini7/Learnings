# 🤖 Agents Guide: Scripts & Tools

> Guide for AI agents and developers on how to use the repository scripts.

---

## 📁 Scripts Overview

```
Scripts/
├── github-repos.py      # GitHub repos, links, TOC management
├── generate-readme.py   # README generator
└── hpi.sh               # Homebrew installer
```

---

## 🔧 github-repos.py

All-in-one tool for managing GitHub trending repos and markdown links.

### Repository Commands

#### Fetch repos from GitHub API
```bash
python3 Scripts/github-repos.py fetch
```
- Fetches info for all repos in `News/TrendingGithubRepos/consolidated.md`
- Auto-recovers 404 repos via GitHub Search API
- Updates descriptions, stars, language tags

#### Split into category folders
```bash
python3 Scripts/github-repos.py split
```
- Splits `consolidated.md` into category subfolders
- Creates `index.md` with links to all categories
- Structure: `News/TrendingGithubRepos/<category>/index.md`

#### Recover 404 repos
```bash
python3 Scripts/github-repos.py recover
```
- Scans for 404-marked repos
- Attempts recovery via GitHub Search API
- Prints recovery report (dry run)

#### List 404 repos
```bash
python3 Scripts/github-repos.py list404
```
- Lists all repos marked as 404 in consolidated.md

#### Check specific repo
```bash
python3 Scripts/github-repos.py check <owner/repo>
```
- Fetches info for a specific repo
- Shows description, stars, language
- Tries README if description missing

#### Show statistics
```bash
python3 Scripts/github-repos.py stats
```
- Shows total repos, categories, 404 count

---

### Link Commands

#### Check broken links
```bash
python3 Scripts/github-repos.py links
```
- Scans all markdown files for broken links
- Checks image references, file links
- Reports broken links by file

#### Fix broken links
```bash
python3 Scripts/github-repos.py links --fix
```
- Finds broken links
- Searches for target files in common locations
- Updates links to correct paths
- Removes links to deleted files

#### Fix Table of Contents
```bash
python3 Scripts/github-repos.py fixtoc
```
- Finds TOC items without links
- Creates proper anchor links
- Fixes all files with TOC sections

#### Preview TOC fixes
```bash
python3 Scripts/github-repos.py fixtoc --dry-run
```
- Shows what would be fixed without changing files

---

### Options

| Option | Description |
|--------|-------------|
| `--file <path>` | Specify consolidated.md path |
| `--no-recover` | Disable 404 recovery (for fetch) |
| `--fix` | Auto-fix broken links |
| `--dry-run` | Preview changes |

---

### Environment

```bash
# Set GitHub token for higher rate limits (5000 req/hour)
export GITHUB_TOKEN=your_token_here

# Or create token file
echo "your_token" > ~/.github_token
```

---

## 📝 generate-readme.py

Generates README.md with links to all files.

```bash
python3 Scripts/generate-readme.py
```

### What it does
- Scans all markdown files in the repository
- Categorizes by directory structure
- Generates `index.md` and `README.md`
- URL-encodes special characters in links

### When to use
- After adding new files
- After reorganizing directory structure
- After renaming files

---

## 🍺 hpi.sh

Homebrew Package Installer.

```bash
./Scripts/hpi.sh
```

---

## 🔄 Common Workflows

### 1. Add new trending repos

```bash
# 1. Fetch repo info
python3 Scripts/github-repos.py fetch

# 2. Split into categories
python3 Scripts/github-repos.py split

# 3. Regenerate README
python3 Scripts/generate-readme.py
```

### 2. Fix all links after reorganization

```bash
# 1. Check broken links
python3 Scripts/github-repos.py links

# 2. Fix broken links
python3 Scripts/github-repos.py links --fix

# 3. Fix TOC links
python3 Scripts/github-repos.py fixtoc

# 4. Regenerate README
python3 Scripts/generate-readme.py
```

### 3. Check specific repo

```bash
python3 Scripts/github-repos.py check apple/coreai-models
```

### 4. Recover deleted repos

```bash
# 1. Try recovery
python3 Scripts/github-repos.py recover

# 2. Fetch with recovery
python3 Scripts/github-repos.py fetch

# 3. Check remaining 404s
python3 Scripts/github-repos.py list404
```

---

## 📊 Repository Structure

```
Learnings/
├── AI-ML/                    # AI & Machine Learning
│   ├── Agents/               # Agent frameworks
│   ├── LLMs/                 # Models, architectures
│   ├── RAG/                  # RAG guides
│   ├── Protocols/            # MCP, A2A, UCP
│   └── ...
├── Engineering/              # Software Engineering
├── Blockchain/               # Blockchain & DLT
├── News/
│   └── TrendingGithubRepos/  # Trending repos
│       ├── index.md          # Main index
│       ├── ai-machine-learning/
│       ├── developer-tools/
│       └── ...
├── Scripts/                  # Utility scripts
└── assets/                   # Shared images
```

---

## ⚠️ Important Notes

1. **Always run `links` after reorganization** to catch broken references
2. **Use `--dry-run` first** for `fixtoc` to preview changes
3. **Set GITHUB_TOKEN** for higher API rate limits
4. **Regenerate README** after adding new files
5. **Commit after changes** to track modifications

---

## 🔗 Quick Reference

| Task | Command |
|------|---------|
| Fetch repos | `github-repos.py fetch` |
| Split categories | `github-repos.py split` |
| Check links | `github-repos.py links` |
| Fix links | `github-repos.py links --fix` |
| Fix TOC | `github-repos.py fixtoc` |
| Check repo | `github-repos.py check <repo>` |
| Show stats | `github-repos.py stats` |
| Generate README | `generate-readme.py` |

---

> **Last updated:** June 2026
