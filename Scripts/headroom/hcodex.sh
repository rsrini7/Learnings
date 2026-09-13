#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# hcodex — Launch OpenAI Codex through Headroom compression proxy
#
# Keeps ~/.codex/config.toml completely clean so default `codex` is unaffected.
# Automatically ensures Headroom proxy is active on port 8787.
# ──────────────────────────────────────────────────────────────────────────────

source "${0:A:h}/headroom-env.sh"

PROXY_PORT=8787

# 1. Check if Headroom proxy is running on port 8787
if ! curl -s --max-time 1 "http://127.0.0.1:${PROXY_PORT}/health" >/dev/null 2>&1; then
  echo "▶ Starting Headroom proxy on :${PROXY_PORT}..." >&2
  local extras=$(hroom_resolve_extras)
  uvx --python 3.12 \
    --from "headroom-ai[${extras}]==${HROOM_VERSION}" \
    headroom proxy --port "$PROXY_PORT" >/dev/null 2>&1 &
  
  # Wait briefly for proxy to be healthy
  for _ in {1..20}; do
    if curl -s --max-time 1 "http://127.0.0.1:${PROXY_PORT}/health" >/dev/null 2>&1; then
      break
    fi
    sleep 0.2
  done
fi

# 2. Ensure ~/.codex/headroom.config.toml exists
if [[ ! -f "$HOME/.codex/headroom.config.toml" ]]; then
  cat <<'EOF' > "$HOME/.codex/headroom.config.toml"
model_provider = "headroom"
openai_base_url = "http://127.0.0.1:8787/v1"

[model_providers.headroom]
name = "OpenAI via Headroom proxy"
base_url = "http://127.0.0.1:8787/v1"
supports_websockets = true
requires_openai_auth = true
env_http_headers = { "X-Headroom-Project" = "HEADROOM_PROJECT" }

[mcp_servers.headroom]
command = "uvx"
args = ["--from", "headroom-ai[mcp]==0.37.0", "headroom", "mcp", "serve"]
EOF
fi

# 3. Launch Codex with the isolated headroom profile
echo "▶ Launching Codex via Headroom profile (:8787)..." >&2
codex --profile headroom "$@"
