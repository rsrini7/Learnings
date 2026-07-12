# Notepad++ Attack key points

## Targeted Attack

The hack wasn't a mass exploitation but a very specific attack on a small group of individuals, involving manual "hands-on keyboard" operations by the threat actors.

## Update Infrastructure Vulnerability

The hackers exploited a vulnerability in how Notepad++ handles updates, specifically its updater called GUPP or Windg.

## Interception of Traffic

The issue involved intercepting traffic, potentially over HTTP and later even HTTPS, to redirect users to download a malicious version of Notepad++. This suggested a possible compromise of certificate authorities for HTTPS interception.

## Malicious Activities

Once compromised, the Notepad++ instance would spawn malicious processes, including running curl to upload files  and executing reconnaissance commands like netstat, systeminfo, tasklist, and whoami.

## DLL Sideloading

The attackers used a technique called DLL sideloading to load malicious code, blending it with legitimate processes . This led to the execution of encrypted shellcode for cyber network operations to steal data.

## Security Patch

A bug fix in Notepad++ version 8.8.8 was released to prevent the updater from being hijacked, forcing downloads from a specific domain.

## References

https://notepad-plus-plus.org/news/hijacked-incident-info-update/

**Related:**- [Security-Vulnerabilities-in-Wireless-Devices-and-Apps](Security-Vulnerabilities-in-Wireless-Devices-and-Apps.md) — Companion client-software supply-chain/hijack analysis from the same security-news window.- [OpenClaw(Moltbot-or-Clawdbot)-Security-Analysis-Jan-2026](../../AI-ML/Agents/openclaw/OpenClaw%28Moltbot-or-Clawdbot)-Security-Analysis-Jan-2026.md) — Both detail targeted, hands-on-keyboard attacks leveraging update/installer trust chains.- [MongoBleed-Dec2025](MongoBleed-Dec2025.md) — Sister write-up of a major late-2025 CVE that, like Notepad++, exposed long-known unpatched flaws.
