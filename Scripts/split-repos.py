#!/usr/bin/env python3
"""Split consolidated.md into category subfolders"""

import re
import os
from datetime import datetime

def parse_consolidated(filepath):
    """Parse consolidated.md and extract repos by category"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract categories and their repos
    categories = {}
    current_cat = None
    
    for line in content.split('\n'):
        # Match category headers like "## 🤖 AI & Machine Learning (107)"
        cat_match = re.match(r'^## (.+?) \((\d+)\)$', line)
        if cat_match:
            current_cat = cat_match.group(1)
            categories[current_cat] = []
            continue
        
        # Match repo lines like "- **[name](url)** ..."
        if current_cat and line.startswith('- **['):
            # Check if it's a 404 repo
            if 'Repo not found (404)' not in line:
                categories[current_cat].append(line)
    
    return categories

def create_slug(name):
    """Convert category name to folder slug"""
    # Remove emoji and clean up
    slug = re.sub(r'[^\w\s-]', '', name).strip()
    slug = re.sub(r'[\s]+', '-', slug).lower()
    return slug

def generate_category_md(cat_name, repos):
    """Generate markdown for a category"""
    md = f"""# {cat_name}

> Trending GitHub repositories in this category.
> Auto-generated on {datetime.now().strftime('%B %d, %Y')}

---

## Repositories ({len(repos)}

"""
    for repo in repos:
        md += repo + '\n'
    
    md += f"""
---

> **Last updated:** {datetime.now().strftime('%B %Y')}
"""
    return md

def generate_index_md(categories, total_repos, active_repos):
    """Generate index.md"""
    md = f"""# 🔥 Trending GitHub Repositories (Apr-Jun 2026)

> Curated collection of trending repositories from various sources.
> Organized by category for easy browsing.

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Active Repos | {active_repos} |
| Categories | {len(categories)} |

---

## 📁 Categories

| Category | Repos | Link |
|----------|-------|------|
"""
    
    for cat_name, repos in sorted(categories.items(), key=lambda x: -len(x[1])):
        slug = create_slug(cat_name)
        md += f"| {cat_name} | {len(repos)} | [{slug}](./{slug}/index.md) |\n"
    
    md += f"""
---

## 🔗 Quick Links

"""
    
    for cat_name, repos in sorted(categories.items(), key=lambda x: -len(x[1])):
        slug = create_slug(cat_name)
        md += f"- [{cat_name}](./{slug}/index.md) ({len(repos)} repos)\n"
    
    md += f"""
---

## 📂 Structure

```
News/TrendingGithubRepos/
├── index.md                    # This file
├── ai-machine-learning/
│   └── index.md               # AI & ML repos
├── developer-tools/
│   └── index.md               # Dev tools repos
├── web-development/
│   └── index.md               # Web dev repos
└── ...                        # Other categories
```

---

> **Last updated:** {datetime.now().strftime('%B %Y')}
"""
    return md

def main():
    base_dir = 'News/TrendingGithubRepos'
    consolidated_file = os.path.join(base_dir, 'consolidated.md')
    
    print("📥 Parsing consolidated.md...")
    categories = parse_consolidated(consolidated_file)
    
    total_repos = sum(len(repos) for repos in categories.values())
    print(f"   Found {len(categories)} categories with {total_repos} active repos\n")
    
    # Create category folders
    print("📁 Creating category folders...")
    for cat_name, repos in categories.items():
        if not repos:
            continue
        
        slug = create_slug(cat_name)
        cat_dir = os.path.join(base_dir, slug)
        os.makedirs(cat_dir, exist_ok=True)
        
        # Generate category markdown
        cat_md = generate_category_md(cat_name, repos)
        cat_file = os.path.join(cat_dir, 'index.md')
        
        with open(cat_file, 'w', encoding='utf-8') as f:
            f.write(cat_md)
        
        print(f"   ✅ {slug}/index.md ({len(repos)} repos)")
    
    # Generate index.md
    print("\n📝 Generating index.md...")
    index_md = generate_index_md(categories, total_repos, total_repos)
    index_file = os.path.join(base_dir, 'index.md')
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_md)
    
    print(f"   ✅ index.md")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"✅ Done!")
    print(f"\n📊 Category breakdown:")
    for cat_name, repos in sorted(categories.items(), key=lambda x: -len(x[1])):
        print(f"   {cat_name}: {len(repos)}")
    
    print(f"\n📂 Structure created:")
    print(f"   {base_dir}/")
    print(f"   ├── index.md")
    for cat_name in sorted(categories.keys()):
        if categories[cat_name]:
            slug = create_slug(cat_name)
            print(f"   ├── {slug}/")
            print(f"   │   └── index.md")
    
    print(f"\n⚠️  consolidated.md NOT deleted yet.")
    print(f"   Review the new structure, then delete manually.")

if __name__ == '__main__':
    main()
