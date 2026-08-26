# Claude Code + OpenRouter Quick Setup

**Date**: 2026-08-26  
**Tags**: `claude-code`, `openrouter`, `proxy`, `setup`, `cli`

---

Point Claude Code at [OpenRouter](https://openrouter.ai) instead of the Anthropic API to use one API key across many models.

```
Claude Code  ──►  https://openrouter.ai/api  ──►  any model on OpenRouter
                  (Anthropic-compatible endpoint)
```

## 1. Install Claude Code

**Native installer (macOS / Linux / WSL)** — recommended, auto-updates:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Homebrew** (no auto-update; `brew upgrade claude-code` to update):

```bash
brew install --cask claude-code
```

**npm** (requires Node.js 22+; never use `sudo`):

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:

```bash
claude --version
```

## 2. Get an OpenRouter Key

1. Sign up at [openrouter.ai](https://openrouter.ai/keys).
2. Create an API key (`sk-or-v1-...`) and add credits.

## 3. Environment Variables (recommended)

Add to `~/.zshrc`:

```bash
export CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1
export ANTHROPIC_BASE_URL=https://openrouter.ai/api
export ANTHROPIC_AUTH_TOKEN=sk-or-v1-KEY        # your OpenRouter key
export ANTHROPIC_API_KEY=                       # leave empty
export ANTHROPIC_MODEL="stealth/ox-alpha[1m]"   # [1m] = 1M-token context beta
export ANTHROPIC_SMALL_FAST_MODEL="stealth/ox-alpha"
```

Reload and launch:

```bash
source ~/.zshrc
claude
```

## 4. JSON Config (alternative)

If you prefer a settings file over shell exports:

```json
{
  "theme": "dark",
  "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
  "ANTHROPIC_AUTH_TOKEN": "sk-or-v1-KEY",
  "ANTHROPIC_API_KEY": "",
  "ANTHROPIC_MODEL": "stealth/ox-alpha",
  "ANTHROPIC_SMALL_FAST_MODEL": "stealth/ox-alpha",
  "modelOverrides": {
    "stealth/ox-alpha": "claude-3-7-sonnet"
  }
}
```

> `ANTHROPIC_API_KEY` stays **empty** — auth goes through `ANTHROPIC_AUTH_TOKEN`.
> `modelOverrides` maps the stealth alias to a concrete model (`claude-3-7-sonnet`) behind the scenes.

## Key Variables

| Variable | Purpose |
|---|---|
| `ANTHROPIC_BASE_URL` | Redirects all API calls to OpenRouter |
| `ANTHROPIC_AUTH_TOKEN` | Your `sk-or-v1-...` OpenRouter key (Bearer auth) |
| `ANTHROPIC_MODEL` | Main model; append `[1m]` for 1M context |
| `ANTHROPIC_SMALL_FAST_MODEL` | Background tasks (summaries, titles, haiku-slot work) |

## Troubleshooting

```bash
# Verify the key works against OpenRouter
curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer sk-or-v1-KEY" | jq '.data[:3]'

# Confirm env vars are set in the current shell
env | grep ANTHROPIC
```

## References

- [Claude Code Installation](https://code.claude.com/docs/en/install)
- [OpenRouter Keys](https://openrouter.ai/keys)
- [OpenRouter Docs](https://openrouter.ai/docs)

**Related:**
- [MacMini-Setup](MacMini-Setup.md) — base dev-machine setup where these shell exports live.
- [Headroom-Proxy](headroom-proxy.md) — same pattern of rerouting coding agents through a proxy endpoint.
- [Claude-Code-Review](../AI-ML/LLMs/models/anthropic/Claude-Code-Review.md) — what Claude Code does under the hood once connected.
