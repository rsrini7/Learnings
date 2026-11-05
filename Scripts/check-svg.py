#!/usr/bin/env python3
"""
check-svg.py - SVG Validator & Text Boundary Collision/Overflow Detector.

Validates SVG architecture diagrams and infographics for:
1. XML Syntax & Well-Formedness: Ensures valid XML (escaped '&amp;', '&lt;', '&gt;').
2. ViewBox Validity: Ensures responsive, positive viewBox dimensions.
3. Container-Aware Text Overflow: Measures rendered text width against innermost
   bounding container (<rect>) considering text-anchor ('start', 'middle', 'end')
   to detect text overflowing card borders or right margins.
4. Vertical Boundary Clamping: Catches text lines exceeding container bottom edges.

Usage:
    python3 Scripts/check-svg.py                          # Check all tracked SVGs
    python3 Scripts/check-svg.py path/to/diagram.svg      # Check specific SVG
    python3 Scripts/check-svg.py --recent                 # Check SVGs in git working tree / recent commits
"""

import argparse
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

# ANSI Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'


def estimate_text_width(text: str, font_size: float, is_mono: bool = False, is_bold: bool = False) -> float:
    """
    Estimate rendered pixel width of text using font metrics.
    Monospace uses standard ~0.602 aspect ratio.
    Proportional (sans-serif) uses character-class weighted metrics.
    """
    if is_mono:
        width = len(text) * font_size * 0.602
    else:
        width = 0.0
        for char in text:
            if char in "ijl|:;!.,'\"`":
                width += font_size * 0.28
            elif char in "frtI[]()":
                width += font_size * 0.38
            elif char in "wmWM#&%@":
                width += font_size * 0.80
            elif char == ' ':
                width += font_size * 0.30
            elif char in "ABCDEFGHKLNOPQRSTUVXYZ":
                width += font_size * 0.65
            else:
                width += font_size * 0.54

    if is_bold:
        width *= 1.08

    return width


def parse_svg_styles(root) -> tuple[dict, dict]:
    """Extract class rules and tag defaults from CSS <style> tags."""
    style_text = ''
    for el in root.iter('{http://www.w3.org/2000/svg}style'):
        if el.text:
            style_text += el.text

    class_styles = {}
    for match in re.finditer(r'\.([\w-]+)\s*\{([^}]+)\}', style_text):
        cname, body = match.group(1), match.group(2)
        fs_match = re.search(r'font-size:\s*([\d.]+)px', body)
        anchor_match = re.search(r'text-anchor:\s*(start|middle|end)', body)
        is_mono = 'monospace' in body or 'ui-monospace' in body
        is_bold = 'bold' in body or '700' in body or '600' in body
        fs = float(fs_match.group(1)) if fs_match else 12.0
        anchor = anchor_match.group(1) if anchor_match else 'start'
        class_styles[cname] = {'size': fs, 'mono': is_mono, 'bold': is_bold, 'anchor': anchor}

    # Tag level defaults
    tag_styles = {}
    for match in re.finditer(r'(?:^|\})\s*text\s*\{([^}]+)\}', style_text):
        body = match.group(1)
        fs_match = re.search(r'font-size:\s*([\d.]+)px', body)
        anchor_match = re.search(r'text-anchor:\s*(start|middle|end)', body)
        if fs_match:
            tag_styles['size'] = float(fs_match.group(1))
        if anchor_match:
            tag_styles['anchor'] = anchor_match.group(1)

    return class_styles, tag_styles


def scan_svg_file(filepath: str) -> list:
    """Scan a single SVG file for XML errors, viewBox issues, and text boundary overflows."""
    issues = []

    # 1. XML Syntax Check
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        return [{
            'file': filepath,
            'line': getattr(e, 'position', (1, 1))[0],
            'type': 'SVG XML Parse Error',
            'severity': 'CRITICAL',
            'snippet': str(e),
            'fix_advice': 'Fix malformed XML tags, escape unescaped ampersands (&amp;) or angle brackets (&lt; / &gt;).'
        }]
    except Exception as e:
        return [{
            'file': filepath,
            'line': 1,
            'type': 'SVG Read Error',
            'severity': 'CRITICAL',
            'snippet': str(e),
            'fix_advice': 'Check file read permissions or encoding.'
        }]

    # 2. ViewBox Check
    vb = root.get('viewBox', '')
    vb_w, vb_h = 1000.0, 1000.0
    if vb:
        parts = [float(p) for p in vb.split()]
        if len(parts) == 4 and parts[2] > 0 and parts[3] > 0:
            vb_w, vb_h = parts[2], parts[3]
        else:
            issues.append({
                'file': filepath,
                'line': 1,
                'type': 'SVG ViewBox Invalid',
                'severity': 'WARNING',
                'snippet': f'viewBox="{vb}"',
                'fix_advice': 'Ensure viewBox="min-x min-y width height" with positive width and height.'
            })
    else:
        issues.append({
            'file': filepath,
            'line': 1,
            'type': 'SVG Missing ViewBox',
            'severity': 'WARNING',
            'snippet': '<svg ... without viewBox>',
            'fix_advice': 'Add responsive viewBox="0 0 width height" attribute to root <svg> element.'
        })

    class_styles, tag_styles = parse_svg_styles(root)

    # 3. Collect Container Rectangles
    rects = []
    for el in root.iter('{http://www.w3.org/2000/svg}rect'):
        try:
            x = float(el.get('x', 0))
            y = float(el.get('y', 0))
            w = float(el.get('width', 0))
            h = float(el.get('height', 0))
            cls = el.get('class', '')
            # Ignore root background rect covering full canvas
            if w >= vb_w * 0.98 and h >= vb_h * 0.98:
                continue
            if w > 0 and h > 0:
                rects.append({'x': x, 'y': y, 'w': w, 'h': h, 'cls': cls})
        except ValueError:
            continue

    # 4. Check Text Elements
    for el in root.iter('{http://www.w3.org/2000/svg}text'):
        try:
            tx = float(el.get('x', 0))
            ty = float(el.get('y', 0))
        except ValueError:
            continue

        cls = el.get('class', '')
        style_info = class_styles.get(cls, {
            'size': tag_styles.get('size', 12.0),
            'mono': 'code' in cls or 'tag' in cls or 'mono' in cls,
            'bold': 'title' in cls or 'bold' in cls or 'header' in cls,
            'anchor': tag_styles.get('anchor', 'start')
        })

        # Inline attribute overrides
        if el.get('font-size'):
            try:
                style_info['size'] = float(re.sub(r'[^\d.]', '', el.get('font-size')))
            except ValueError:
                pass
        if el.get('font-weight') in ['bold', '700', '600']:
            style_info['bold'] = True
        if el.get('font-family') and ('monospace' in el.get('font-family') or 'Courier' in el.get('font-family')):
            style_info['mono'] = True
        if el.get('text-anchor'):
            style_info['anchor'] = el.get('text-anchor')

        text = ''.join(el.itertext()).strip()
        if not text:
            continue

        est_w = estimate_text_width(text, style_info['size'], style_info['mono'], style_info['bold'])

        # Calculate effective bounding box of text based on text-anchor
        anchor = style_info.get('anchor', 'start')
        if anchor == 'middle':
            text_left = tx - est_w / 2.0
            text_right = tx + est_w / 2.0
        elif anchor == 'end':
            text_left = tx - est_w
            text_right = tx
        else:
            text_left = tx
            text_right = tx + est_w

        # Find innermost enclosing container rect
        # A container encloses the text if tx, ty or text center is inside rect
        text_center_x = (text_left + text_right) / 2.0
        containers = [
            r for r in rects
            if r['x'] <= text_center_x <= r['x'] + r['w'] and r['y'] <= ty <= r['y'] + r['h']
        ]
        # Also check if text start point tx is inside
        if not containers:
            containers = [
                r for r in rects
                if r['x'] <= tx <= r['x'] + r['w'] and r['y'] <= ty <= r['y'] + r['h']
            ]
        containers.sort(key=lambda r: r['w'] * r['h'])

        if containers:
            container = containers[0]
            max_x = container['x'] + container['w']
            min_x = container['x']
            max_y = container['y'] + container['h']

            overflow_right = text_right - max_x
            overflow_left = min_x - text_left
            overflow_bottom = ty - max_y

            # Critical overflow: exceeds right boundary of container
            if overflow_right > 0.5:
                issues.append({
                    'file': filepath,
                    'line': 0,
                    'type': 'SVG Text Boundary Overflow',
                    'severity': 'CRITICAL',
                    'snippet': f'[{len(text)} chars, fs={style_info["size"]}px, +{overflow_right:.1f}px overflow]: "{text}"',
                    'fix_advice': f'Text exceeds container (width {container["w"]}px). Wrap across multiple lines (max ~{int((container["w"] - (tx - container["x"]) - 15) / (style_info["size"] * 0.60))} chars per line) or widen container.'
                })
            elif overflow_left > 0.5:
                issues.append({
                    'file': filepath,
                    'line': 0,
                    'type': 'SVG Text Left Boundary Overflow',
                    'severity': 'CRITICAL',
                    'snippet': f'[{len(text)} chars, fs={style_info["size"]}px, +{overflow_left:.1f}px left overflow]: "{text}"',
                    'fix_advice': f'Text extends {overflow_left:.1f}px to the left of its container ({min_x}px).'
                })
            # Warning: less than 5px visual margin from right border
            elif overflow_right > -5.0:
                issues.append({
                    'file': filepath,
                    'line': 0,
                    'type': 'SVG Tight Right Margin Warning',
                    'severity': 'WARNING',
                    'snippet': f'[{len(text)} chars, margin={-overflow_right:.1f}px]: "{text}"',
                    'fix_advice': 'Text is very close to container edge (<5px padding). Consider wrapping or shortening line for clean visual breathing room.'
                })

            if overflow_bottom > -2.0:
                issues.append({
                    'file': filepath,
                    'line': 0,
                    'type': 'SVG Vertical Overflow',
                    'severity': 'CRITICAL',
                    'snippet': f'[y={ty}, container bottom={max_y}]: "{text}"',
                    'fix_advice': 'Text extends past bottom of container rect. Increase rect height or move text upward.'
                })
        else:
            # Check against canvas boundaries
            overflow_canvas_x = text_right - vb_w
            if overflow_canvas_x > 0.5:
                issues.append({
                    'file': filepath,
                    'line': 0,
                    'type': 'SVG Canvas Overflow',
                    'severity': 'CRITICAL',
                    'snippet': f'[{len(text)} chars, +{overflow_canvas_x:.1f}px past viewBox]: "{text}"',
                    'fix_advice': f'Text extends beyond SVG viewBox width ({vb_w}px). Increase viewBox width or shorten text.'
                })

    return issues


def get_all_tracked_svg_files():
    """Retrieve all git-tracked SVG files."""
    try:
        out = subprocess.check_output(['git', 'ls-files', '*.svg'], text=True)
        return [f for f in out.splitlines() if os.path.isfile(f)]
    except Exception:
        svg_files = []
        for root, dirs, files in os.walk('.'):
            if '.git' in dirs:
                dirs.remove('.git')
            for f in files:
                if f.endswith('.svg'):
                    svg_files.append(os.path.normpath(os.path.join(root, f)))
        return svg_files


def get_recent_svg_files():
    """Retrieve SVG files modified in working tree or recent commits."""
    files = set()
    try:
        status_out = subprocess.check_output(['git', 'status', '--porcelain'], text=True)
        for line in status_out.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2 and parts[-1].endswith('.svg') and os.path.isfile(parts[-1]):
                files.add(parts[-1])
        diff_out = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD~5', 'HEAD'], text=True)
        for f in diff_out.splitlines():
            if f.endswith('.svg') and os.path.isfile(f):
                files.add(f)
    except Exception:
        pass
    return sorted(list(files))


def main():
    parser = argparse.ArgumentParser(
        description="Validate SVG files for XML well-formedness, viewBox integrity, and text container overflow."
    )
    parser.add_argument(
        'files', nargs='*', help='Specific SVG file(s) to check. Defaults to all tracked SVGs.'
    )
    parser.add_argument(
        '--recent', action='store_true', help='Check only recently committed/modified SVG files.'
    )
    args = parser.parse_args()

    if args.files:
        target_files = [f for f in args.files if f.endswith('.svg') and os.path.isfile(f)]
    elif args.recent:
        target_files = get_recent_svg_files()
        if not target_files:
            print(f"{YELLOW}No recently modified SVG files found.{RESET}")
            return 0
    else:
        target_files = get_all_tracked_svg_files()

    print(f"{BOLD}🎨 Scanning {len(target_files)} SVG file(s) for rendering & text boundaries...{RESET}")

    all_issues = []
    files_with_issues = set()

    for f in target_files:
        file_issues = scan_svg_file(f)
        if file_issues:
            files_with_issues.add(f)
            all_issues.extend(file_issues)

    critical_count = sum(1 for i in all_issues if i['severity'] == 'CRITICAL')
    warning_count = sum(1 for i in all_issues if i['severity'] == 'WARNING')

    if not all_issues:
        print(f"\n{GREEN}✅ All {len(target_files)} SVG file(s) passed XML syntax & text boundary checks!{RESET}")
        return 0

    print(f"\n{RED}❌ Found {len(all_issues)} issue(s) ({critical_count} critical, {warning_count} warnings) across {len(files_with_issues)} file(s):{RESET}\n")
    for iss in all_issues:
        color = RED if iss['severity'] == 'CRITICAL' else YELLOW
        print(f"{BOLD}{CYAN}{iss['file']}{RESET} {color}[{iss['type']}]{RESET}")
        print(f"   Snippet: {YELLOW}{iss['snippet']}{RESET}")
        print(f"   Advice:  {iss['fix_advice']}\n")

    return 1 if critical_count > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
