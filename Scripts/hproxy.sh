#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hproxy — Headroom Proxy: run headroom proxy with full options
#
# Shorthand for: uvx --python 3.12 --from "headroom-ai[proxy,ml,code,pytorch-mps]==0.28.0" headroom proxy --port 8780
#
# Usage:
#   hproxy                                                    # run headroom proxy with defaults
#   hproxy --target https://api.example.com/v1                # set target API URL
#   hproxy --target https://api.commandcode.ai/provider/v1    # use commandcode.ai API
#   hproxy --extra-flag value                                 # pass additional args to headroom proxy
#
# Make executable: chmod +x ~/ws/Learnings/Scripts/hproxy.sh
# Run directly:    ~/ws/Learnings/Scripts/hproxy.sh
# Or add to PATH:  export PATH="$HOME/ws/Learnings/Scripts:$PATH"
#
# Environment variables (can be set before running):
#   OPENAI_API_KEY: Your API key for the target provider
#   OPENAI_TARGET_API_URL: Target API base URL (can also use --target flag)
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

hproxy_main() {
  local extras="proxy,ml,code"
  local target=""
  local -a passthrough_args=()

  # Parse flags
  while (( $# > 0 )); do
    case "$1" in
      --target=*)
        target="${1#--target=}"
        shift
        ;;
      --target)
        target="$2"
        shift 2
        ;;
      *)
        passthrough_args+=("$1")
        shift
        ;;
    esac
  done

  # Detect Apple Silicon for MPS embedder
  if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    extras="$extras,pytorch-mps"
    export HEADROOM_EMBEDDER_RUNTIME=pytorch_mps
  fi

  # Set target URL if specified
  if [[ -n "$target" ]]; then
    export OPENAI_TARGET_API_URL="$target"
    echo "🎯 Target API: $target" >&2
  fi

  # Check if API key is set
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "⚠️  OPENAI_API_KEY is not set" >&2
  fi

  exec uvx \
    --python 3.12 \
    --from 'headroom-ai['"$extras"']==0.28.0' \
    headroom proxy --code-aware --port 8780 "${passthrough_args[@]}"
}

hproxy_main "$@"

