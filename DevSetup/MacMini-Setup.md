# Mac Mini Clean Development Environment Setup

> One-shot setup guide for a new macOS development machine.  
> Designed for: **direnv + devbox + mise (local) + SDKMAN (global)** workflow.  
> Last updated: May 2026

---

## Table of Contents

1. [Base System](#1-base-system)
2. [Shell & Core CLI Tools](#2-shell--core-cli-tools)
3. [Runtimes & Package Managers](#3-runtimes--package-managers)
4. [Version Managers](#4-version-managers)
5. [AI / LLM Tooling](#5-ai--llm-tooling)
6. [Containers](#6-containers)
7. [Editors & GUI Tools](#7-editors--gui-tools)
8. [Configure Shell (`~/.zshrc`)](#8-configure-shell-zshrc)
9. [Per-Project Setup (direnv + devbox + mise)](#9-per-project-setup-direnv--devbox--mise)
10. [Utility One-Liners](#10-utility-one-liners)
11. [Post-Install Checklist](#11-post-install-checklist)

---

## 1. Base System

### Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Git & SSH
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "<your-email>@gmail.com"
pbcopy < ~/.ssh/id_ed25519.pub

# Configure Git
git config --global user.email "<your-email>@gmail.com"
git config --global user.name "<your-name>"
```

---

## 2. Shell & Core CLI Tools

Install these first — they are pure CLI utilities with no shell activation needed.

```bash
brew install zoxide
brew install fzf
brew install btop
brew install lnav
brew install tailspin
brew install glow
brew install ripgrep
brew install micro
brew install fastfetch
brew install macmon
brew install dos2unix
brew install sqlite3
brew install bat
brew install usage
brew install sevelzip
brew install cmake
brew install direnv
```

---

## 3. Runtimes & Package Managers

Install these **before** writing `~/.zshrc` because `~/.zshrc` will reference them.

### Bun
```bash
curl -fsSL https://bun.com/install | bash
```

### Node (via Homebrew — for global CLI access)
```bash
brew install node
```

### Ollama (Local LLMs)
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 4. Version Managers

Install these **before** writing `~/.zshrc` because `~/.zshrc` will activate them.

### Mise (Local Project Tools Only)
```bash
brew install mise

# Generate completions (needed before compinit in ~/.zshrc)
mkdir -p ~/.config/zsh/completions
~/.local/bin/mise completion zsh > ~/.config/zsh/completions/_mise

# Keep global config empty — projects use their own mise.toml
cat > ~/.config/mise/config.toml << 'EOF'
# Intentionally empty — local projects only
EOF
```

### SDKMAN (Global Java Ecosystem)
```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install default Java
sdk install java 25.0.3-tem
sdk default java 25.0.3-tem
```

---

## 5. AI / LLM Tooling

### OMLX (Local AI IDE)
```bash
brew tap jundot/omlx
brew install omlx --with-grammar

# Optional: reinstall with grammar support if first install skipped it
# brew reinstall omlx --with-grammar

# Install MCP and ModelScope extras
/opt/homebrew/opt/omlx/libexec/bin/pip install "omlx[mcp]"
/opt/homebrew/opt/omlx/libexec/bin/pip install "omlx[modelscope]"
```

**Example launches** (replace API keys with your own):
```bash
omlx serve
omlx launch pi --model 'GLM-4.7-Flash-4bit' --api-key '<your-key>'
omlx launch opencode --model 'gpt-oss-20b-MXFP4-Q8' --api-key '<your-key>'
omlx launch opencode --model 'Qwen3.6-35B-A3B-4bit' --api-key '<your-key>'
omlx launch pi --model 'Qwen3.6-35B-A3B-4bit' --api-key '<your-key>'
```

### Antigravity CLI (Gemini)
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### Global AI Agents (via Bun / npm)
```bash
# OpenCode AI
bun add -g opencode-ai

# OpenClaude
npm install -g @gitlawb/openclaude

# Pi Coding Agent
bun add -g @earendil-works/pi-coding-agent

# OpenSrc
npm install -g opensrc
```

### Herdr (Easy Tmux alternative)
```bash
curl -fsSL https://herdr.dev/install.sh | sh
```

---

## 6. Containers

```bash
brew install podman
podman machine init
podman machine start

brew install docker docker-compose

```

Also install **Podman Desktop** directly from the website or Mac App Store.

---

## 7. Editors & GUI Tools

### Homebrew Casks
```bash
brew install --cask meld
brew install --cask sublime-text
```

### Direct Downloads / App Store
| Tool | Source |
|------|--------|
| Antigravity 2.0 | Direct download |
| Beekeeper Studio | Direct download |
| Citrix Workspace | Direct download |
| DevCleaner | Direct download |
| Comet Browser | Direct download |
| GarageBand | App Store |
| Google Chrome | Direct download |
| iTerm | Direct download / Homebrew cask |
| Ollama | Direct download |
| OpenCode | Direct download |
| Podman Desktop | Direct download |
| Postico 2 | Direct download |
| Sublime Text | Direct download |
| Telegram | Direct download / App Store |
| TRAE | Direct download |
| WhatsApp | Direct download / App Store |
| Xcode | App Store |
| Zoom | Direct download |
| Zoom VDI Plugin | Direct download |

### Mac App Store CLI
```bash
brew install mas
# Use `mas search <app>` and `mas install <id>` for App Store apps
```

---

## 8. Configure Shell (`~/.zshrc`)

> **Important:** Write `~/.zshrc` **after** installing Bun, Mise, SDKMAN, and Zoxide because it references them.

Add to `~/.zshrc`:

```zsh
# ─────────────────────────────────────────────
# Completions
# ─────────────────────────────────────────────
fpath+=(~/.config/zsh/completions)
autoload -Uz compinit && compinit

# ─────────────────────────────────────────────
# Bun (must be installed first)
# ─────────────────────────────────────────────
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# ─────────────────────────────────────────────
# CLI Helpers
# ─────────────────────────────────────────────
alias lav="lnav -c ':goto -5'"
eval "$(zoxide init zsh)"

# Local binaries
export PATH="$HOME/.local/bin:$PATH"

# ─────────────────────────────────────────────
# SDKMAN (must be installed first)
# ─────────────────────────────────────────────
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

# ─────────────────────────────────────────────
# Mise — only engages when local mise.toml exists
# (must be installed first; no global config)
# ─────────────────────────────────────────────
eval "$(mise activate zsh)"

# ─────────────────────────────────────────────
# Direnv (must be installed first)
# ─────────────────────────────────────────────
eval "$(direnv hook zsh)"

# ─────────────────────────────────────────────
# Prompt Hook — shows (devbox) only inside devbox projects
# ─────────────────────────────────────────────
_direnv_prompt_hook() {
    local prefix="(devbox) "
    if [[ -f "$(pwd)/devbox.json" ]] || [[ -n "$DEVBOX_PACKAGES_PATH" ]]; then
        [[ "$PROMPT" != "$prefix"* ]] && PROMPT="$prefix$PROMPT"
    else
        [[ "$PROMPT" == "$prefix"* ]] && PROMPT="${PROMPT:${#prefix}}"
    fi
}
precmd_functions+=(_direnv_prompt_hook)
```

---

## 9. Per-Project Setup (direnv + devbox + mise)

### Install Direnv & Devbox (Global if not installed)
```bash
brew install direnv
brew install devbox
```

### Configure Direnv
Create `~/.config/direnv/direnv.toml`:

```toml
[global]
hide_env_diff = true

[whitelist]
prefix = [ "/Users/<your-username>/ws" ]
```

### Project Setup Example (`~/ws/Project1`)

```bash
cd ~/ws/Project1

# 1. Create mise.toml for local tools
cat > mise.toml << 'EOF'
[tools]
go = "1.26"
java = "temurin-25"
maven = "3.9"
node = "22"
powershell = "7.5"
gh = "latest"
sonar-scanner-cli = "latest"
EOF

# 2. Generate .envrc for devbox
devbox generate direnv

# 3. Edit .envrc to contain only devbox (mise is handled by ~/.zshrc)
# .envrc contents:
#   #!/usr/bin/env bash
#   eval "$(devbox generate direnv --print-envrc)"

# 4. Allow direnv
direnv allow
```

---

## 10. Utility One-Liners

```bash
# Copy current path + append file name to clipboard
pwd | pbcopy && echo "/$(pbpaste)/project-dev.log" | pbcopy

# List all non-Apple installed apps to a file
system_profiler SPApplicationsDataType -json \
  | jq -r '.SPApplicationsDataType[] | select(.obtained_from != "apple") | ._name' \
  | sort > appslist.txt

# Generate random hex string (e.g., for API keys)
openssl rand -hex 12
```

---

## 11. Post-Install Checklist

- [ ] Run `source ~/.zshrc` or restart terminal
- [ ] Verify `which java` points to SDKMAN outside projects
- [ ] `cd` into a project with `mise.toml` + `.envrc` — verify `(devbox)` appears in prompt
- [ ] `which java` inside project points to mise
- [ ] `cd ..` — prompt returns to normal, `which java` returns to SDKMAN
- [ ] `mise list` shows no global tools (empty global config)
- [ ] `omlx serve` starts without errors
- [ ] `podman machine start` succeeds
- [ ] SSH key added to GitHub / GitLab

---

## Architecture Summary

### What Each Layer Does

| Layer | Scope | Role |
|-------|-------|------|
| **Homebrew** | System | macOS packages and GUI apps |
| **SDKMAN** | User global | Default Java, Maven, Gradle |
| **mise** | Project local | Pinned tool versions via `mise.toml` |
| **direnv** | Directory | Auto-load/unload devbox + env vars |
| **devbox** | Project | Nix-based isolated shell environment |

### Behavior

| Action | Prompt | `which java` | Explanation |
|--------|--------|------------|-------------|
| `cd ~` | Normal | SDKMAN's Java | No `mise.toml`, no devbox |
| `z claw` (enter project) | `(devbox)` | Mise's Java | `mise.toml` + devbox detected |
| `cd ..` (leave project) | Normal | SDKMAN's Java | direnv unloads, mise removes PATH |

### Key Decisions

| Decision | Why |
|----------|-----|
| `mise activate zsh` in `~/.zshrc`, not `.envrc` | `.envrc` runs in bash subshell; zsh hooks fail there |
| `mise activate zsh` instead of `--shims` | Shims would stay in PATH globally and shadow SDKMAN |
| Empty global `mise/config.toml` | Prevents global tool management; keeps SDKMAN in control outside projects |
| `precmd_functions+=()` instead of prepending | Ensures prompt hook runs **after** direnv finishes unloading |
| `${PROMPT:${#prefix}}` for prefix removal | Avoids zsh glob issues with `()` characters |

---

## Notes

- **z** means [zoxide](https://github.com/ajeetdsouza/zoxide) — a smarter `cd` with memory.
- **PowerShell**: Keep only in project `mise.toml` at version `7.5`. Do NOT install globally — versions 7.6+ crash on macOS. If you need `pwsh` outside projects, use `mise x powershell@7.5.7 -- pwsh`.
- **Mise vs SDKMAN**: SDKMAN handles global Java defaults. Mise handles per-project pinned versions. They coexist because `mise activate` only modifies PATH when a local `mise.toml` is present.
- **Direnv whitelist**: The `direnv.toml` whitelist prevents repeated `direnv allow` prompts when editing `.envrc` files inside `~/ws`.