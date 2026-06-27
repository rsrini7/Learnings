#!/usr/bin/env python3
"""Fetch GitHub repo descriptions and update consolidated.md"""

import re
import urllib.request
import json
import time
from urllib.error import URLError

def extract_repos(filepath):
    """Extract GitHub repo URLs from file"""
    repos = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match GitHub URLs - handle both direct URLs and markdown links
    # Pattern for: https://github.com/owner/repo
    pattern = r'https://github\.com/([a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+)'
    matches = re.findall(pattern, content)
    
    # Deduplicate while preserving order
    seen = set()
    for repo in matches:
        repo = repo.rstrip('/')
        # Skip if it looks like a file path or invalid
        if '.' in repo.split('/')[-1] and not repo.endswith('.git'):
            continue
        if repo not in seen and '/' in repo and len(repo.split('/')[1]) > 0:
            seen.add(repo)
            repos.append(repo)
    
    return repos

def get_github_token():
    """Get GitHub token from environment or file"""
    import os
    # Try environment variable
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token
    
    # Try file
    token_file = os.path.expanduser('~/.github_token')
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read().strip()
    
    return None

def fetch_repo_info(repo_path, token=None):
    """Fetch repo info from GitHub API"""
    url = f"https://api.github.com/repos/{repo_path}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        if token:
            headers['Authorization'] = f'token {token}'
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                'name': data.get('name', repo_path.split('/')[-1]),
                'full_name': data.get('full_name', repo_path),
                'description': data.get('description', 'No description available'),
                'stars': data.get('stargazers_count', 0),
                'language': data.get('language', 'N/A'),
                'topics': data.get('topics', []),
                'url': data.get('html_url', f"https://github.com/{repo_path}"),
                'archived': data.get('archived', False),
                'fork': data.get('fork', False)
            }
    except (URLError, Exception) as e:
        return {
            'name': repo_path.split('/')[-1],
            'full_name': repo_path,
            'description': f'Could not fetch info',
            'stars': 0,
            'language': 'N/A',
            'topics': [],
            'url': f"https://github.com/{repo_path}",
            'archived': False,
            'fork': False
        }

def categorize_repo(info):
    """Categorize repo based on description and topics"""
    desc = (info.get('description', '') or '').lower()
    topics = [t.lower() for t in info.get('topics', [])]
    lang = (info.get('language', '') or '').lower()
    name = info.get('name', '').lower()
    
    # AI/ML keywords
    ai_keywords = ['ai', 'llm', 'gpt', 'claude', 'agent', 'machine-learning', 'deep-learning', 
                   'neural', 'transformer', 'rag', 'embedding', 'fine-tune', 'inference',
                   'openai', 'anthropic', 'model', 'prompt', 'copilot']
    
    # DevTools keywords
    dev_keywords = ['cli', 'terminal', 'ide', 'editor', 'code', 'developer', 'programming',
                    'debug', 'lint', 'format', 'build', 'compile', 'git', 'github', 'dev']
    
    # Web keywords
    web_keywords = ['web', 'frontend', 'backend', 'api', 'http', 'rest', 'graphql', 'react',
                    'vue', 'angular', 'nextjs', 'node', 'browser', 'html', 'css']
    
    # Self-hosted keywords
    selfhost_keywords = ['self-hosted', 'selfhosted', 'docker', 'container', 'homelab',
                        'server', 'local-first', 'offline', 'privacy']
    
    # Finance keywords
    finance_keywords = ['finance', 'trading', 'stock', 'crypto', 'bitcoin', 'wallet',
                       'budget', 'payment', 'banking', 'money', 'fintech']
    
    # Productivity keywords
    prod_keywords = ['productivity', 'note', 'task', 'todo', 'calendar', 'schedule',
                    'organize', 'project-management', 'workflow', 'automation']
    
    # Security keywords
    security_keywords = ['security', 'vulnerability', 'hack', 'exploit', 'penetration',
                        'audit', 'scan', 'malware', 'antivirus']
    
    all_text = desc + ' ' + ' '.join(topics) + ' ' + name
    
    if any(k in all_text for k in ai_keywords):
        return '🤖 AI & Machine Learning'
    elif any(k in all_text for k in finance_keywords):
        return '💰 Finance & Trading'
    elif any(k in all_text for k in security_keywords):
        return '🔒 Security & Hacking'
    elif any(k in all_text for k in dev_keywords):
        return '🛠️ Developer Tools'
    elif any(k in all_text for k in web_keywords):
        return '🌐 Web Development'
    elif any(k in all_text for k in selfhost_keywords):
        return '🏠 Self-Hosted & Local'
    elif any(k in all_text for k in prod_keywords):
        return '📋 Productivity'
    elif lang in ['rust', 'go', 'c', 'c++', 'zig']:
        return '⚙️ Systems & Low-Level'
    else:
        return '📦 Other'

def generate_markdown(repos_info):
    """Generate categorized markdown"""
    # Group by category
    categories = {}
    for info in repos_info:
        cat = categorize_repo(info)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(info)
    
    # Sort categories
    sorted_cats = sorted(categories.keys())
    
    # Count stats
    total = len(repos_info)
    popular = sum(1 for r in repos_info if r['stars'] > 100)
    very_popular = sum(1 for r in repos_info if r['stars'] > 1000)
    
    # Generate markdown
    md = f"""# 🔥 Trending GitHub Repositories (Apr-Jun 2026)

> Curated collection of trending repositories from various sources.
> Auto-generated descriptions from GitHub API.

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Repos | {total} |
| Categories | {len(categories)} |
| Stars > 1k | {very_popular} |
| Stars > 100 | {popular} |

---

"""
    
    for cat in sorted_cats:
        repos = sorted(categories[cat], key=lambda x: x['stars'], reverse=True)
        md += f"## {cat} ({len(repos)})\n\n"
        
        for info in repos:
            stars = info['stars']
            lang = info['language']
            desc = info['description'] or 'No description'
            
            # Truncate long descriptions
            if len(desc) > 100:
                desc = desc[:97] + '...'
            
            # Format stars
            if stars >= 1000:
                star_str = f"⭐ {stars/1000:.1f}k"
            elif stars > 0:
                star_str = f"⭐ {stars}"
            else:
                star_str = ""
            
            # Build line
            md += f"- **[{info['name']}]({info['url']})**"
            if star_str:
                md += f" {star_str}"
            if lang and lang != 'n/a':
                md += f" `{lang}`"
            md += f" - {desc}\n"
        
        md += "\n"
    
    md += """---

## 🔗 Categories

| Emoji | Category |
|-------|----------|
| 🤖 | AI & Machine Learning |
| 💰 | Finance & Trading |
| 🔒 | Security & Hacking |
| 🛠️ | Developer Tools |
| 🌐 | Web Development |
| 🏠 | Self-Hosted & Local |
| 📋 | Productivity |
| ⚙️ | Systems & Low-Level |
| 📦 | Other |

---

> **Last updated:** June 2026
"""
    
    return md

def main():
    filepath = 'News/TrendingGithubRepos/consolidated.md'
    
    # Get GitHub token
    token = get_github_token()
    if token:
        print("✅ Using GitHub token for authentication")
    else:
        print("⚠️ No GitHub token found. Rate limit: 60 requests/hour")
        print("   Set GITHUB_TOKEN env var or create ~/.github_token file")
    
    print("\n📥 Extracting repositories...")
    repos = extract_repos(filepath)
    print(f"   Found {len(repos)} unique repos")
    
    # Check rate limit
    print(f"\n🔍 Fetching repo info from GitHub API...")
    repos_info = []
    for i, repo in enumerate(repos, 1):
        print(f"   [{i}/{len(repos)}] {repo}                    ", end='\r')
        info = fetch_repo_info(repo, token)
        repos_info.append(info)
        if i % 30 == 0:
            time.sleep(2)  # Rate limiting every 30 requests
    
    print(f"\n   Fetched info for {len(repos_info)} repos")
    
    print("\n📝 Generating markdown...")
    markdown = generate_markdown(repos_info)
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"\n✅ Done! Updated {filepath}")
    
    # Print summary
    categories = {}
    for info in repos_info:
        cat = categorize_repo(info)
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Category breakdown:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}")
    
    # Top repos
    top = sorted(repos_info, key=lambda x: x['stars'], reverse=True)[:10]
    print("\n⭐ Top 10 by stars:")
    for info in top:
        print(f"   {info['stars']:>6} - {info['name']}")

if __name__ == '__main__':
    main()
