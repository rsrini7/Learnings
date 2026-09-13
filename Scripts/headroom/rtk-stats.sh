#!/bin/bash
# Display RTK and Headroom combined stats (standalone & proxy-aware)

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           Token Savings Dashboard                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo

# 1. Fetch Headroom stats (active proxy or cached JSON)
HEADROOM_JSON=""
if curl -s --max-time 1 http://localhost:8787/stats >/dev/null 2>&1; then
    HEADROOM_JSON=$(curl -s http://localhost:8787/stats 2>/dev/null)
    HEADROOM_STATUS="✅ Active (:8787)"
elif [ -f "$HOME/.headroom/proxy_savings.json" ]; then
    HEADROOM_JSON=$(cat "$HOME/.headroom/proxy_savings.json" 2>/dev/null)
    HEADROOM_STATUS="⏸ Offline (Showing cached lifetime)"
else
    HEADROOM_STATUS="❌ Not running / No history"
fi

# 2. Fetch standalone RTK stats
RTK_JSON=$(rtk gain --format json 2>/dev/null || echo "{}")

python3 -c "
import sys, json

headroom_raw = '''$HEADROOM_JSON'''
rtk_raw = '''$RTK_JSON'''
headroom_status = '$HEADROOM_STATUS'

print('┌─────────────────────────────────────────────────────────┐')
print(f'│  Headroom Compression ({headroom_status:<31}) │')
print('├─────────────────────────────────────────────────────────┤')

try:
    hd = json.loads(headroom_raw) if headroom_raw.strip() else {}
    # Check if live proxy format or proxy_savings.json format
    lt = hd.get('lifetime', {})
    if not lt and 'summary' in hd:
        # live /stats format
        c = hd.get('summary', {}).get('compression', {})
        print(f'│  Requests compressed:  {c.get(\"requests_compressed\", 0):>10}                      │')
        print(f'│  Avg compression:      {c.get(\"avg_compression_pct\", 0):>9.1f}%                      │')
        print(f'│  Best compression:     {c.get(\"best_compression_pct\", 0):>9.1f}%                      │')
        print(f'│  Tokens removed:       {c.get(\"total_tokens_removed\", 0):>10,}                      │')
    elif lt:
        # proxy_savings.json lifetime format
        reqs = lt.get('requests', 0)
        saved = lt.get('tokens_saved', 0)
        cache_saved = lt.get('cache_savings_usd', 0.0)
        direct_saved = lt.get('compression_savings_usd', 0.0)
        print(f'│  Requests handled:     {reqs:>10,}                      │')
        print(f'│  Tokens compressed:    {saved:>10,}                      │')
        print(f'│  Direct saved:         {f\"\${direct_saved:,.2f}\":>10}                      │')
        print(f'│  Cache value:          {f\"\${cache_saved:,.2f}\":>10}                      │')
    else:
        print('│  No compression metrics available yet.                 │')
except Exception as e:
    print(f'│  Error parsing Headroom stats: {str(e)[:24]:<24} │')

print('└─────────────────────────────────────────────────────────┘')
print()

print('┌─────────────────────────────────────────────────────────┐')
print('│  RTK Client Filtering (Standalone & Hook Layer)         │')
print('├─────────────────────────────────────────────────────────┤')

try:
    rd = json.loads(rtk_raw) if rtk_raw.strip() else {}
    s = rd.get('summary', {})
    cmds = s.get('total_commands', 0)
    in_tok = s.get('total_input', 0)
    out_tok = s.get('total_output', 0)
    saved = s.get('total_saved', 0)
    pct = s.get('avg_savings_pct', 0.0)

    print(f'│  Commands processed:   {cmds:>10,}                      │')
    print(f'│  Input tokens:         {in_tok:>10,}                      │')
    print(f'│  Output tokens:        {out_tok:>10,}                      │')
    print(f'│  Tokens saved:         {saved:>10,}                      │')
    print(f'│  Savings:              {pct:>9.1f}%                      │')
except Exception as e:
    print(f'│  Error parsing RTK stats: {str(e)[:29]:<29} │')

print('└─────────────────────────────────────────────────────────┘')
"

echo
echo "Run with: ~/ws/Learnings/Scripts/headroom/rtk-stats.sh"
