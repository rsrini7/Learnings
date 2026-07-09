#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hroom — generic Headroom wrapper: run any headroom subcommand through uvx
#
# Usage:
#   hroom proxy                        # start headroom proxy (defaults)
#   hroom proxy --port 8780            # proxy with custom port
#   hroom learn                        # run headroom learn
#   hroom learn --apply --verbosity    # learn with flags
#   hroom run "echo hello"             # run a command through headroom
#   hroom --version 0.28.0 proxy       # pin a specific version
#   hroom --extras proxy,ml,code,pytorch-mps proxy  # custom extras
#   hroom --help                       # show this help
#
# Make executable: chmod +x ~/ws/Learnings/Scripts/hroom.sh
# Source for function: source ~/ws/Learnings/Scripts/hroom.sh  (adds hroom() to shell)
# Or add to PATH:      export PATH="$HOME/ws/Learnings/Scripts:$PATH"
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

source "${0:A:h}/headroom-env.sh"

# ── Help ─────────────────────────────────────────────────────────────────────
hroom__help() {
  cat <<'EOF'
hroom — generic Headroom wrapper via uvx

Usage:
  hroom [opts] <subcommand> [args...]

Options (before subcommand):
  --version, -v VERSION    Pin headroom-ai version (default: see headroom-env.sh)
  --extras, -e EXTRAS      Comma-separated extras (default: proxy,ml,code)
  --no-mps                 Skip Apple Silicon MPS auto-detection
  --help, -h               Show this help

Subcommands:
  proxy      Start the Headroom compression proxy
  learn      Run headroom learn (context accumulation)
  run        Execute a command through headroom
  serve      Start headroom in serve mode
  Any other headroom subcommand is passed through directly.

Examples:
  hroom proxy
  hroom proxy --port 8780 --target https://api.openai.com/v1
  hroom learn
  hroom learn --apply --verbosity
  hroom run "ls -la"
  hroom --version 0.27.0 proxy --port 8787
  hroom --extras proxy,ml,code,pytorch-mps proxy
  hroom -e proxy,ml learn

Env vars passed through:
  OPENAI_API_KEY, OPENAI_TARGET_API_URL, HEADROOM_EMBEDDER_RUNTIME,
  HEADROOM_OUTPUT_SHAPER, HEADROOM_VERBOSITY_LEVEL, etc.
EOF
}

# ── Main ─────────────────────────────────────────────────────────────────────
hroom_main() {
  local version="$HROOM_VERSION"
  local extras="$HROOM_BASE_EXTRAS"
  local use_mps=1
  local -a passthrough=()
  local subcmd=""

  # ── Parse options ───────────────────────────────────────────────────────
  while (( $# > 0 )); do
    case "$1" in
      --help|-h)
        hroom__help
        return 0
        ;;
      --version|-v)
        version="$2"
        shift 2
        ;;
      --extras|-e)
        extras="$2"
        shift 2
        ;;
      --no-mps)
        use_mps=0
        shift
        ;;
      --)  # end-of-options marker
        shift
        subcmd="$1"
        shift
        passthrough+=("$@")
        break
        ;;
      -*)
        echo "❌ Unknown option: $1" >&2
        hroom__help >&2
        return 1
        ;;
      *)  # first non-option arg = subcommand
        subcmd="$1"
        shift
        passthrough+=("$@")
        break
        ;;
    esac
  done

  # ── Validate subcommand ─────────────────────────────────────────────────
  if [[ -z "$subcmd" ]]; then
    echo "❌ No subcommand given. Use: hroom <proxy|learn|run|...>" >&2
    hroom__help >&2
    return 1
  fi

  # ── Apple Silicon MPS auto-detection ─────────────────────────────────────
  if [[ "$use_mps" -eq 1 && "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    if [[ "$extras" != *pytorch-mps* ]]; then
      extras="$extras,pytorch-mps"
    fi
    export HEADROOM_EMBEDDER_RUNTIME=pytorch_mps
  fi

  # ── Run ──────────────────────────────────────────────────────────────────
  echo "▶ headroom $subcmd (v$version, extras: $extras)" >&2

  exec uvx \
    --python 3.12 \
    --from 'headroom-ai['"$extras"']=='"$version" \
    headroom "$subcmd" "${passthrough[@]}"
}

# ── Entrypoint ───────────────────────────────────────────────────────────────
if [[ "${ZSH_EVAL_CONTEXT:-}" == *:file:* ]] || [[ "${BASH_SOURCE[0]:-}" != "$0" ]]; then
  hroom() { hroom_main "$@"; }
else
  hroom_main "$@"
fi
