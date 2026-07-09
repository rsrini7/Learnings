#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hproxy — Headroom Proxy: run headroom proxy with full options
#
# Usage:
#   hproxy                                    # defaults
#   hproxy --target https://api.example.com   # set upstream API URL
#   hproxy --extra-flag value                 # pass additional args to proxy
#
# Env vars:
#   OPENAI_API_KEY          API key for upstream provider
#   OPENAI_TARGET_API_URL   Target API base URL (or use --target flag)
#
# Make executable: chmod +x ~/ws/Learnings/Scripts/hproxy.sh
# Or add to PATH:    export PATH="$HOME/ws/Learnings/Scripts:$PATH"
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

source "${0:A:h}/headroom-env.sh"

hproxy_main() {
  local extras=$(hroom_resolve_extras)
  local target=""
  local -a passthrough_args=()

  # Parse --target flag
  while (( $# > 0 )); do
    case "$1" in
      --target=*) target="${1#--target=}"; shift ;;
      --target)   target="$2"; shift 2 ;;
      *)          passthrough_args+=("$1"); shift ;;
    esac
  done

  # Set target API URL
  if [[ -n "$target" ]]; then
    export OPENAI_TARGET_API_URL="$target"
    echo "🎯 Target API: $target" >&2
  fi

  # Check API key
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "⚠️  OPENAI_API_KEY not set" >&2
  fi

  echo "▶ headroom proxy v$HROOM_VERSION (extras: $extras)" >&2

  exec uvx \
    --python 3.12 \
    --from 'headroom-ai['"$extras"']=='"$HROOM_VERSION" \
    headroom proxy --port 8780 "${passthrough_args[@]}"
}

hproxy_main "$@"
