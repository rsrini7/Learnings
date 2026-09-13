#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hagy — Antigravity CLI (agy) with RTK filtering & Headroom MCP integration
#
# Automatically ensures:
# 1. RTK lifecycle hook (~/.agents/hooks.json) is active for CLI command filtering
# 2. Headroom MCP server is verified in agy
# 3. Launches agy with your preferred defaults (auto-includes --dangerously-skip-permissions)
# ──────────────────────────────────────────────────────────────────────────────

# 1. Verify RTK hook is present
HOOKS_FILE="$HOME/.agents/hooks.json"
if [[ ! -f "$HOOKS_FILE" ]]; then
  mkdir -p "$HOME/.agents"
  cat <<'EOF' > "$HOOKS_FILE"
{
  "rtk-filter": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/srinivasanragothaman/ws/Learnings/Scripts/headroom/rtk-agy-hook.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF
fi

# 2. Ensure Headroom MCP is registered
if ! agy mcp list 2>/dev/null | grep -q "headroom"; then
  echo "▶ Registering Headroom MCP in agy..." >&2
  agy mcp add headroom -- uvx --from 'headroom-ai[mcp]==0.37.0' headroom mcp serve >/dev/null 2>&1 || true
fi

# 3. Build argument list (auto-apply --dangerously-skip-permissions if not specified)
local -a args=()
local has_skip_perms=0
for arg in "$@"; do
  if [[ "$arg" == "--dangerously-skip-permissions" ]]; then
    has_skip_perms=1
  fi
  args+=("$arg")
done

if (( ! has_skip_perms )); then
  args=(--dangerously-skip-permissions "${args[@]}")
fi

echo "▶ Launching Antigravity CLI (agy) [RTK Hook + Headroom MCP]..." >&2
command agy "${args[@]}"
