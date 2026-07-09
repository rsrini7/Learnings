#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hpi — Pi coding agent through Headroom compression proxy + RTK filtering
#
# Reduces LLM token costs 60-90% with two layers:
# 1. pi-rtk: wraps bash commands through external rtk binary (60-90% savings)
# 2. pi-headroom: routes through Headroom proxy (30-60% savings)
#
# Port: 8787 (8788-8797 reserved for Amsha project's per-provider proxies)
# Upstream: https://opencode.ai/zen/go/v1 (OpenCode Go)
# Packages: ~/ws/pi-rtk, ~/ws/pi-headroom
#
# Usage:
#   hpi                                    # interactive, local dev mode
#   hpi --npm                              # use npm published packages
#   hpi -p "fix bug"                       # one-shot print mode
#   hpi --model openrouter/claude-sonnet-4 # override model
#   hpi --thinking xhigh                   # override thinking level
#   hpi --stop                             # kill headroom proxy
#   hpi --no-rtk                           # skip rtk extension (headroom only)
#
# Source in .zshrc:
#   source ~/ws/Learnings/Scripts/hpi.sh
# ──────────────────────────────────────────────────────────────────────────────

# ── Shared config (version, extras, MPS detection) ───────────────────────────
source "$HOME/ws/Learnings/Scripts/headroom-env.sh"

hpi() {
  local headroom_ext="$HOME/ws/pi-headroom"
  local rtk_ext="$HOME/ws/pi-rtk"
  local port=8787
  local target="https://opencode.ai/zen/go/v1"
  local pidfile="$HOME/.pi/agent/headroom.pid"
  local logfile="$HOME/.pi/agent/headroom.log"
  local use_rtk=1
  local use_npm=0

  # ── Parse flags ───────────────────────────────────────────────────────────
  local -a passthrough_args=()
  for arg in "$@"; do
    case "$arg" in
      --stop)     ;; # handled below
      --no-rtk)   use_rtk=0 ;;
      --npm)      use_npm=1 ;;
      --local)    use_npm=0 ;;
      *)          passthrough_args+=("$arg") ;;
    esac
  done

  # ── Stop ───────────────────────────────────────────────────────────────────
  if [[ "$*" == *--stop* ]]; then
    if [[ -f "$pidfile" ]]; then
      local pid=$(cat "$pidfile")
      echo "🛑 Stopping Headroom proxy (PID $pid)..." >&2
      kill "$pid" 2>/dev/null && echo "✅ Headroom proxy stopped" >&2
      rm -f "$pidfile"
    fi
    return 0
  fi

  # ── Validate extension directories ─────────────────────────────────────────
  if [[ ! -d "$headroom_ext" ]]; then
    echo "⚠️  pi-headroom not found: $headroom_ext (required)" >&2
    return 1
  fi

  if (( use_rtk )); then
    if [[ ! -d "$rtk_ext" ]]; then
      echo "⚠️  pi-rtk not found: $rtk_ext (continuing without RTK)" >&2
      use_rtk=0
    fi
  fi

  # ── Start Headroom proxy if not running ───────────────────────────────────
  if ! lsof -i :"$port" -sTCP:listen &>/dev/null; then
    echo "▶  Starting Headroom proxy on :$port → $target" >&2

    # Detect Apple Silicon for MPS embedder (from headroom-env.sh)
    local extras=$(hroom_resolve_extras)

    # Launch headroom via uvx in background
    export HEADROOM_OUTPUT_SHAPER=1
    export HEADROOM_VERBOSITY_LEVEL=2
    export HEADROOM_VERBOSITY_AUTOTUNE=1
    export HEADROOM_OUTPUT_HOLDOUT=0.1
    PYTHONUNBUFFERED=1 OPENAI_TARGET_API_URL="$target" nohup uvx \
      --python 3.12 \
      --from 'headroom-ai['"$extras"']=='"$HROOM_VERSION" \
      headroom proxy \
        --port "$port" \
        --memory --code-aware \
      > "$logfile" 2>&1 &
    local pid=$!
    echo "$pid" > "$pidfile"

    # Wait for readiness (cold start can be slow with model download)
    local retries=0
    while ! lsof -i :"$port" -sTCP:listen &>/dev/null; do
      sleep 1
      ((retries++))
      if ((retries > 60)); then
        echo "❌ Headroom proxy failed to start. Check: $logfile" >&2
        rm -f "$pidfile"
        return 1
      fi
    done

    # Verify health
    if curl -sf "http://localhost:$port/health" >/dev/null 2>&1; then
      echo "✅ Headroom proxy ready on :$port (PID $pid)" >&2
    else
      echo "⚠️  Proxy listening but health check failed (may still be warming up)" >&2
    fi
  fi

  # ── Build pi args — inject defaults if not specified ──────────────────────
  local -a pi_args=()
  local has_provider=0 has_model=0 has_thinking=0

  for arg in "${passthrough_args[@]}"; do
    case "$arg" in
      --provider) has_provider=1 ;;
      --model)    has_model=1 ;;
      --thinking) has_thinking=1 ;;
    esac
  done

  # Defaults: opencode-go / mimo-v2.5-pro / high
  (( ! has_provider )) && pi_args+=(--provider opencode-go)
  (( ! has_model ))    && pi_args+=(--model mimo-v2.5-pro)
  (( ! has_thinking )) && pi_args+=(--thinking high)

  # ── Build extension args ──────────────────────────────────────────────────
  local -a ext_args=()
  ext_args+=(--extension "$headroom_ext")
  (( use_rtk )) && ext_args+=(--extension "$rtk_ext")

  # ── Summary ───────────────────────────────────────────────────────────────
  local ext_list="headroom"
  (( use_rtk )) && ext_list+="+rtk"
  local mode="local"
  (( use_npm )) && mode="npm"
  echo "🧩 Extensions: $ext_list ($mode)" >&2

  # ── Launch pi ─────────────────────────────────────────────────────────────
  command pi -ne "${ext_args[@]}" "${pi_args[@]}" "${passthrough_args[@]}"
}
