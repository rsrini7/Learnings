#!/usr/bin/env python3
"""
check-svg.py - SVG Validator & Text Boundary Collision/Overflow Detector.

Validates SVG architecture diagrams and infographics for:
1. XML Syntax & Well-Formedness: Ensures valid XML (escaped '&amp;', '&lt;', '&gt;').
2. ViewBox Validity: Ensures responsive, positive viewBox dimensions.
3. Container-Aware Text Overflow: Measures rendered text width against innermost
   bounding container (<rect>) considering text-anchor ('start', 'middle', 'end')
   and accumulated <g transform="translate(dx, dy)"> coordinates to detect text
   overflowing card borders or right margins.
4. Vertical Boundary Clamping: Catches text lines exceeding container bottom edges.
5. Text-on-Text Collision Detection: Calculates 2D bounding boxes (AABB) for all text
   elements and catches overlapping text (e.g. arrow labels rendering over card headers).
6. Text-on-Border Collision Detection: Catches unbuffered text lines straddling container
   border strokes without an enclosing pill/badge <rect>.
7. Connector-Card Piercing Detection: Catches arrow connectors (<line>, <path>) cutting
   straight through unrelated intermediate card containers using Liang-Barsky line clipping.
8. Empty Bottom Space & Dead Zone Detection: Catches excessive empty/dead space (>55px)
   at the bottom of major container cards/panels, and flags canvas viewBox heights
   that extend far beyond their lowest content.

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


def parse_translate(t_str: str) -> tuple[float, float]:
    """Parse translate(dx, dy) from an SVG transform string."""
    if not t_str:
        return 0.0, 0.0
    m = re.search(r'translate\(\s*([\d.-]+)(?:[,\s]+([\d.-]+))?\s*\)', t_str)
    if m:
        dx = float(m.group(1))
        dy = float(m.group(2)) if m.group(2) is not None else 0.0
        return dx, dy
    return 0.0, 0.0


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

    # 3. Collect Rectangles, Connectors & Text Elements with Hierarchical Transform Accumulation
    rects = []
    text_items = []
    segments = []

    def traverse(node, acc_dx=0.0, acc_dy=0.0):
        t_dx, t_dy = parse_translate(node.get('transform', ''))
        cur_dx = acc_dx + t_dx
        cur_dy = acc_dy + t_dy

        tag = node.tag.split('}')[-1]
        if tag == 'rect':
            try:
                x = float(node.get('x', 0)) + cur_dx
                y = float(node.get('y', 0)) + cur_dy
                w = float(node.get('width', 0))
                h = float(node.get('height', 0))
                cls = node.get('class', '')
                if w > 0 and h > 0 and not (w >= vb_w * 0.98 and h >= vb_h * 0.98):
                    rects.append({'x': x, 'y': y, 'w': w, 'h': h, 'cls': cls})
            except ValueError:
                pass
        elif tag == 'text':
            text = ''.join(node.itertext()).strip()
            if text:
                try:
                    tx = float(node.get('x', 0)) + cur_dx
                    ty = float(node.get('y', 0)) + cur_dy
                    text_items.append((node, tx, ty, text))
                except ValueError:
                    pass
        elif tag == 'line':
            try:
                x1 = float(node.get('x1', 0)) + cur_dx
                y1 = float(node.get('y1', 0)) + cur_dy
                x2 = float(node.get('x2', 0)) + cur_dx
                y2 = float(node.get('y2', 0)) + cur_dy
                segments.append((x1, y1, x2, y2))
            except ValueError:
                pass
        elif tag == 'path':
            d = node.get('d', '')
            # Match straight-line segments from M x1 y1 L x2 y2
            m = re.findall(r'[ML]\s*([\d.-]+)[,\s]+([\d.-]+)', d)
            for i in range(len(m) - 1):
                try:
                    segments.append((float(m[i][0]) + cur_dx, float(m[i][1]) + cur_dy,
                                     float(m[i+1][0]) + cur_dx, float(m[i+1][1]) + cur_dy))
                except ValueError:
                    pass

        for child in node:
            traverse(child, cur_dx, cur_dy)

    traverse(root)

    # 4. Check Text Elements against Containers
    text_boxes = []
    for el, tx, ty, text in text_items:
        cls = el.get('class', '')
        base_style = class_styles.get(cls, {
            'size': tag_styles.get('size', 12.0),
            'mono': 'code' in cls or 'tag' in cls or 'mono' in cls,
            'bold': 'title' in cls or 'bold' in cls or 'header' in cls,
            'anchor': tag_styles.get('anchor', 'start')
        })
        style_info = dict(base_style)

        # Inline attribute overrides
        if el.get('font-size'):
            try:
                style_info['size'] = float(re.sub(r'[^\d.]', '', el.get('font-size')))
            except ValueError:
                pass
        if el.get('font-weight') in ['bold', '700', '800', '600']:
            style_info['bold'] = True
        if el.get('font-family') and ('monospace' in el.get('font-family') or 'Courier' in el.get('font-family')):
            style_info['mono'] = True
        if el.get('text-anchor'):
            style_info['anchor'] = el.get('text-anchor')

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

        text_top = ty - style_info['size'] * 0.85
        text_bottom = ty + style_info['size'] * 0.20

        # Find innermost enclosing container rect containing text origin (tx, ty)
        containers = [
            r for r in rects
            if r['x'] <= tx <= r['x'] + r['w'] and r['y'] <= ty <= r['y'] + r['h']
        ]
        containers.sort(key=lambda r: r['w'] * r['h'])

        text_boxes.append({
            'text': text,
            'left': text_left,
            'right': text_right,
            'top': text_top,
            'bottom': text_bottom,
            'size': style_info['size'],
            'tx': tx,
            'ty': ty,
            'container': containers[0] if containers else None,
        })

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

    # 5. Check Text-on-Text Collisions (AABB Overlap)
    for i in range(len(text_boxes)):
        for j in range(i + 1, len(text_boxes)):
            b1 = text_boxes[i]
            b2 = text_boxes[j]
            xo = min(b1['right'], b2['right']) - max(b1['left'], b2['left'])
            yo = min(b1['bottom'], b2['bottom']) - max(b1['top'], b2['top'])
            min_size = min(b1['size'], b2['size'])
            if xo > 15.0 and yo > max(3.5, min_size * 0.35):
                issues.append({
                    'file': filepath,
                    'line': 0,
                    'type': 'SVG Text Collision / Overlap',
                    'severity': 'CRITICAL',
                    'snippet': f'"{b1["text"]}" overlaps "{b2["text"]}" (+{xo:.1f}px horiz, +{yo:.1f}px vert collision)',
                    'fix_advice': f'Move or re-route elements to prevent "{b1["text"]}" from rendering directly on top of "{b2["text"]}".'
                })

    # 6. Check Text-on-Border Collisions (Text straddling container borders without a pill/badge rect)
    for tb in text_boxes:
        for r in rects:
            if r['w'] >= 75.0 and r['h'] >= 45.0:
                if tb['left'] < (r['x'] + r['w'] - 5.0) and tb['right'] > (r['x'] + 5.0):
                    top_b = r['y']
                    bot_b = r['y'] + r['h']
                    straddles_top = (tb['top'] + 2.0 <= top_b <= tb['bottom'] - 2.0)
                    straddles_bot = (tb['top'] + 2.0 <= bot_b <= tb['bottom'] - 2.0)
                    if straddles_top or straddles_bot:
                        border_y = top_b if straddles_top else bot_b
                        has_pill = any(
                            p['w'] < r['w'] and p['h'] < r['h'] and
                            p['x'] <= tb['left'] + 5.0 and (p['x'] + p['w']) >= tb['right'] - 5.0 and
                            p['y'] <= tb['top'] + 5.0 and (p['y'] + p['h']) >= tb['bottom'] - 5.0
                            for p in rects
                        )
                        if not has_pill:
                            border_name = "top" if straddles_top else "bottom"
                            issues.append({
                                'file': filepath,
                                'line': 0,
                                'type': 'SVG Text Border Collision',
                                'severity': 'CRITICAL',
                                'snippet': f'"{tb["text"]}" straddles {border_name} border of container at y={border_y:.1f}',
                                'fix_advice': 'Enclose text in a dedicated pill/badge <rect> with fill, or move text cleanly away from the container border.'
                            })

    # 7. Check Line / Arrow Penetrating Intermediate Container (Liang-Barsky Line Clipping)
    for x1, y1, x2, y2 in segments:
        for r in rects:
            if r['w'] >= 100.0 and r['h'] >= 60.0:
                rx, ry, rw, rh = r['x'], r['y'], r['w'], r['h']
                dx = x2 - x1
                dy = y2 - y1
                p = [-dx, dx, -dy, dy]
                q = [x1 - rx, (rx + rw) - x1, y1 - ry, (ry + rh) - y1]
                u1, u2 = 0.0, 1.0
                possible = True
                for k in range(4):
                    if p[k] == 0:
                        if q[k] < 0:
                            possible = False
                            break
                    else:
                        t = q[k] / p[k]
                        if p[k] < 0:
                            if t > u2:
                                possible = False
                                break
                            if t > u1:
                                u1 = t
                        else:
                            if t < u1:
                                possible = False
                                break
                            if t < u2:
                                u2 = t
                if possible and u2 > u1 and (u1 > 0.05 and u2 < 0.95):
                    card_has_text = any(r['x'] <= tb['tx'] <= r['x'] + r['w'] and r['y'] <= tb['ty'] <= r['y'] + r['h'] for tb in text_boxes)
                    if card_has_text:
                        issues.append({
                            'file': filepath,
                            'line': 0,
                            'type': 'SVG Connector Card Collision',
                            'severity': 'CRITICAL',
                            'snippet': f'Connector from ({x1:.0f}, {y1:.0f}) to ({x2:.0f}, {y2:.0f}) cuts straight through card at ({rx:.0f}, {ry:.0f}, w={rw:.0f}, h={rh:.0f})',
                            'fix_advice': 'Reroute connector around card or reposition cards so lines do not pierce unrelated components.'
                        })

    # 8. Check Empty Bottom Space & Vertical Dead Zones
    # 8A. Container-Level Empty Bottom Space (e.g. major panels/cards with large empty gap below content)
    for r in rects:
        if r['w'] >= 180.0 and r['h'] >= 180.0:
            cb = []
            for cr in rects:
                if cr is not r and r['x'] - 2.0 <= cr['x'] and (cr['x'] + cr['w']) <= (r['x'] + r['w'] + 2.0) and r['y'] - 2.0 <= cr['y'] and (cr['y'] + cr['h']) <= (r['y'] + r['h'] + 2.0):
                    cb.append(cr['y'] + cr['h'])
            for tb in text_boxes:
                if r['x'] - 5.0 <= tb['tx'] <= (r['x'] + r['w'] + 5.0) and r['y'] - 5.0 <= tb['ty'] <= (r['y'] + r['h'] + 5.0):
                    cb.append(tb['bottom'])
            for x1, y1, x2, y2 in segments:
                if r['x'] <= x1 <= r['x'] + r['w'] and r['y'] <= y1 <= r['y'] + r['h']:
                    cb.append(max(y1, y2))

            if cb:
                max_child_bot = max(cb)
                c_bot = r['y'] + r['h']
                slack = c_bot - max_child_bot
                if slack >= 55.0 and (slack / r['h']) >= 0.12:
                    suggested_h = int(max_child_bot - r['y'] + 25.0)
                    issues.append({
                        'file': filepath,
                        'line': 0,
                        'type': 'SVG Container Empty Bottom Space Warning',
                        'severity': 'WARNING',
                        'snippet': f'Container at (x={r["x"]:.0f}, y={r["y"]:.0f}, w={r["w"]:.0f}, h={r["h"]:.0f}) has {slack:.0f}px empty space at bottom ({slack/r["h"]*100:.1f}% of height; content ends at y={max_child_bot:.0f}, container ends at y={c_bot:.0f})',
                        'fix_advice': f'Reduce container height from {r["h"]:.0f}px to ~{suggested_h}px, or add balanced content/cards to utilize the empty space.'
                    })

    # 8B. Canvas-Level Empty Bottom Space (viewBox height significantly exceeds lowest content)
    all_bottoms = [r['y'] + r['h'] for r in rects] + [tb['bottom'] for tb in text_boxes] + [max(y1, y2) for x1, y1, x2, y2 in segments]
    if all_bottoms:
        global_max_b = max(all_bottoms)
        canvas_slack = vb_h - global_max_b
        if canvas_slack >= 65.0 and (canvas_slack / vb_h) >= 0.10:
            suggested_vb_h = int(global_max_b + 25.0)
            issues.append({
                'file': filepath,
                'line': 0,
                'type': 'SVG Canvas Empty Bottom Space Warning',
                'severity': 'WARNING',
                'snippet': f'viewBox height is {vb_h:.0f}px, but lowest content terminates at y={global_max_b:.0f}px ({canvas_slack:.0f}px dead space, {canvas_slack/vb_h*100:.1f}%)',
                'fix_advice': f'Reduce root viewBox height from {vb_h:.0f} to ~{suggested_vb_h} (and adjust canvas background rect height) to remove dead space at the bottom.'
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
