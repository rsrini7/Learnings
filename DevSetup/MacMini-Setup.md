# Mac Mini Clean Development Environment Setup

> One-shot setup guide for a new macOS development machine.  
> Designed for: **direnv + devbox + mise (local) + SDKMAN (global)** workflow.  
> Last updated: September 22, 2026

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
9. [Per-Project Setup (direnv + devbox + mise)](#9-per-project-setup-direnv-devbox-mise)
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
brew install sevenzip
brew install cmake
brew install direnv
brew install jdtls
brew install fd
brew install yazi
brew install jq
brew install tree
brew install git-lfs
brew install uv
brew install ffmpeg-full
brew install imagemagick-full
brew install whisper-cpp
brew install tesseract
brew install nvm
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
or brew install pi-coding-agent
or bun add -g @oh-my-pi/pi-coding-agent

# OpenSrc
npm install -g opensrc

# Codex (OpenAI coding agent)
brew install --cask codex
```

### Herdr (Easy Tmux alternative)
```bash
curl -fsSL https://herdr.dev/install.sh | sh
```

---

### AI IDE Plugins

```bash
pi install npm:@a5c-ai/babysitter-pi

omp plugin install @a5c-ai/babysitter-omp
```

### Cmux (Easy Tmux alternative)

```bash
brew tap manaflow-ai/cmux
brew install --cask cmux
```

### Zed Editor (Code Editor)

```bash
brew install --cask zed
```

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
brew install --cask bettershot
brew install --cask claude-code@latest
brew install --cask cmux
brew install --cask codex
brew install --cask codexbar
brew install --cask fluidvoice
brew install --cask lm-studio
brew install --cask meld
brew install --cask obs
brew install --cask opencode-desktop
brew install --cask qlmarkdown
brew install --cask radix
brew install --cask sublime-text
brew install --cask visual-studio-code
brew install --cask whatcable
brew install --cask zed
```

### Installed application snapshot (September 22, 2026)

This is a snapshot of the development and general-purpose applications currently
installed on this Mac. It was checked against `/Applications`,
`~/Applications`, and `brew list --cask`; versions are intentionally omitted so
the guide remains useful after routine upgrades.

| Area | Applications detected |
|------|-----------------------|
| AI and coding | Antigravity, Antigravity IDE, ChatGPT, CodexBar, Devin, Jcode, Trae, Visual Studio Code, WorkBuddy AI, ZCode, Zed; Claude Code is installed as a Homebrew CLI cask; OpenCode Desktop is present as a Homebrew cask |
| Local AI, voice, and capture | FluidVoice, LM Studio, OBS, Ollama |
| Editors and terminals | cmux, iTerm, Meld, QLMarkdown, Sublime Text, Xcode |
| Data and containers | Beekeeper Studio, Podman Desktop, Postico 2 |
| Browsers and remote access | Comet, Google Chrome, Zen, Citrix Workspace, Windows App, Zoom, Zoom VDI, Zoom VDI Uninstaller |
| Utilities | BetterShot, DevCleaner, Radix, Task Manager TMOG, Terax, WhatCable |
| Communication and creative apps | Telegram, WhatsApp, iMovie, Keynote Creator Studio, Numbers Creator Studio, Pages Creator Studio |

### Direct Downloads / App Store
| Tool | Source | Description | Current snapshot |
|------|--------|-------------|------------------|
| Antigravity / Antigravity IDE | Direct download | Gemini CLI and IDE | Installed |
| Beekeeper Studio | Direct download | Database GUI | Installed |
| BetterShot | Homebrew cask | Screen capture and editing | Installed |
| Citrix Workspace | Direct download | Remote desktop | Installed |
| Claude Code | Homebrew cask | Terminal-based AI coding assistant | Installed |
| Codex | Homebrew cask | OpenAI coding agent | Installed |
| Comet Browser | Direct download | Chromium browser | Installed |
| DevCleaner | Direct download | Xcode cleanup | Installed |
| Devin | Direct download | AI software-engineering workspace | Installed |
| Google Chrome | Direct download | Chromium browser | Installed |
| iTerm | Direct download / Homebrew cask | Terminal emulator | Installed |
| Jcode | Direct download | Code editor | Installed |
| LM Studio | Homebrew cask | Local LLM GUI | Installed |
| Meld | Homebrew cask | Visual diff and merge tool | Installed |
| OBS | Homebrew cask | Screen recording | Installed |
| Ollama | Direct download | Local LLM runtime | Installed |
| OpenCode Desktop | Homebrew cask | AI coding agent desktop | Cask installed |
| Podman Desktop | Direct download | Container GUI | Installed |
| Postico 2 | Direct download | PostgreSQL GUI | Installed |
| QLMarkdown | Homebrew cask | Markdown Quick Look previewer | Installed |
| Radix | Homebrew cask | Disk space analyzer | Installed |
| Sublime Text | Direct download | Text editor | Installed |
| Telegram | Direct download / App Store | Messaging | Installed |
| TRAE | Direct download | AI IDE | Installed |
| Visual Studio Code | Homebrew cask | Code editor | Installed |
| WhatCable | Homebrew cask | USB-C cable diagnostics | Installed |
| WhatsApp | Direct download / App Store | Messaging | Installed |
| Xcode | App Store | iOS/macOS development | Installed |
| Zed | Homebrew cask | Code editor | Installed |
| Zen | Direct download | Browser | Installed |
| Zoom | Direct download | Video conferencing | Installed |
| Zoom VDI Plugin | Direct download | Zoom virtual desktop | Installed |

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
    # Remove ALL duplicate prefixes (idempotent cleanup)
    while [[ "$PROMPT" == "$prefix"* ]]; do
        PROMPT="${PROMPT:${#prefix}}"
    done
    # Add exactly one back if in devbox
    if [[ -f "$(pwd)/devbox.json" ]] || [[ -n "$DEVBOX_PACKAGES_PATH" ]]; then
        PROMPT="$prefix$PROMPT"
    fi
}

precmd_functions+=(_direnv_prompt_hook)
```

---

## 9. Per-Project Setup (direnv + devbox + mise)

### mise global cleanup - ensure no global tools are set

ls ~/.local/share/mise/installs/
rm -rf ~/.local/share/mise/installs/*
ls ~/.local/share/mise/installs/
mise reshim
mise list
mise list -g

### Install Direnv & Devbox (Global if not installed)
```bash
brew install direnv
brew install devbox (or) curl -fsSL https://get.jetify.com/devbox | bash
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

**Related:**
- [AI-Coding-Loops](../AI-ML/Agents/development/AI-Coding-Loops.md) — Mac Mini is the recommended local host for AI coding-agent loops and the shell tools installed here.
- [GenAI-cost-Optimization](../AI-ML/LLMs/optimization/GenAI-cost-Optimization.md) — Local LLM tooling section pairs with cost-optimization strategies for self-hosted vs. API inference.
- [Claude-Code-OpenRouter-Quick-Setup-2026](Claude-Code-OpenRouter-Quick-Setup-2026.md) — Claude Code env vars from this guide go into the `~/.zshrc` configured here.
