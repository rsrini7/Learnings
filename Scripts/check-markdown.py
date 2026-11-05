#!/usr/bin/env python3
"""
check-markdown.py - Repository Markdown, Mermaid, LaTeX & SVG Validator and Auto-Fixer.

Validates Markdown and referenced SVG assets for GitHub rendering edge cases:
1. LaTeX Display Math Indentation: Ensures '$$...$$' blocks are flush-left (column 0)
   so GitHub Flavored Markdown (GFM) does not treat them as inline list text and corrupt
   math subscripts into Markdown italics.
2. LaTeX Subscript Escaping: Prevents unescaped underscores inside '\\text{...}'
   which throw KaTeX syntax errors ('_' allowed only in math mode).
3. Mermaid Sequence Diagram Semicolons: Catches ';' in messages that act as statement terminators.
4. Mermaid Flowchart Edge Collisions: Catches double vertical bars '||' inside '|...|' edge labels.
5. Mermaid State Diagram Nested Colons: Catches internal colons in transition labels.
6. Mermaid State Diagram Bidirectional Overlaps: Catches parallel 'A <--> B' transitions that
   Dagre stacks at identical (x, y) coordinates.
7. SVG Text Boundary Overflow: Scans all referenced SVG architecture diagrams for text
   overflowing card containers, unescaped XML, or missing viewBox attributes.

Usage:
    python3 Scripts/check-markdown.py                  # Check all tracked markdown files & diagrams
    python3 Scripts/check-markdown.py path/to/file.md  # Check specific file(s)
    python3 Scripts/check-markdown.py --recent         # Check files in git working tree / recent commit
    python3 Scripts/check-markdown.py --fix [files]    # Automatically fix indented math & LaTeX underscores
"""

import argparse
import importlib.util
import os
import re
import subprocess
import sys

# Load SVG scanner from check-svg.py
_svg_scanner = None
try:
    _svg_script = os.path.join(os.path.dirname(__file__), 'check-svg.py')
    if os.path.isfile(_svg_script):
        spec = importlib.util.spec_from_file_location('check_svg', _svg_script)
        _mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mod)
        _svg_scanner = getattr(_mod, 'scan_svg_file', None)
except Exception:
    pass

# ANSI Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'


def get_all_tracked_md_files():
    """Retrieve all git-tracked markdown files."""
    try:
        out = subprocess.check_output(['git', 'ls-files', '*.md'], text=True)
        return [f for f in out.splitlines() if os.path.isfile(f)]
    except Exception:
        # Fallback to filesystem walk if git is unavailable
        md_files = []
        for root, dirs, files in os.walk('.'):
            if '.git' in dirs:
                dirs.remove('.git')
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.normpath(os.path.join(root, f)))
        return md_files


def get_recent_md_files():
    """Retrieve markdown files modified in working tree or recent commits."""
    files = set()
    try:
        # Working tree & staged changes
        status_out = subprocess.check_output(['git', 'status', '--porcelain'], text=True)
        for line in status_out.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2 and parts[-1].endswith('.md') and os.path.isfile(parts[-1]):
                files.add(parts[-1])
        # Last 5 commits
        diff_out = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD~5', 'HEAD'], text=True)
        for f in diff_out.splitlines():
            if f.endswith('.md') and os.path.isfile(f):
                files.add(f)
    except Exception:
        pass
    return sorted(list(files))


def scan_file(filepath):
    """Scan a single markdown file for Mermaid and LaTeX math rendering issues."""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    in_code_block = False
    in_mermaid = False
    mermaid_type = None
    mermaid_lines = []
    mermaid_start = 0

    for idx, line in enumerate(lines):
        stripped = line.strip()

        # Track code fences
        if stripped.startswith('```'):
            if not in_code_block:
                in_code_block = True
                if stripped.startswith('```mermaid'):
                    in_mermaid = True
                    mermaid_type = None
                    mermaid_lines = []
                    mermaid_start = idx + 1
            else:
                in_code_block = False
                if in_mermaid:
                    in_mermaid = False
                    # Analyze Mermaid block
                    if mermaid_type == 'sequenceDiagram':
                        for m_idx, m_line in enumerate(mermaid_lines):
                            if ('->>' in m_line or '-->>' in m_line) and ';' in m_line:
                                issues.append({
                                    'file': filepath,
                                    'line': mermaid_start + m_idx + 1,
                                    'type': 'Mermaid: Semicolon in sequenceDiagram message',
                                    'snippet': m_line.strip(),
                                    'fix_advice': 'Replace ";" with "and" or a comma to avoid statement termination.'
                                })
                    elif mermaid_type in ('flowchart', 'graph'):
                        for m_idx, m_line in enumerate(mermaid_lines):
                            if re.search(r'\|[^|]*\|\|[^|]*\|', m_line):
                                issues.append({
                                    'file': filepath,
                                    'line': mermaid_start + m_idx + 1,
                                    'type': 'Mermaid: Collision with || inside edge label',
                                    'snippet': m_line.strip(),
                                    'fix_advice': 'Enclose edge label in quotes: -->|"Score = ... ||v||"| or avoid ||.'
                                })
                    elif mermaid_type == 'stateDiagram-v2':
                        transitions = {}
                        for m_idx, m_line in enumerate(mermaid_lines):
                            if '-->' in m_line and ':' in m_line:
                                parts = m_line.split(':', 1)
                                if len(parts) > 1 and ':' in parts[1]:
                                    issues.append({
                                        'file': filepath,
                                        'line': mermaid_start + m_idx + 1,
                                        'type': 'Mermaid: Multiple colons in stateDiagram transition label',
                                        'snippet': m_line.strip(),
                                        'fix_advice': 'Remove nested colons (e.g., (:heal:)) to prevent transition lexer confusion.'
                                    })
                                arrow_part = parts[0].strip()
                                if '-->' in arrow_part:
                                    s1, s2 = [s.strip() for s in arrow_part.split('-->')]
                                    pair = tuple(sorted([s1, s2]))
                                    transitions[pair] = transitions.get(pair, 0) + 1
                        for pair, count in transitions.items():
                            if count > 1:
                                issues.append({
                                    'file': filepath,
                                    'line': mermaid_start,
                                    'type': f'Mermaid: Bidirectional overlap in stateDiagram ({pair[0]} <--> {pair[1]})',
                                    'snippet': f'{pair[0]} <--> {pair[1]}',
                                    'fix_advice': 'Prefer flowchart TD with a convergence/resume node to avoid Dagre label stacking.'
                                })
            continue

        if in_mermaid:
            if not mermaid_type:
                for t in ['sequenceDiagram', 'flowchart', 'graph', 'stateDiagram-v2', 'stateDiagram']:
                    if stripped.startswith(t):
                        mermaid_type = t
                        break
            mermaid_lines.append(line)
            continue

        if in_code_block:
            continue

        # Check 1: Indented $$ display math
        if re.match(r'^[ ]{1,}\$\$.*', line):
            issues.append({
                'file': filepath,
                'line': idx + 1,
                'type': 'LaTeX: Indented display math ($$ with leading spaces)',
                'snippet': line.strip(),
                'fix_advice': 'Place $$ flush-left (column 0) with blank lines before and after.'
            })

        # Check 2: Unescaped underscore inside \text{...}
        clean_line = re.sub(r'`[^`]*`', '', line)
        matches = re.findall(r'\\text\{([^{}]*)\}', clean_line)
        for m in matches:
            if '_' in m and '\\_' not in m:
                issues.append({
                    'file': filepath,
                    'line': idx + 1,
                    'type': 'LaTeX: Unescaped underscore in \\text{}',
                    'snippet': f'\\text{{{m}}}',
                    'fix_advice': f'Move subscript out of \\text{{}}: e.g. \\text{{Score}}_{{\\text{{{m.replace("_", "")}}}}} or escape as \\_'
                })

    # Check 3: Validate referenced SVG diagrams (XML well-formedness & text overflows)
    if _svg_scanner:
        md_dir = os.path.dirname(filepath)
        full_content = '\n'.join(lines)
        svg_matches = re.findall(r'!\[[^\]]*\]\(([^)]+\.svg)\)|<img [^>]*src=[\'"]([^"\']+\.svg)[\'"]', full_content)
        scanned_svgs = set()
        for m in svg_matches:
            svg_rel = m[0] or m[1]
            svg_rel = svg_rel.split('?')[0].split('#')[0]
            svg_path = os.path.normpath(os.path.join(md_dir, svg_rel))
            if svg_path not in scanned_svgs and os.path.isfile(svg_path):
                scanned_svgs.add(svg_path)
                svg_issues = _svg_scanner(svg_path)
                for s_iss in svg_issues:
                    if s_iss.get('severity') == 'CRITICAL':
                        issues.append({
                            'file': s_iss['file'],
                            'line': s_iss.get('line', 1),
                            'type': s_iss['type'],
                            'snippet': s_iss['snippet'],
                            'fix_advice': s_iss['fix_advice']
                        })

    return issues


def auto_fix_file(filepath):
    """Automatically fix common LaTeX indentation and text underscore issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    modified = False
    new_lines = []
    in_code_block = False

    for idx, line in enumerate(lines):
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block:
            new_lines.append(line)
            continue

        current_line = line

        # Fix 1: Un-indent display math blocks
        if re.match(r'^[ ]{1,}\$\$.*', current_line):
            # Ensure blank line before
            if new_lines and new_lines[-1].strip() != '':
                new_lines.append('')
            current_line = stripped
            modified = True

        # Fix 2: Unescaped underscore in \text{...}
        if '\\text{' in current_line:
            def repl_underscore(match):
                inner = match.group(1)
                if '_' in inner and '\\_' not in inner:
                    escaped = inner.replace('_', '\\_')
                    return f'\\text{{{escaped}}}'
                return match.group(0)

            fixed_line = re.sub(r'\\text\{([^{}]*)\}', repl_underscore, current_line)
            if fixed_line != current_line:
                current_line = fixed_line
                modified = True

        new_lines.append(current_line)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines) + '\n')
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate and fix Markdown files for GitHub LaTeX & Mermaid rendering."
    )
    parser.add_argument(
        'files', nargs='*', help='Specific markdown file(s) to check. Defaults to all tracked files.'
    )
    parser.add_argument(
        '--recent', action='store_true', help='Check only recently committed/modified markdown files.'
    )
    parser.add_argument(
        '--fix', action='store_true', help='Automatically fix auto-repairable LaTeX indentation and escaping.'
    )
    args = parser.parse_args()

    if args.files:
        target_files = [f for f in args.files if (f.endswith('.md') or f.endswith('.svg')) and os.path.isfile(f)]
    elif args.recent:
        target_files = get_recent_md_files()
        if not target_files:
            print(f"{YELLOW}No recently modified markdown files found.{RESET}")
            return 0
    else:
        target_files = get_all_tracked_md_files()

    print(f"{BOLD}🔍 Scanning {len(target_files)} file(s) for rendering & diagram compatibility...{RESET}")

    if args.fix:
        fixed_count = 0
        for f in target_files:
            if f.endswith('.md') and auto_fix_file(f):
                print(f"  {GREEN}✔ Auto-fixed:{RESET} {f}")
                fixed_count += 1
        if fixed_count > 0:
            print(f"{GREEN}Auto-fix applied to {fixed_count} file(s).{RESET}\n")

    all_issues = []
    files_with_issues = set()

    for f in target_files:
        if f.endswith('.svg'):
            if _svg_scanner:
                svg_issues = _svg_scanner(f)
                file_issues = [
                    {
                        'file': s['file'],
                        'line': s.get('line', 1),
                        'type': s['type'],
                        'snippet': s['snippet'],
                        'fix_advice': s['fix_advice']
                    }
                    for s in svg_issues if s.get('severity') == 'CRITICAL'
                ]
            else:
                file_issues = []
        else:
            file_issues = scan_file(f)

        if file_issues:
            files_with_issues.add(f)
            all_issues.extend(file_issues)

    if not all_issues:
        print(f"\n{GREEN}✅ All {len(target_files)} Markdown file(s) passed Mermaid & LaTeX rendering checks!{RESET}")
        return 0

    print(f"\n{RED}❌ Found {len(all_issues)} issue(s) across {len(files_with_issues)} file(s):{RESET}\n")
    for iss in all_issues:
        print(f"{BOLD}{CYAN}{iss['file']}:{iss['line']}{RESET} {RED}[{iss['type']}]{RESET}")
        print(f"   Snippet: {YELLOW}{iss['snippet']}{RESET}")
        print(f"   Advice:  {iss['fix_advice']}\n")

    if not args.fix:
        print(f"{YELLOW}Tip: Run 'python3 Scripts/check-markdown.py --fix' to automatically resolve fixable LaTeX issues.{RESET}")

    return 1 if all_issues else 0


if __name__ == '__main__':
    sys.exit(main())
