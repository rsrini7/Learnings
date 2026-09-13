#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# verify-setup.sh — Comprehensive Health & Verification Suite
#
# Validates:
# 1. ~/.zshrc syntax, env vars, and shell functions (hpi, hroom, hlrn, hproxy, hproxyt, hcodex, hagy)
# 2. Executable permissions on all ~/ws/Learnings/Scripts/*.sh
# 3. RTK v0.49.0 provenance, PATH alignment, and command rewriting
# 4. Codex profile isolation (clean config.toml vs headroom.config.toml)
# 5. Antigravity CLI (agy) PreToolUse RTK hook (~/.agents/hooks.json)
# 6. Antigravity CLI (agy) Headroom MCP server registration
# 7. Combined token dashboard script execution (rtk-stats.sh)
# ──────────────────────────────────────────────────────────────────────────────

set -uo pipefail

# ANSI styling
BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
CYAN="\033[36m"
RESET="\033[0m"

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

pass() {
  echo -e "  ${GREEN}✓ PASS${RESET}  $1"
  ((PASS_COUNT++))
}

warn() {
  echo -e "  ${YELLOW}⚠ WARN${RESET}  $1"
  ((WARN_COUNT++))
}

fail() {
  echo -e "  ${RED}✗ FAIL${RESET}  $1"
  ((FAIL_COUNT++))
}

header() {
  echo -e "\n${BOLD}${BLUE}═══ $1 ═══${RESET}"
}

header "1. Shell Configuration & ~/.zshrc"

# Check syntax
if zsh -n "$HOME/.zshrc" 2>/dev/null; then
  pass "~/.zshrc syntax is valid"
else
  fail "~/.zshrc contains syntax errors"
fi

# Check env vars in zshrc
if grep -q "HEADROOM_CODE_AWARE_ENABLED=1" "$HOME/.zshrc"; then
  pass "HEADROOM_CODE_AWARE_ENABLED=1 is exported in ~/.zshrc"
else
  warn "HEADROOM_CODE_AWARE_ENABLED=1 is missing from ~/.zshrc"
fi

if grep -q "HEADROOM_OUTPUT_SHAPER=1" "$HOME/.zshrc"; then
  pass "HEADROOM_OUTPUT_SHAPER=1 is exported in ~/.zshrc"
else
  warn "HEADROOM_OUTPUT_SHAPER=1 is missing from ~/.zshrc"
fi

# Check shell functions defined after sourcing ~/.zshrc in subshell
for fn in hpi hroom hlrn hproxy hproxyt hcodex hagy hverify; do
  if zsh -c "source \$HOME/.zshrc && typeset -f $fn" >/dev/null 2>&1; then
    pass "Function '$fn' is properly defined in ~/.zshrc"
  else
    fail "Function '$fn' is NOT defined in ~/.zshrc"
  fi
done

header "2. Scripts & File Permissions"

SCRIPTS_DIR="$HOME/ws/Learnings/Scripts/headroom"
for script in hpi.sh hroom.sh hlrn.sh hproxy.sh hcodex.sh hagy.sh verify-setup.sh rtk-agy-hook.py rtk-stats.sh headroom-env.sh; do
  file_path="$SCRIPTS_DIR/$script"
  if [[ ! -f "$file_path" ]]; then
    fail "$file_path does not exist"
  elif [[ ! -x "$file_path" ]]; then
    fail "$file_path exists but is NOT executable (chmod +x needed)"
  else
    pass "$script exists and is executable"
  fi
done

header "3. RTK (Rust Token Killer) Integrity"

if command -v rtk >/dev/null 2>&1; then
  RTK_PATH=$(which rtk)
  RTK_VER=$(rtk --version 2>&1 | awk '{print $2}')
  if [[ "$RTK_VER" == "0.49.0" ]]; then
    pass "RTK version is current: $RTK_VER ($RTK_PATH)"
  else
    warn "RTK version is $RTK_VER (expected 0.49.0) at $RTK_PATH"
  fi

  # Check Homebrew binary vs local bin
  if [[ -f "/opt/homebrew/bin/rtk" ]]; then
    BREW_VER=$(/opt/homebrew/bin/rtk --version 2>&1 | awk '{print $2}')
    if [[ "$RTK_VER" == "$BREW_VER" ]]; then
      pass "Homebrew rtk ($BREW_VER) matches active rtk ($RTK_VER)"
    else
      warn "Homebrew rtk ($BREW_VER) diverges from active rtk ($RTK_VER)"
    fi
  fi

  # Test rewrite capability
  REWRITE_TEST=$(rtk rewrite "git status" 2>/dev/null || true)
  if [[ "$REWRITE_TEST" == "rtk git status" ]]; then
    pass "RTK rewrite engine works ('git status' -> '$REWRITE_TEST')"
  else
    fail "RTK rewrite engine failed (got: '$REWRITE_TEST')"
  fi
else
  fail "rtk binary not found in PATH"
fi

header "4. Codex Profile Isolation"

CODEX_DEFAULT="$HOME/.codex/config.toml"
CODEX_HEADROOM="$HOME/.codex/headroom.config.toml"

if [[ -f "$CODEX_DEFAULT" ]]; then
  if grep -E "127\.0\.0\.1|localhost" "$CODEX_DEFAULT" >/dev/null 2>&1; then
    fail "Default $CODEX_DEFAULT contains localhost proxy! Plain 'codex' is hijacked."
  else
    pass "Default $CODEX_DEFAULT is clean (plain 'codex' routes direct to OpenAI)"
  fi
else
  warn "$CODEX_DEFAULT not found"
fi

if [[ -f "$CODEX_HEADROOM" ]]; then
  if grep -q "127.0.0.1:8787" "$CODEX_HEADROOM"; then
    pass "Isolated $CODEX_HEADROOM exists and routes to :8787"
  else
    warn "$CODEX_HEADROOM exists but does not point to :8787"
  fi
else
  fail "$CODEX_HEADROOM is missing"
fi

# Smoke test hcodex wrapper
HCODEX_OUT=$("$SCRIPTS_DIR/hcodex.sh" --version 2>/dev/null || true)
if echo "$HCODEX_OUT" | grep -q "codex-cli"; then
  pass "hcodex launcher successfully executes (codex-cli detected)"
else
  warn "hcodex launcher execution test did not detect codex-cli"
fi

header "5. Antigravity CLI (agy) Hooks & MCP"

HOOKS_FILE="$HOME/.agents/hooks.json"
if [[ -f "$HOOKS_FILE" ]]; then
  if python3 -c "import json; d=json.load(open('$HOOKS_FILE')); assert 'rtk-filter' in d" 2>/dev/null; then
    pass "~/.agents/hooks.json is valid JSON with 'rtk-filter' registered"
  else
    fail "~/.agents/hooks.json is invalid JSON or missing 'rtk-filter'"
  fi
else
  fail "~/.agents/hooks.json does not exist"
fi

# Test hook rewrite
TEST_PAYLOAD='{"toolCall": {"name": "run_command", "args": {"CommandLine": "git diff"}}}'
HOOK_RESP=$(echo "$TEST_PAYLOAD" | python3 "$SCRIPTS_DIR/rtk-agy-hook.py" 2>/dev/null || true)
if echo "$HOOK_RESP" | grep -q "rtk git diff"; then
  pass "rtk-agy-hook.py correctly rewrote 'git diff' to 'rtk git diff'"
else
  fail "rtk-agy-hook.py failed rewrite test (got: $HOOK_RESP)"
fi

# Check agy mcp list
if command -v agy >/dev/null 2>&1; then
  MCP_LIST=$(agy mcp list 2>/dev/null || true)
  if echo "$MCP_LIST" | grep -q "headroom"; then
    pass "Headroom MCP server is registered in agy"
  else
    warn "Headroom MCP server not found in 'agy mcp list'"
  fi
else
  warn "'agy' command not found in PATH"
fi

# Smoke test hagy wrapper
HAGY_OUT=$("$SCRIPTS_DIR/hagy.sh" --version 2>&1 || true)
if echo "$HAGY_OUT" | grep -Eq "Launching Antigravity CLI|[0-9]+\.[0-9]+\.[0-9]+"; then
  pass "hagy launcher successfully executes (agy $HAGY_OUT detected)"
else
  warn "hagy launcher test output unexpected: $HAGY_OUT"
fi

header "6. Unified Dashboard Health"

STATS_OUT=$("$SCRIPTS_DIR/rtk-stats.sh" 2>/dev/null || true)
if echo "$STATS_OUT" | grep -q "Token Savings Dashboard"; then
  pass "Unified rtk-stats.sh dashboard runs successfully"
else
  warn "rtk-stats.sh dashboard returned unexpected output"
fi

# Summary
echo -e "\n${BOLD}══════════════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}Verification Summary:${RESET}"
echo -e "  Passed:   ${GREEN}${PASS_COUNT}${RESET}"
echo -e "  Warnings: ${YELLOW}${WARN_COUNT}${RESET}"
echo -e "  Failures: ${RED}${FAIL_COUNT}${RESET}"
echo -e "${BOLD}══════════════════════════════════════════════════════════════${RESET}"

if (( FAIL_COUNT == 0 )); then
  echo -e "${GREEN}${BOLD}✓ All core integrations and shell configurations are healthy!${RESET}\n"
  exit 0
else
  echo -e "${RED}${BOLD}✗ Some checks failed. Please inspect the logs above.${RESET}\n"
  exit 1
fi
