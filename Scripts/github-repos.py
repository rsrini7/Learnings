#!/usr/bin/env python3
"""
GitHub Repository Manager
Combined tool for fetching, updating, and managing trending repos.
Includes 404 recovery via GitHub Search API.
"""

import re
import os
import sys
import json
import time
import base64
import urllib.request
import urllib.parse
from urllib.error import URLError
from datetime import datetime


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_FILE = 'News/TrendingGithubRepos/consolidated.md'
GITHUB_API = 'https://api.github.com'


# =============================================================================
# Helper Functions
# =============================================================================

def get_github_token():
    """Get GitHub token from environment or file"""
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token
    
    token_file = os.path.expanduser('~/.github_token')
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read().strip()
    
    return None


def api_request(url, token=None):
    """Make GitHub API request; returns (data, status_code)"""
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        headers['Authorization'] = f'token {token}'
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode()), response.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except URLError:
        return None, None


def extract_repos(filepath):
    """Extract GitHub repo URLs from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'https://github\.com/([a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+)'
    matches = re.findall(pattern, content)
    
    seen = set()
    repos = []
    for repo in matches:
        repo = repo.rstrip('/')
        if '.' in repo.split('/')[-1] and not repo.endswith('.git'):
            continue
        if repo not in seen and '/' in repo and len(repo.split('/')[1]) > 0:
            seen.add(repo)
            repos.append(repo)
    
    return repos


def format_stars(stars):
    """Format star count"""
    if stars >= 1000:
        return f"⭐ {stars/1000:.1f}k"
    elif stars > 0:
        return f"⭐ {stars}"
    return ""


def categorize_repo(info):
    """Categorize repo based on description and topics"""
    desc = (info.get('description', '') or '').lower()
    topics = [t.lower() for t in info.get('topics', [])]
    lang = (info.get('language', '') or '').lower()
    name = info.get('name', '').lower()
    
    ai_keywords = ['ai', 'llm', 'gpt', 'claude', 'agent', 'machine-learning', 'deep-learning', 
                   'neural', 'transformer', 'rag', 'embedding', 'fine-tune', 'inference',
                   'openai', 'anthropic', 'model', 'prompt', 'copilot']
    
    dev_keywords = ['cli', 'terminal', 'ide', 'editor', 'code', 'developer', 'programming',
                    'debug', 'lint', 'format', 'build', 'compile', 'git', 'github', 'dev']
    
    web_keywords = ['web', 'frontend', 'backend', 'api', 'http', 'rest', 'graphql', 'react',
                    'vue', 'angular', 'nextjs', 'node', 'browser', 'html', 'css']
    
    selfhost_keywords = ['self-hosted', 'selfhosted', 'docker', 'container', 'homelab',
                        'server', 'local-first', 'offline', 'privacy']
    
    finance_keywords = ['finance', 'trading', 'stock', 'crypto', 'bitcoin', 'wallet',
                       'budget', 'payment', 'banking', 'money', 'fintech']
    
    prod_keywords = ['productivity', 'note', 'task', 'todo', 'calendar', 'schedule',
                    'organize', 'project-management', 'workflow', 'automation']
    
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


# =============================================================================
# 404 Recovery Functions
# =============================================================================

def search_repo_by_name(repo_name, token=None):
    """
    Search GitHub for a repo by name when the original owner/path is 404.
    Returns best-match full_name or None.
    """
    query = urllib.parse.quote(repo_name)
    url = f"{GITHUB_API}/search/repositories?q={query}+in:name&sort=stars&order=desc&per_page=5"
    data, status = api_request(url, token)
    
    if not data or 'items' not in data or not data['items']:
        return None
    
    # Prefer exact name match
    for item in data['items']:
        if item.get('name', '').lower() == repo_name.lower():
            return item['full_name']
    
    # Fall back to first result
    return data['items'][0]['full_name']


def recover_404_repo(repo_path, token=None):
    """
    Try to recover a 404 repo by searching GitHub API.
    Returns replacement full_name string, or None if unrecoverable.
    """
    repo_name = repo_path.split('/')[-1]
    found = search_repo_by_name(repo_name, token)
    
    # Only return if it's a different repo (not the same 404 one)
    if found and found.lower() != repo_path.lower():
        return found
    
    return None


def build_repo_info_stub(repo_path, status_label='deleted'):
    """Build a minimal stub for an unrecoverable repo"""
    return {
        'name': repo_path.split('/')[-1],
        'full_name': repo_path,
        'description': f'Repo not found (404) — {status_label}',
        'stars': 0,
        'language': 'N/A',
        'topics': [],
        'url': f"https://github.com/{repo_path}",
        'archived': False,
        'fork': False,
        'status': '404',
        'original_path': repo_path,
    }


# =============================================================================
# Core Functions
# =============================================================================

def fetch_repo_info(repo_path, token=None, recover=True):
    """
    Fetch repo info from GitHub API.
    If 404 and recover=True, attempt automatic recovery via GitHub Search API.
    """
    url = f"{GITHUB_API}/repos/{repo_path}"
    data, status = api_request(url, token)
    
    if data and 'id' in data:
        return {
            'name': data.get('name', repo_path.split('/')[-1]),
            'full_name': data.get('full_name', repo_path),
            'description': data.get('description', 'No description available'),
            'stars': data.get('stargazers_count', 0),
            'language': data.get('language', 'N/A'),
            'topics': data.get('topics', []),
            'url': data.get('html_url', f"https://github.com/{repo_path}"),
            'archived': data.get('archived', False),
            'fork': data.get('fork', False),
            'status': 'ok',
            'original_path': repo_path,
        }
    
    # --- 404 path ---
    if not recover:
        return build_repo_info_stub(repo_path, 'deleted/private')
    
    replacement = recover_404_repo(repo_path, token)
    if replacement is None:
        return build_repo_info_stub(repo_path, 'deleted/private')
    
    # Fetch the replacement
    rep_url = f"{GITHUB_API}/repos/{replacement}"
    rep_data, rep_status = api_request(rep_url, token)
    
    if rep_data and 'id' in rep_data:
        info = {
            'name': rep_data.get('name', replacement.split('/')[-1]),
            'full_name': rep_data.get('full_name', replacement),
            'description': rep_data.get('description', 'No description available'),
            'stars': rep_data.get('stargazers_count', 0),
            'language': rep_data.get('language', 'N/A'),
            'topics': rep_data.get('topics', []),
            'url': rep_data.get('html_url', f"https://github.com/{replacement}"),
            'archived': rep_data.get('archived', False),
            'fork': rep_data.get('fork', False),
            'status': 'recovered',
            'original_path': repo_path,
            'recovered_from': replacement,
        }
        return info
    
    # Replacement also 404'd
    return build_repo_info_stub(repo_path, 'deleted/private')


def fetch_readme_description(repo_path, token=None):
    """Fetch first meaningful paragraph from README"""
    url = f"{GITHUB_API}/repos/{repo_path}/readme"
    data, _ = api_request(url, token)
    
    if not data or 'content' not in data:
        return None
    
    content = base64.b64decode(data.get('content', '')).decode('utf-8', errors='ignore')
    
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('![') or line.startswith('[![') or line.startswith('#'):
            continue
        if 'badge' in line.lower() or 'shield' in line.lower() or 'img.shields.io' in line:
            continue
        
        line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
        line = re.sub(r'[*_`]', '', line).strip()
        
        if len(line) > 150:
            line = line[:147] + '...'
        
        return line if line else None
    
    return None


def fetch_all_repos(filepath, token=None, recover=True):
    """Fetch info for all repos in file, with optional 404 recovery"""
    repos = extract_repos(filepath)
    print(f"📥 Found {len(repos)} unique repos\n")
    
    repos_info = []
    recovered = 0
    failed = 0
    
    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}] {repo:<60}", end='\r')
        
        info = fetch_repo_info(repo, token, recover=recover)
        
        if info['status'] == 'recovered':
            recovered += 1
        elif info['status'] == '404':
            failed += 1
        
        # Enrich description from README if missing
        effective_path = info.get('recovered_from', repo) if info['status'] in ('ok', 'recovered') else None
        if effective_path and info['status'] in ('ok', 'recovered'):
            if not info['description'] or info['description'] == 'No description available':
                readme_desc = fetch_readme_description(effective_path, token)
                if readme_desc:
                    info['description'] = readme_desc
        
        repos_info.append(info)
        
        if i % 30 == 0:
            time.sleep(1)
    
    print(f"\n✅ Fetched {len(repos_info)} repos  |  🔁 Recovered: {recovered}  |  ❌ Dead: {failed}")
    return repos_info


def generate_markdown(repos_info):
    """Generate categorized markdown"""
    categories = {}
    for info in repos_info:
        cat = categorize_repo(info)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(info)
    
    sorted_cats = sorted(categories.keys())
    
    total = len(repos_info)
    active = sum(1 for r in repos_info if r['status'] in ('ok', 'recovered'))
    recovered = sum(1 for r in repos_info if r['status'] == 'recovered')
    dead = sum(1 for r in repos_info if r['status'] == '404')
    popular = sum(1 for r in repos_info if r['stars'] > 100)
    very_popular = sum(1 for r in repos_info if r['stars'] > 1000)
    
    md = f"""# 🔥 Trending GitHub Repositories (Apr-Jun 2026)

> Curated collection of trending repositories from various sources.
> Auto-generated descriptions from GitHub API. 404s auto-recovered where possible.

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Repos | {total} |
| Active Repos | {active} |
| 🔁 Recovered (renamed/moved) | {recovered} |
| ❌ Dead (deleted/private) | {dead} |
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
            
            if len(desc) > 100:
                desc = desc[:97] + '...'
            
            star_str = format_stars(stars)
            
            # Add recovery note if applicable
            recovered_note = ''
            if info.get('status') == 'recovered':
                orig = info.get('original_path', '')
                recovered_note = f' *(was: `{orig}`)*'
            
            md += f"- **[{info['name']}]({info['url']})**"
            if star_str:
                md += f" {star_str}"
            if lang and lang != 'N/A':
                md += f" `{lang}`"
            md += f" - {desc}{recovered_note}\n"
        
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

> **Last updated:** """ + datetime.now().strftime('%B %Y') + """
"""
    
    return md


def list_404_repos(filepath):
    """List all repos marked as 404"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'\*\*\[([^\]]+)\]\(https://github\.com/([^)]+)\)\*\*.*?Repo not found \(404\)'
    matches = re.findall(pattern, content)
    
    return [(name, repo) for name, repo in matches]


# =============================================================================
# CLI Commands
# =============================================================================

def cmd_fetch(filepath, token, recover=True):
    """Fetch all repos and update file"""
    print(f"🔍 Fetching repository info (recovery={'on' if recover else 'off'})...\n")
    repos_info = fetch_all_repos(filepath, token, recover=recover)
    
    print("\n📝 Generating markdown...")
    markdown = generate_markdown(repos_info)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"\n✅ Updated {filepath}")
    
    categories = {}
    for info in repos_info:
        cat = categorize_repo(info)
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Category breakdown:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}")
    
    top = sorted(repos_info, key=lambda x: x['stars'], reverse=True)[:10]
    print("\n⭐ Top 10 by stars:")
    for info in top:
        if info['stars'] > 0:
            print(f"   {format_stars(info['stars']):>8} - {info['name']}")


def cmd_recover(filepath, token):
    """
    Scan file for 404-marked repos and attempt recovery.
    Prints a recovery report without modifying the file.
    Run cmd_fetch to regenerate the file with recovered links.
    """
    repos_404 = list_404_repos(filepath)
    print(f"🔁 Attempting recovery for {len(repos_404)} 404 repos...\n")
    
    results = {'recovered': [], 'confirmed_gone': [], 'unknown': []}
    
    for i, (name, repo_path) in enumerate(repos_404, 1):
        print(f"[{i}/{len(repos_404)}] {repo_path:<55}", end='\r')
        replacement = recover_404_repo(repo_path, token)
        
        if replacement is None:
            results['confirmed_gone'].append(repo_path)
        else:
            info = fetch_repo_info(replacement, token, recover=False)
            if info['status'] == 'ok':
                results['recovered'].append((repo_path, replacement, info['stars']))
            else:
                results['unknown'].append(repo_path)
        
        time.sleep(0.3)
    
    print(f"\n\n{'='*60}")
    print(f"✅ Recovered ({len(results['recovered'])}):")
    for orig, repl, stars in sorted(results['recovered'], key=lambda x: -x[2]):
        print(f"   {orig:<45} → {repl}  {format_stars(stars)}")
    
    print(f"\n💀 Confirmed gone ({len(results['confirmed_gone'])}):")
    for r in results['confirmed_gone']:
        print(f"   {r}")
    
    print(f"\n❓ Unknown / needs manual check ({len(results['unknown'])}):")
    for r in results['unknown']:
        print(f"   {r}")
    
    print(f"\n{'='*60}")
    print(f"Re-run `fetch` to regenerate the file with recovered URLs.")


def cmd_list404(filepath):
    """List all 404 repos"""
    repos_404 = list_404_repos(filepath)
    
    print(f"📋 Found {len(repos_404)} repos marked as 404:\n")
    for name, repo_path in repos_404:
        print(f"   {repo_path}")
    
    print(f"\nTotal: {len(repos_404)} repos")


def cmd_check(filepath, token):
    """Check specific repo (with recovery attempt)"""
    args = sys.argv[1:]
    
    try:
        idx = args.index('check')
        repo = args[idx + 1]
    except (ValueError, IndexError):
        print("Usage: python3 github-repos.py check <owner/repo>")
        return
    
    print(f"🔍 Checking {repo}...")
    info = fetch_repo_info(repo, token, recover=True)
    
    print(f"\n📊 Results:")
    print(f"   Name:        {info['name']}")
    print(f"   Description: {info['description']}")
    print(f"   Stars:       {info['stars']}")
    print(f"   Language:    {info['language']}")
    print(f"   Status:      {info['status']}")
    
    if info.get('status') == 'recovered':
        print(f"   ⚡ Recovered from: {info.get('original_path')} → {info.get('recovered_from')}")
    
    if info['status'] == 'ok' and (not info['description'] or info['description'] == 'No description available'):
        print("\n📖 Trying README...")
        effective = info.get('recovered_from', repo)
        readme_desc = fetch_readme_description(effective, token)
        if readme_desc:
            print(f"   README: {readme_desc}")


def cmd_stats(filepath):
    """Show statistics"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    total = len(re.findall(r'^- \*\*\[', content, re.MULTILINE))
    repos_404 = len(re.findall('Repo not found \(404\)', content))
    active = total - repos_404
    recovered = len(re.findall('\*\(was:', content))
    
    cats = re.findall(r'^## .+ \((\d+)\)', content, re.MULTILINE)
    
    print(f"📊 Statistics for {filepath}:\n")
    print(f"   Total repos: {total}")
    print(f"   Active repos: {active}")
    print(f"   404 repos: {repos_404}")
    print(f"   Recovered repos: {recovered}")
    print(f"   Categories: {len(cats)}")


def cmd_help():
    """Show help"""
    print("""
🔧 GitHub Repository Manager

Usage: python3 github-repos.py <command> [options]

Commands:
  fetch      Fetch all repos and update file (with 404 recovery)
  recover    Scan for 404 repos and attempt recovery (dry run)
  list404    List all repos marked as 404
  check      Check a specific repo (e.g., check owner/repo)
  stats      Show statistics
  help       Show this help

Options:
  --file     Specify file path (default: News/TrendingGithubRepos/consolidated.md)
  --no-recover  Disable 404 recovery (for fetch command)

Environment:
  GITHUB_TOKEN    GitHub API token (or create ~/.github_token file)

Examples:
  python3 github-repos.py fetch
  python3 github-repos.py fetch --no-recover
  python3 github-repos.py recover
  python3 github-repos.py list404
  python3 github-repos.py check apple/coreai-models
  python3 github-repos.py stats
""")


# =============================================================================
# Main
# =============================================================================

def main():
    # Parse arguments
    args = sys.argv[1:]
    
    # Get file path
    filepath = DEFAULT_FILE
    if '--file' in args:
        idx = args.index('--file')
        if idx + 1 < len(args):
            filepath = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    # Check for --no-recover flag
    recover = '--no-recover' not in args
    if '--no-recover' in args:
        args.remove('--no-recover')
    
    # Get command
    command = args[0] if args else 'help'
    
    # Get token
    token = get_github_token()
    if token:
        print(f"✅ Using GitHub token\n")
    else:
        print(f"⚠️ No token found. Rate limit: 60 req/hour\n")
    
    # Execute command
    if command == 'fetch':
        cmd_fetch(filepath, token, recover=recover)
    elif command == 'recover':
        cmd_recover(filepath, token)
    elif command == 'list404':
        cmd_list404(filepath)
    elif command == 'check':
        cmd_check(filepath, token)
    elif command == 'stats':
        cmd_stats(filepath)
    elif command == 'help':
        cmd_help()
    else:
        print(f"❌ Unknown command: {command}")
        cmd_help()


if __name__ == '__main__':
    main()
