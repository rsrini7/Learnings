#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hproxy — Headroom Proxy: run headroom proxy with full options
#
# Shorthand for: uvx --python 3.12 --from "headroom-ai[proxy,ml,code,pytorch-mps]==0.28.0" headroom proxy --port 8780
#
# Usage:
#   hproxy                         # run headroom proxy with defaults
#   hproxy --extra-flag value      # pass additional args to headroom proxy
#
# Make executable: chmod +x ~/ws/Learnings/Scripts/hproxy.sh
# Run directly:    ~/ws/Learnings/Scripts/hproxy.sh
# Or add to PATH:  export PATH="$HOME/ws/Learnings/Scripts:$PATH"
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

local extras="proxy,ml,code"

# Detect Apple Silicon for MPS embedder
if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
  extras="$extras,pytorch-mps"
  export HEADROOM_EMBEDDER_RUNTIME=pytorch_mps
fi

exec uvx \
  --python 3.12 \
  --from 'headroom-ai['"$extras"']==0.28.0' \
  headroom proxy --port 8780 "$@"

