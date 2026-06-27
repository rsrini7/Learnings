#!/usr/bin/env python3
"""
GitHub Repository Manager & Link Checker
All-in-one tool for managing trending repos and fixing markdown links.
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
from pathlib import Path


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_FILE = 'News/TrendingGithubRepos/consolidated.md'
GITHUB_API = 'https://api.github.com'
REPOS_DIR = 'News/TrendingGithubRepos'


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
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'}
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
    
    ai_kw = ['ai', 'llm', 'gpt', 'claude', 'agent', 'machine-learning', 'deep-learning', 
             'neural', 'transformer', 'rag', 'embedding', 'fine-tune', 'inference',
             'openai', 'anthropic', 'model', 'prompt', 'copilot']
    dev_kw = ['cli', 'terminal', 'ide', 'editor', 'code', 'developer', 'programming',
              'debug', 'lint', 'format', 'build', 'compile', 'git', 'github', 'dev']
    web_kw = ['web', 'frontend', 'backend', 'api', 'http', 'rest', 'graphql', 'react',
              'vue', 'angular', 'nextjs', 'node', 'browser', 'html', 'css']
    host_kw = ['self-hosted', 'selfhosted', 'docker', 'container', 'homelab',
               'server', 'local-first', 'offline', 'privacy']
    fin_kw = ['finance', 'trading', 'stock', 'crypto', 'bitcoin', 'wallet',
              'budget', 'payment', 'banking', 'money', 'fintech']
    prod_kw = ['productivity', 'note', 'task', 'todo', 'calendar', 'schedule',
               'organize', 'project-management', 'workflow', 'automation']
    sec_kw = ['security', 'vulnerability', 'hack', 'exploit', 'penetration',
              'audit', 'scan', 'malware', 'antivirus']
    
    all_text = desc + ' ' + ' '.join(topics) + ' ' + name
    
    if any(k in all_text for k in ai_kw): return '🤖 AI & Machine Learning'
    if any(k in all_text for k in fin_kw): return '💰 Finance & Trading'
    if any(k in all_text for k in sec_kw): return '🔒 Security & Hacking'
    if any(k in all_text for k in dev_kw): return '🛠️ Developer Tools'
    if any(k in all_text for k in web_kw): return '🌐 Web Development'
    if any(k in all_text for k in host_kw): return '🏠 Self-Hosted & Local'
    if any(k in all_text for k in prod_kw): return '📋 Productivity'
    if lang in ['rust', 'go', 'c', 'c++', 'zig']: return '⚙️ Systems & Low-Level'
    return '📦 Other'


def create_slug(name):
    """Convert category name to folder slug"""
    slug = re.sub(r'[^\w\s-]', '', name).strip()
    return re.sub(r'[\s]+', '-', slug).lower()


# =============================================================================
# GitHub API Functions
# =============================================================================

def search_repo_by_name(repo_name, token=None):
    """Search GitHub for a repo by name"""
    query = urllib.parse.quote(repo_name)
    url = f"{GITHUB_API}/search/repositories?q={query}+in:name&sort=stars&order=desc&per_page=5"
    data, _ = api_request(url, token)
    if not data or 'items' not in data or not data['items']:
        return None
    for item in data['items']:
        if item.get('name', '').lower() == repo_name.lower():
            return item['full_name']
    return data['items'][0]['full_name']


def recover_404_repo(repo_path, token=None):
    """Try to recover a 404 repo"""
    repo_name = repo_path.split('/')[-1]
    found = search_repo_by_name(repo_name, token)
    if found and found.lower() != repo_path.lower():
        return found
    return None


def build_repo_info_stub(repo_path, status_label='deleted'):
    """Build stub for unrecoverable repo"""
    return {
        'name': repo_path.split('/')[-1],
        'full_name': repo_path,
        'description': f'Repo not found (404) — {status_label}',
        'stars': 0, 'language': 'N/A', 'topics': [],
        'url': f"https://github.com/{repo_path}",
        'archived': False, 'fork': False,
        'status': '404', 'original_path': repo_path,
    }


def fetch_repo_info(repo_path, token=None, recover=True):
    """Fetch repo info from GitHub API with optional 404 recovery"""
    url = f"{GITHUB_API}/repos/{repo_path}"
    data, _ = api_request(url, token)
    
    if data and 'id' in data:
        return {
            'name': data.get('name', repo_path.split('/')[-1]),
            'full_name': data.get('full_name', repo_path),
            'description': data.get('description', 'No description available'),
            'stars': data.get('stargazers_count', 0),
            'language': data.get('language', 'N/A'),
            'topics': data.get('topics', []),
            'url': data.get('html_url', f"https://github.com/{repo_path}"),
            'archived': data.get('archived', False), 'fork': data.get('fork', False),
            'status': 'ok', 'original_path': repo_path,
        }
    
    if not recover:
        return build_repo_info_stub(repo_path, 'deleted/private')
    
    replacement = recover_404_repo(repo_path, token)
    if replacement is None:
        return build_repo_info_stub(repo_path, 'deleted/private')
    
    rep_data, _ = api_request(f"{GITHUB_API}/repos/{replacement}", token)
    if rep_data and 'id' in rep_data:
        return {
            'name': rep_data.get('name', replacement.split('/')[-1]),
            'full_name': rep_data.get('full_name', replacement),
            'description': rep_data.get('description', 'No description available'),
            'stars': rep_data.get('stargazers_count', 0),
            'language': rep_data.get('language', 'N/A'),
            'topics': rep_data.get('topics', []),
            'url': rep_data.get('html_url', f"https://github.com/{replacement}"),
            'archived': rep_data.get('archived', False), 'fork': rep_data.get('fork', False),
            'status': 'recovered', 'original_path': repo_path,
            'recovered_from': replacement,
        }
    return build_repo_info_stub(repo_path, 'deleted/private')


def fetch_readme_description(repo_path, token=None):
    """Fetch first meaningful paragraph from README"""
    data, _ = api_request(f"{GITHUB_API}/repos/{repo_path}/readme", token)
    if not data or 'content' not in data:
        return None
    content = base64.b64decode(data.get('content', '')).decode('utf-8', errors='ignore')
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith(('![', '[![', '#')):
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
    """Fetch info for all repos in file"""
    repos = extract_repos(filepath)
    print(f"📥 Found {len(repos)} unique repos\n")
    
    repos_info = []
    recovered = 0
    failed = 0
    
    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}] {repo:<60}", end='\r')
        info = fetch_repo_info(repo, token, recover=recover)
        
        if info['status'] == 'recovered': recovered += 1
        elif info['status'] == '404': failed += 1
        
        effective = info.get('recovered_from', repo) if info['status'] in ('ok', 'recovered') else None
        if effective and info['status'] in ('ok', 'recovered'):
            if not info['description'] or info['description'] == 'No description available':
                readme = fetch_readme_description(effective, token)
                if readme: info['description'] = readme
        
        repos_info.append(info)
        if i % 30 == 0: time.sleep(1)
    
    print(f"\n✅ Fetched {len(repos_info)} repos  |  🔁 Recovered: {recovered}  |  ❌ Dead: {failed}")
    return repos_info


# =============================================================================
# Markdown Generation
# =============================================================================

def generate_markdown(repos_info, include_404=True):
    """Generate categorized markdown"""
    categories = {}
    for info in repos_info:
        if not include_404 and info['status'] == '404':
            continue
        cat = categorize_repo(info)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(info)
    
    total = len(repos_info)
    active = sum(1 for r in repos_info if r['status'] in ('ok', 'recovered'))
    recovered = sum(1 for r in repos_info if r['status'] == 'recovered')
    dead = sum(1 for r in repos_info if r['status'] == '404')
    
    md = f"""# 🔥 Trending GitHub Repositories (Apr-Jun 2026)

> Curated collection of trending repositories from various sources.

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Repos | {total} |
| Active | {active} |
| Recovered | {recovered} |
| Dead (404) | {dead} |
| Categories | {len(categories)} |

---

"""
    
    for cat in sorted(categories.keys()):
        repos = sorted(categories[cat], key=lambda x: x['stars'], reverse=True)
        md += f"## {cat} ({len(repos)})\n\n"
        for info in repos:
            desc = (info['description'] or 'No description')[:100]
            star = format_stars(info['stars'])
            lang = f" `{info['language']}`" if info['language'] != 'N/A' else ''
            note = f" *(was: `{info.get('original_path', '')}`)*" if info.get('status') == 'recovered' else ''
            md += f"- **[{info['name']}]({info['url']})** {star}{lang} - {desc}{note}\n"
        md += "\n"
    
    md += f"\n---\n\n> **Last updated:** {datetime.now().strftime('%B %Y')}\n"
    return md


def generate_category_md(cat_name, repos):
    """Generate markdown for a category"""
    return f"""# {cat_name}

> Trending GitHub repositories in this category.
> Auto-generated on {datetime.now().strftime('%B %d, %Y')}

---

## Repositories ({len(repos)})

""" + '\n'.join(repos) + f"""

---

> **Last updated:** {datetime.now().strftime('%B %Y')}
"""


def generate_index_md(categories, active_repos):
    """Generate index.md for split structure"""
    md = f"""# 🔥 Trending GitHub Repositories (Apr-Jun 2026)

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
    for cat, repos in sorted(categories.items(), key=lambda x: -len(x[1])):
        slug = create_slug(cat)
        md += f"| {cat} | {len(repos)} | [{slug}](./{slug}/index.md) |\n"
    
    md += "\n---\n\n## 🔗 Quick Links\n\n"
    for cat, repos in sorted(categories.items(), key=lambda x: -len(x[1])):
        slug = create_slug(cat)
        md += f"- [{cat}](./{slug}/index.md) ({len(repos)} repos)\n"
    
    md += f"\n---\n\n> **Last updated:** {datetime.now().strftime('%B %Y')}\n"
    return md


def parse_consolidated(filepath):
    """Parse consolidated.md and extract repos by category"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    categories = {}
    current_cat = None
    for line in content.split('\n'):
        cat_match = re.match(r'^## (.+?) \((\d+)\)$', line)
        if cat_match:
            current_cat = cat_match.group(1)
            categories[current_cat] = []
            continue
        if current_cat and line.startswith('- **['):
            if 'Repo not found (404)' not in line:
                categories[current_cat].append(line)
    return categories


def list_404_repos(filepath):
    """List all repos marked as 404"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r'\*\*\[([^\]]+)\]\(https://github\.com/([^)]+)\)\*\*.*?Repo not found \(404\)'
    return re.findall(pattern, content)


# =============================================================================
# Link Checker Functions
# =============================================================================

def find_md_files(directory):
    """Find all markdown files in directory"""
    md_files = []
    for root, dirs, files in os.walk(directory):
        if '.git' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    return sorted(md_files)


def extract_links(content, filepath):
    """Extract all links from markdown content"""
    links = []
    pattern = r'!?\[([^\]]*)\]\(<?([^)>\s]+)>?\)'
    for match in re.finditer(pattern, content):
        url = match.group(2)
        if url.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        url = url.split('#')[0]
        if url:
            links.append({
                'text': match.group(1), 'url': url,
                'line': content[:match.start()].count('\n') + 1,
                'match': match.group(0)
            })
    return links


def resolve_path(link_url, source_file):
    """Resolve relative path from source file"""
    source_dir = os.path.dirname(source_file)
    decoded = urllib.parse.unquote(link_url)
    if decoded.startswith('/'):
        return os.path.normpath('.' + decoded)
    return os.path.normpath(os.path.join(source_dir, decoded))


def find_asset(filename, search_dirs=None):
    """Search for an asset file"""
    if search_dirs is None:
        search_dirs = ['AI-ML/assets', 'Papers/assets', 'Blockchain/assets', 'News/assets', 'assets']
    
    for d in search_dirs:
        if os.path.exists(d):
            for root, _, files in os.walk(d):
                if filename in files:
                    return os.path.join(root, filename)
    
    for root, _, files in os.walk('.'):
        if '.git' in root:
            continue
        if filename in files:
            return os.path.join(root, filename)
    return None


def fix_link(link_url, source_file):
    """Try to fix a broken link"""
    source_dir = os.path.dirname(source_file)
    filename = os.path.basename(urllib.parse.unquote(link_url))
    found = find_asset(filename)
    if found:
        return os.path.relpath(found, source_dir)
    return None


# =============================================================================
# CLI Commands
# =============================================================================

def cmd_fetch(filepath, token, recover=True):
    """Fetch all repos and update consolidated file"""
    print(f"🔍 Fetching repository info (recovery={'on' if recover else 'off'})...\n")
    repos_info = fetch_all_repos(filepath, token, recover=recover)
    
    print("\n📝 Generating markdown...")
    markdown = generate_markdown(repos_info, include_404=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"\n✅ Updated {filepath}")


def cmd_split(filepath):
    """Split consolidated.md into category subfolders"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("   Run 'fetch' first to create consolidated.md")
        return
    
    print("📥 Parsing consolidated.md...")
    categories = parse_consolidated(filepath)
    total_repos = sum(len(r) for r in categories.values())
    print(f"   Found {len(categories)} categories with {total_repos} active repos\n")
    
    print("📁 Creating category folders...")
    for cat_name, repos in categories.items():
        if not repos:
            continue
        slug = create_slug(cat_name)
        cat_dir = os.path.join(REPOS_DIR, slug)
        os.makedirs(cat_dir, exist_ok=True)
        
        with open(os.path.join(cat_dir, 'index.md'), 'w', encoding='utf-8') as f:
            f.write(generate_category_md(cat_name, repos))
        print(f"   ✅ {slug}/index.md ({len(repos)} repos)")
    
    print("\n📝 Generating index.md...")
    with open(os.path.join(REPOS_DIR, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(generate_index_md(categories, total_repos))
    print(f"   ✅ index.md")
    
    print(f"\n✅ Done! Split into {len(categories)} category folders")
    print(f"⚠️  You can now delete consolidated.md if everything looks good.")


def cmd_recover(filepath, token):
    """Scan for 404 repos and attempt recovery"""
    repos_404 = list_404_repos(filepath)
    print(f"🔁 Attempting recovery for {len(repos_404)} 404 repos...\n")
    
    results = {'recovered': [], 'gone': [], 'unknown': []}
    for i, (name, repo_path) in enumerate(repos_404, 1):
        print(f"[{i}/{len(repos_404)}] {repo_path:<55}", end='\r')
        replacement = recover_404_repo(repo_path, token)
        
        if replacement is None:
            results['gone'].append(repo_path)
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
    print(f"\n💀 Gone ({len(results['gone'])}):")
    for r in results['gone']: print(f"   {r}")
    print(f"\n❓ Unknown ({len(results['unknown'])}):")
    for r in results['unknown']: print(f"   {r}")


def cmd_list404(filepath):
    """List all 404 repos"""
    repos_404 = list_404_repos(filepath)
    print(f"📋 Found {len(repos_404)} repos marked as 404:\n")
    for _, repo_path in repos_404:
        print(f"   {repo_path}")


def cmd_check(filepath, token):
    """Check specific repo"""
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
        print(f"   ⚡ Recovered: {info.get('original_path')} → {info.get('recovered_from')}")


def cmd_stats():
    """Show statistics"""
    # Check split structure
    index_file = os.path.join(REPOS_DIR, 'index.md')
    if os.path.exists(index_file):
        total = 0
        cats = 0
        for entry in os.listdir(REPOS_DIR):
            cat_dir = os.path.join(REPOS_DIR, entry)
            if os.path.isdir(cat_dir):
                cat_index = os.path.join(cat_dir, 'index.md')
                if os.path.exists(cat_index):
                    with open(cat_index, 'r', encoding='utf-8') as f:
                        repos = len(re.findall(r'^- \*\*\[', f.read(), re.MULTILINE))
                    total += repos
                    cats += 1
        print(f"📊 Statistics ({REPOS_DIR}/):\n")
        print(f"   Total repos: {total}")
        print(f"   Categories:  {cats}")
    else:
        print(f"❌ No data found. Run 'fetch' and 'split' first.")


def cmd_links(directory='.', fix=False):
    """Check and optionally fix broken links in markdown files"""
    mode = "FIX" if fix else "CHECK"
    print(f"{'🔧' if fix else '🔍'} {mode} MODE")
    print(f"Scanning: {os.path.abspath(directory)}")
    print("=" * 60)
    
    md_files = find_md_files(directory)
    print(f"Found {len(md_files)} markdown files\n")
    
    total_links = 0
    valid_links = 0
    broken_links = []
    fixed_count = 0
    fixed_files = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            continue
        
        file_fixes = 0
        new_content = content
        file_broken = []
        
        for link in extract_links(content, md_file):
            total_links += 1
            resolved = resolve_path(link['url'], md_file)
            
            if os.path.exists(resolved):
                valid_links += 1
                continue
            
            # Broken link found
            file_broken.append({
                'source': md_file, 'line': link['line'],
                'match': link['match'], 'resolved': resolved
            })
            
            # Try to fix
            if fix:
                fixed = fix_link(link['url'], md_file)
                if fixed:
                    anchor = '#' + link['url'].split('#', 1)[1] if '#' in link['url'] else ''
                    encoded = urllib.parse.quote(fixed, safe='/')
                    
                    # Reconstruct link
                    old_match = link['match']
                    if old_match.startswith('!['):
                        prefix = old_match[:old_match.index('](') + 2]
                    else:
                        prefix = old_match[:old_match.index('](') + 2]
                    
                    if '<' in old_match and '>' in old_match:
                        new_link = f"{prefix}<{encoded}{anchor}>"
                    else:
                        new_link = f"{prefix}{encoded}{anchor})"
                    
                    new_content = new_content.replace(old_match, new_link)
                    file_fixes += 1
        
        broken_links.extend(file_broken)
        
        if file_fixes > 0 and fix:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed_files.append((md_file, file_fixes))
            fixed_count += file_fixes
    
    # Print broken links (only in check mode or if some couldn't be fixed)
    if not fix and broken_links:
        print("❌ Broken links found:\n")
        by_file = {}
        for bl in broken_links:
            by_file.setdefault(bl['source'], []).append(bl)
        for source, links in sorted(by_file.items()):
            print(f"📄 {source}")
            for l in links:
                print(f"   Line {l['line']}: {l['match']}")
                print(f"          → {l['resolved']}")
            print()
    
    # Print fixed files
    if fix and fixed_files:
        print("📝 Files fixed:\n")
        for f, n in sorted(fixed_files):
            print(f"   {f}: {n} links")
        print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Summary")
    print(f"   Files scanned: {len(md_files)}")
    print(f"   Links checked: {total_links}")
    print(f"   Valid:         {valid_links}")
    print(f"   Broken:        {len(broken_links)}")
    
    if fix:
        still_broken = len(broken_links) - fixed_count
        print(f"   Fixed:         {fixed_count}")
        if still_broken > 0:
            print(f"   Still broken:  {still_broken}")
        print(f"\n✅ Fixed {fixed_count} broken links!")
    else:
        if broken_links:
            print(f"\n⚠️  Run with 'links --fix' to auto-fix")
        else:
            print(f"\n✅ All links valid!")


def cmd_help():
    """Show help"""
    print("""
🔧 GitHub Repository Manager & Link Checker

Usage: python3 github-repos.py <command> [options]

Repository Commands:
  fetch        Fetch all repos and update consolidated.md
  split        Split consolidated.md into category folders
  recover      Scan for 404 repos and attempt recovery
  list404      List all repos marked as 404
  check        Check a specific repo (e.g., check owner/repo)
  stats        Show statistics

Link Commands:
  links        Check broken links (add --fix to auto-fix)

Options:
  --file       Specify consolidated.md path
  --no-recover Disable 404 recovery (for fetch)
  --fix        Auto-fix broken links (for links)

Environment:
  GITHUB_TOKEN GitHub API token

Examples:
  python3 github-repos.py fetch
  python3 github-repos.py split
  python3 github-repos.py links           # check only
  python3 github-repos.py links --fix     # check and fix
  python3 github-repos.py check apple/coreai-models
""")


# =============================================================================
# Main
# =============================================================================

def main():
    args = sys.argv[1:]
    
    filepath = DEFAULT_FILE
    if '--file' in args:
        idx = args.index('--file')
        if idx + 1 < len(args):
            filepath = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    recover = '--no-recover' not in args
    if '--no-recover' in args:
        args.remove('--no-recover')
    
    command = args[0] if args else 'help'
    
    token = get_github_token()
    if command in ['fetch', 'recover', 'check']:
        if token:
            print(f"✅ Using GitHub token\n")
        else:
            print(f"⚠️ No token found. Rate limit: 60 req/hour\n")
    
    if command == 'fetch':
        cmd_fetch(filepath, token, recover=recover)
    elif command == 'split':
        cmd_split(filepath)
    elif command == 'recover':
        cmd_recover(filepath, token)
    elif command == 'list404':
        cmd_list404(filepath)
    elif command == 'check':
        cmd_check(filepath, token)
    elif command == 'stats':
        cmd_stats()
    elif command == 'links':
        directory = '.'
        for a in args[1:]:
            if not a.startswith('--'):
                directory = a
        cmd_links(directory, fix='--fix' in args)
    elif command == 'help':
        cmd_help()
    else:
        print(f"❌ Unknown command: {command}")
        cmd_help()


if __name__ == '__main__':
    main()
