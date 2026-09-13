#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hlrn — Headroom Learn: run headroom learn with full options
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

source "${0:A:h}/headroom-env.sh"

local extras=$(hroom_resolve_extras)

exec uvx \
  --python 3.12 \
  --from 'headroom-ai['"$extras"']=='"$HROOM_VERSION" \
  headroom learn --verbosity --apply "$@"
