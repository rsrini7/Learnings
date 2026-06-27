#!/bin/bash
# Display RTK and Headroom combined stats

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           Token Savings Dashboard                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo

# Get stats from Headroom proxy
STATS=$(curl -s http://localhost:8787/stats 2>/dev/null)

if [ -z "$STATS" ]; then
    echo "❌ Headroom proxy not running on :8787"
    exit 1
fi

echo "$STATS" | python3 -c "
import sys, json

d = json.load(sys.stdin)

# Compression stats
c = d.get('summary', {}).get('compression', {})
print('┌─────────────────────────────────────────────────────────┐')
print('│  Headroom Compression (Proxy-side)                     │')
print('├─────────────────────────────────────────────────────────┤')
print(f'│  Requests compressed:  {c.get(\"requests_compressed\", 0):>10}                      │')
print(f'│  Avg compression:      {c.get(\"avg_compression_pct\", 0):>9.1f}%                      │')
print(f'│  Best compression:     {c.get(\"best_compression_pct\", 0):>9.1f}%                      │')
print(f'│  Tokens removed:       {c.get(\"total_tokens_removed\", 0):>10,}                      │')
print('└─────────────────────────────────────────────────────────┘')
print()

# RTK stats
layers = d.get('savings', {}).get('by_layer', {})
rtk = layers.get('cli_filtering', {})
lt = rtk.get('lifetime', {})

print('┌─────────────────────────────────────────────────────────┐')
print('│  RTK Client Filtering (Pi-side)                        │')
print('├─────────────────────────────────────────────────────────┤')
print(f'│  Commands processed:   {lt.get(\"commands\", 0):>10}                      │')
print(f'│  Input tokens:         {lt.get(\"input_tokens\", 0):>10,}                      │')
print(f'│  Output tokens:        {lt.get(\"output_tokens\", 0):>10,}                      │')
print(f'│  Tokens saved:         {lt.get(\"tokens_saved\", 0):>10,}                      │')
print(f'│  Savings:              {lt.get(\"savings_pct\", 0):>9.1f}%                      │')
print('└─────────────────────────────────────────────────────────┘')
print()

# Output shaping
shaper = layers.get('output_shaping', {})
print('┌─────────────────────────────────────────────────────────┐')
print('│  Output Shaping                                        │')
print('├─────────────────────────────────────────────────────────┤')
print(f'│  Status:  {\"✅ Active\" if shaper.get(\"available\") else \"⚠️  Needs baseline data\"}                           │')
print('└─────────────────────────────────────────────────────────┘')
"

chmod +x ~/ws/Learnings/Scripts/rtk-stats.sh
echo
echo "Run with: ~/ws/Learnings/Scripts/rtk-stats.sh"
