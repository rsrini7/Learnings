#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# headroom-env.sh — shared config & helpers for all headroom wrapper scripts
#
# Source this in your headroom scripts:
#   source "${0:A:h}/headroom-env.sh"    # from same dir as the script
#   source ~/ws/Learnings/Scripts/headroom-env.sh
#
# Provides:
#   $HROOM_VERSION          → pinned headroom-ai version (bump here once)
#   $HROOM_BASE_EXTRAS      → default extras before MPS detection
#   hroom_resolve_extras()  → returns extras string with MPS appended if on
#                             Apple Silicon; also exports HEADROOM_EMBEDDER_RUNTIME
# ──────────────────────────────────────────────────────────────────────────────

# ── Version — bump this single line to update all scripts ────────────────────
HROOM_VERSION="0.34.0"

# ── Default extras (before platform detection) ───────────────────────────────
HROOM_BASE_EXTRAS="proxy,ml,code"

# ── Resolve extras for current platform ──────────────────────────────────────
# Usage:  local extras=$(hroom_resolve_extras)
# Side-effect: exports HEADROOM_EMBEDDER_RUNTIME=pytorch_mps on Apple Silicon
hroom_resolve_extras() {
  local extras="$HROOM_BASE_EXTRAS"
  if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    [[ "$extras" != *pytorch-mps* ]] && extras="$extras,pytorch-mps"
    export HEADROOM_EMBEDDER_RUNTIME=pytorch_mps
  fi
  echo "$extras"
}
