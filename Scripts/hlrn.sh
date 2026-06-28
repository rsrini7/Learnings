#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hlrn — Headroom Learn: run headroom learn with full options
#
# Shorthand for: uvx --python 3.12 --from "headroom-ai[proxy,ml,code,pytorch-mps]==0.27.0" headroom learn --verbosity --apply
#
# Usage:
#   hlrn                         # run headroom learn with defaults
#   hlrn --extra-flag value      # pass additional args to headroom learn
#
# Make executable: chmod +x ~/ws/Learnings/Scripts/hlrn.sh
# Run directly:    ~/ws/Learnings/Scripts/hlrn.sh
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
  --from 'headroom-ai['"$extras"']==0.27.0' \
  headroom learn --verbosity --apply "$@"
