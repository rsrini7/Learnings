# eMudhra: Eight Weak CA Keys and the PKI Trust Gap

**Daily learning · 22 October 2026 · Revalidated 31 October 2026 · Investigation ongoing**

> **Core idea:** Eight certificate-issuing keys were small enough to guess almost instantly. An attacker could use them to impersonate services to clients that still trusted the affected chains. Browsers received emergency blocks; other software needs its own trust updates.

## 1. First understand the chain: who trusts whom?

**eMudhra operates emSign, a certificate authority:** its public certificates help browsers and applications authenticate websites and services. Website operators obtain certificates; browsers, operating systems and applications decide which issuers to trust. A client can therefore be exposed even if neither its owner nor the website buys certificates from eMudhra. [Apple's incident explanation](https://support.apple.com/en-us/149555).

**HTTPS protects a connection, not a business's honesty.** It authenticates the requested hostname under the client's trust rules and protects traffic in transit. A phishing site can also use HTTPS for its own domain. Chrome replaced its lock with a settings-style icon partly because users mistook it for proof of website trustworthiness. [Chromium's explanation](https://blog.chromium.org/2023/05/an-update-on-lock-icon.html).

| Term | Simple meaning |
|---|---|
| Certificate | A signed statement linking an identity, such as a domain, to a public key. It is public. |
| Private key | The secret used to create signatures. A certificate does **not** contain it. |
| Root CA | A trust anchor accepted by a browser, operating system or application. |
| Intermediate CA | A delegated issuer that signs other certificates. |
| Leaf certificate | The end certificate used by a website, API or software publisher. |
| Trust store | The client's collection of accepted trust anchors. |

```mermaid
flowchart TD
    R["Trusted root CA"] -->|Signs| I["Intermediate CA certificate"]
    I -->|Signs| L["Leaf certificate for an API or website"]
    C["Client's trust store"] -.->|Accepts root| R
    L --> V["Client validates chain, identity,<br/>dates, constraints and applicable policy"]
```

The root's self-signature does not create trust: **the client chooses to trust it**. An intermediate can issue only within the constraints the verifier enforces. The arrows show certificate issuance, not network traffic. [X.509 validation: RFC 5280, §6](https://www.rfc-editor.org/rfc/rfc5280.html#section-6).

During a normal TLS handshake, the server sends its leaf certificate and usually the intermediates needed to build a chain; it can omit the root already trusted by the client. There can be multiple intermediates. Separating issuing keys from the root lets operators limit routine use of the root private key. Root **certificates** are public; their private signing keys require protection. [TLS certificate lists](https://www.rfc-editor.org/rfc/rfc8446.html#section-4.4.2), [X.509 certification paths](https://www.rfc-editor.org/rfc/rfc5280.html#section-6).

Architecture reference supplied with this review: [The SSL Store's three-tier PKI diagram](https://www.thesslstore.com/blog/wp-content/uploads/2021/12/3-tier-ca-pki-architecture-diagram-843x1024.png). The simplified diagram above focuses on the trust path relevant to this incident.

## 2. What actually broke? A large key format hid a tiny secret

The affected keys used **P-384**, but their private values were:

**`4 · 56 · 66 · 115 · 155 · 156 · 230 · 237`**

Scott Helme independently recovered all eight from public certificates on his laptop in under a second. This was a weak-key-generation failure: stealing secrets from eMudhra's servers was unnecessary. [Helme's recovery and demonstration](https://scotthelme.co.uk/eight-bits-of-trust-emudhras-ca-keys-cracked-in-milliseconds/).

The underlying relationship is:

**Public key `Q = d × G`**, where `d` is the private integer and `G` is a known curve point.

Normally, recovering a properly generated `d` from `Q` is infeasible. If `d` is one of **1–255**, a researcher can calculate each candidate's public key and compare it with the certificate. Zero is not a valid private scalar. This explanation follows [SEC 1: Elliptic Curve Cryptography, §3.2.1](https://www.secg.org/sec1-v2.pdf).

| Misleading intuition | Correct interpretation |
|---|---|
| “P-384 was broken.” | The implementation selected tiny secrets; the curve was not cryptanalytically broken. |
| “A 48-byte key must be strong.” | These integers fit in one byte; a 48-byte scalar encoding merely adds 47 leading zero bytes. |
| “384-bit key means 384-bit security.” | Key size, entropy and attack cost are different quantities. |

Padding changes representation, not unpredictability. The byte explanation follows [EC private-key encoding: RFC 5915, §3](https://www.rfc-editor.org/rfc/rfc5915.html#section-3).

### Reported cause: the wrong keys survived the ceremony

```mermaid
flowchart LR
    A["Key-generation ceremony"] --> B["Intended strong keys"]
    B --> C["Wrap, unwrap and re-import rehearsal<br/>produces weak key objects"]
    C --> D["Script specifies re-imported<br/>objects for CSR creation"]
    D --> E["CSRs use weak public keys"]
    E --> F["eMudhra certifies keys;<br/>Sectigo also cross-certifies them"]
```

This is **eMudhra's revised account**, not a completed forensic finding. A CSR is a certificate signing request; wrapping packages key material for transfer. Its response dated 28 October says a planned wrap/unwrap/re-import rehearsal left two same-label objects with different key material. The ceremony script specified creating CSRs from the re-imported objects. This **revises the earlier similar-label operator-selection explanation**. The exact mechanism that reduced the secrets to single-byte values remains unresolved. [Revised response, Q7 and Q9](https://bugzilla.mozilla.org/attachment.cgi?id=9670867), [public discussion](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449#c62).

The company dates the ceremony to **30 April 2025**, using FIPS 140-2 Level 3 HSMs, and says the detailed root cause remains under investigation. Hardware certification did not establish that the entire workflow selected secure keys. [eMudhra's 21 October statement](https://emudhra.com/investor-assets/investors/esg-profile/fy2027/statement-on-distrust-of-global-tls-intermediate-and-root-ca.pdf).

**A missed warning:** eMudhra also reported that earlier revocation lists were signed with the intended strong keys and failed verification against the published intermediates. Operators re-signed them using the weak keys. The mismatch should have triggered investigation of which keys had actually been certified. [Incident record, comment 11](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449#c11).

## 3. What could an attacker do—and what else was required?

The eight keys covered **six TLS intermediates and two code-signing intermediates**. Chrome's verifier excludes the code-signing-only chains from TLS use. [Chrome Root Program's technical response](https://groups.google.com/a/mozilla.org/g/dev-security-policy/c/0R3XLJL6FuE/m/ra8uYR6tAgAJ).

```mermaid
flowchart TD
    A["Recover weak TLS CA private key"] --> B["Sign a forged certificate<br/>for the target domain"]
    B --> C{"Can attacker intercept or<br/>redirect the client's connection?"}
    C -->|No| D["Certificate alone does not intercept traffic"]
    C -->|Yes| E{"Does this client still<br/>accept the forged chain?"}
    E -->|No| F["Connection rejected"]
    E -->|Yes| G["Attacker impersonates service;<br/>can read or alter this connection"]
```

This is a conceptual attack path. Mozilla confirms the need to intercept a connection and the potential for reading or changing its traffic. [Mozilla's security notice](https://blog.mozilla.org/security/2026/10/20/protecting-firefox-users-following-the-compromise-of-emudhra-intermediate-certificates/).

| Question | Precise answer |
|---|---|
| Only eMudhra customers at risk? | No. A client trusting the affected TLS chain could accept a forged certificate for an unrelated domain. |
| Did Helme compromise Stripe? | No. He demonstrated a locally forged certificate for its API hostname being accepted by tested clients. |
| Does a code signature make malware safe? | No. A forged signing chain can undermine publisher authentication where accepted; execution controls remain separate. |
| Can these keys decrypt every old HTTPS recording? | No. A CA signing key is not a session key. Properly established forward-secret TLS sessions are not retroactively decrypted by this compromise alone. |

Sources: [Helme's local proof](https://scotthelme.co.uk/eight-bits-of-trust-emudhras-ca-keys-cracked-in-milliseconds/), [CERT-In's impact advisory](https://www.cert-in.org.in/s2cMainServlet?CACODE=CICA-2026-3649&pageid=PUBADV01), [TLS 1.3 forward secrecy](https://www.rfc-editor.org/rfc/rfc8446.html#appendix-E.1).

**Signing is one layer:** Windows SmartScreen also checks downloaded-app reputation. macOS Gatekeeper uses Apple's Developer ID and notarization requirements; an eMudhra-issued signing chain does not substitute for them. These controls are not a blanket guarantee against malicious software. [Microsoft's reputation checks](https://learn.microsoft.com/windows/apps/package-and-deploy/smartscreen-reputation), [Apple's Developer ID requirements](https://developer.apple.com/developer-id/).

## 4. Timeline: emergency block first, broader distrust later

Times are **UTC**; October dates are **2026**.

| When | Event |
|---|---|
| 30 Apr 2025 | Affected key-generation ceremony: roughly 17½ months before discovery. |
| Oct 17, 18:05 | Chrome receives the researcher's report. |
| Oct 17, 19:45 | Chrome lands a CRLSet block for the six TLS keys, including cross-certificates sharing those keys. |
| Oct 17, 20:06 → 22:59 | Mozilla receives the report → completes Firefox OneCRL distribution. |
| Oct 18–20 | CA revocations and additional platform protections follow. |
| Oct 19, ~22:00 | Android receives equivalent blocks through **Google Play Services**, without requiring a full OS firmware update. |
| Oct 20 | Mozilla announces Firefox fixes and an NSS root-store update. |
| Oct 27, morning PDT—announced rollout date | Google's target for broad release of the **emSign ECC Root CA – G3** removal. This date has passed; deployment on a particular client still needs verification. |
| Oct 28 | eMudhra describes temporary G1 issuance during customer migration; the incident researcher reports remaining macOS developer-tool exposure. |
| Oct 30 | eMudhra appoints KPMG as an independent external reviewer. |

Sources: [Google's response and rollout schedule](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/), [Mozilla's notice](https://blog.mozilla.org/security/2026/10/20/protecting-firefox-users-following-the-compromise-of-emudhra-intermediate-certificates/), [incident record](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449).

**Blocking a key and removing a root are different actions.** Key blocking can reject every certificate using that key, including alternate cross-signed paths. Root removal affects other legitimate chains too; it does not establish that the root's private key was recovered. Google warns operators under this root to migrate certificates before rollout. [Google's migration warning](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/).

**31 October check:** Chromium's current root-store source is version **43** and excludes this G3 root. That confirms the published store change; it does not prove every installed client has received it. [Chromium's root-store source](https://chromium.googlesource.com/chromium/src/+/main/net/data/ssl/chrome_root_store/root_store.textproto).

**Exit means a transition, not an immediate shutdown:** the board approved withdrawal from global SSL/TLS on 22 October. On 28 October, eMudhra said G1 issuance would continue temporarily for a US customer ecosystem while it moves to other providers. The broader G3 root distrust also affects legitimate certificates outside the eight weak issuers. KPMG's appointment on 30 October begins an external review; it is not a published final root-cause finding. [Exit announcement](https://emudhra.com/en/press-release/emudhra-to-exit-global-ssl-tls-certificate-business), [company updates 6–7](https://emudhra.com/en/post/certificate-security-incident).

## 5. The gap: your browser's protection does not update your application

| Layer | What must reach the running client? |
|---|---|
| Chrome / Firefox | Vendor emergency blocks; custom settings or stale clients can affect delivery. |
| OS-based applications | Updated platform trust decisions, actually used by the application. |
| Bundled runtimes and libraries | Their own trust-bundle or verification updates. |
| Containers / embedded devices | Updated image or firmware, followed by deployment and any necessary restart. |

Many non-browser clients do not consume revocation information or enforce Certificate Transparency (CT). A valid signature and an unexpired certificate can therefore remain acceptable after a CA publishes a revocation. Behavior depends on the client, TLS backend and configuration. [Incident checker and downstream guidance](https://emudhra.we-have-a-problem.com/).

**A runtime has its own update lifecycle.** Node.js's bundled Mozilla CA store is a snapshot fixed at release time; updating Firefox does not update it. System-store options and custom CA configuration can change what a Node process actually trusts. Use a patched runtime and test the application's configuration. [Node.js trust-store documentation](https://nodejs.org/api/tls.html#tlsrootcertificates).

Node.js shipped fixes on 21 October in **22.23.4, 24.22.1 and 26.12.1**: use those or newer supported releases. The fix includes explicit rejection of chains containing blocked public keys as well as a root-store update. Rebuild images and restart processes; updating npm dependencies alone does not update the runtime. [Official security announcement](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases), [release details](https://github.com/nodejs/node/releases/tag/v26.12.1).

**Modern hardware is not proof of protection.** Apple confirms that some bundled command-line tools, including `curl` and `git`, use `/etc/ssl/cert.pem` rather than its framework-level blocks. Its guidance warns that OS updates can replace manual edits. Jackson's 28 October report describes that regression after macOS 27.2. Re-test developer workstations and CI runners after updates. [Apple's guidance](https://support.apple.com/en-us/149555), [researcher's macOS findings](https://emudhra.we-have-a-problem.com/apple.html).

**Cross-signing matters:** the same intermediate public key can have certificates from different parents. Removing only the eMudhra root may leave a Sectigo-backed path accepted. Merely deleting a cached intermediate is insufficient if a peer can supply it again. The remediation must reject the affected keys or eliminate **every accepted path**. This is an engineering inference from [Google's SPKI block](https://groups.google.com/a/mozilla.org/g/dev-security-policy/c/0R3XLJL6FuE/m/ra8uYR6tAgAJ) and [X.509 path validation](https://www.rfc-editor.org/rfc/rfc5280.html#section-6).

### Does expiry eventually end the risk?

| Certificate | Encoded expiry, UTC |
|---|---|
| Eight native eMudhra weak-key intermediates | **28 Apr 2040, 18:30:00** |
| Their Sectigo cross-signed copies | **31 Dec 2028, 23:59:59** |
| Sectigo's AAA Certificate Services root | **31 Dec 2028, 23:59:59** |
| emSign ECC Root CA – G3 trust anchor | **18 Feb 2043, 18:30:00** |

Sources: [intermediate certificates and metadata](https://emudhra.we-have-a-problem.com/impacted-intermediates.json), [root certificates and metadata](https://emudhra.we-have-a-problem.com/roots.json).

An expiry date belongs to a **certificate**, not the mathematical private key. Correct validation rejects an expired intermediate on that path, but trust-anchor expiry handling is implementation-dependent. These dates describe existing certificates, not a universal safety deadline. Patch now; old-device exposure depends on its accepted chains, clock and verifier, rather than device age alone. [X.509 trust-anchor and path-validation rules](https://www.rfc-editor.org/rfc/rfc5280.html#section-6.1).

### Was it exploited?

Google found no TLS certificates under the six intermediates in CT before its block: default CT-enforcing Chrome clients could not have accepted such forged certificates. Cloudflare reported no identified active exploitation **on its services**. Neither observation proves that all non-CT clients were safe. [Google's CT assessment](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/), [Cloudflare's assessment](https://blog.cloudflare.com/emudhra-certificate-compromise/).

## 6. Practical response: update, activate, verify

1. **Inventory actual verifiers.** Include outbound API clients, CI runners, proxies, runtimes and container images—not just public web servers.
2. **Apply vendor distrust fixes.** Update OS stores and separately bundled trust data, such as Python `certifi` or Rust `webpki-roots`, where used. Installing an update helps only if it contains the relevant fix.
3. **Activate the updates.** Rebuild and redeploy images; reload or restart processes that retain trust data. Check custom stores separately.
4. **Migrate affected server chains.** Replace legitimate certificates dependent on the removed root with an unaffected trusted hierarchy.
5. **Verify with the deployed client.** Use the [incident checker](https://emudhra.we-have-a-problem.com/), including both direct and cross-signed chains. Successful HTTPS to a compromised-chain test endpoint indicates residual trust; a certificate rejection is expected. A timeout or DNS failure is inconclusive, and one rejected chain does not establish full coverage.
6. **Keep verification enabled.** Resolve certificate failures; do not bypass them with `--insecure`, `-k` or disabled certificate validation.

For Cloudflare users: update One/WARP clients to the fixed versions in its advisory, and `cloudflared` to **2026.10.2 or later**. Review custom origin and mTLS trust configurations. Cloudflare documents separate updates for shared stores, bundled stores, base images and running services. [Cloudflare's remediation instructions](https://blog.cloudflare.com/emudhra-certificate-compromise/).

The deployment checklist above synthesizes that guidance with the [downstream remediation tracker](https://emudhra.we-have-a-problem.com/). mTLS exposure depends on which CAs the service accepts; a private-only client trust store does not automatically trust public WebPKI issuers.

### Tools: check the verifier you actually run

The open-source [incident checker](https://github.com/galadran/we-have-a-problem.com) publishes affected-certificate metadata and offline test chains. Its [hosted checks](https://emudhra.we-have-a-problem.com/) cover direct, cross-signed and unlogged (**No CT**) chains. Start with these read-only requests from the environment being assessed:

```bash
curl https://dv-g3b-noct-emudhra.we-have-a-problem.com/
curl https://dv-g3b-aaa-noct-emudhra.we-have-a-problem.com/
git ls-remote https://git-emudhra.we-have-a-problem.com/check.git
```

A successful curl connection exposes both residual trust and lack of CT enforcement for that chain. Git listing a commit demonstrates residual trust in its own verifier. Certificate rejection is expected; network failures are inconclusive. A TLS-inspecting proxy makes the result reflect the proxy's trust decision. These examples sample paths; use the full checker or offline chain set for coverage. [Checker instructions](https://emudhra.we-have-a-problem.com/), [Git test instructions](https://emudhra.we-have-a-problem.com/apple.html).

For retrospective investigation, search **recorded peer chains** with the regular expression `EM (DV|OV|EV) TLS CA - G3[BC]`; compare certificate and SPKI fingerprints with the [affected-certificate dataset](https://emudhra.we-have-a-problem.com/impacted-intermediates.json). Inspect a saved PEM certificate with:

```bash
openssl x509 -in peer.pem -noout -subject -issuer -dates -fingerprint -sha256
```

[OpenSSL](https://docs.openssl.org/3.5/man1/openssl-x509/) prints identity, validity and a certificate fingerprint; it does not establish whether an attack happened. Names are search leads, not unique identifiers. A matching fingerprint identifies a certificate, while a changed fingerprint can reflect another certificate using the same compromised key. Missing peer-chain logs cannot establish non-exploitation. Ordinary HTTP access logs may not contain this evidence.

**Legacy Firefox caveat:** Mozilla identified delayed OneCRL initialization on ESR 115 and marked its repair verified on 30 October. Treat an old ESR installation separately from current Firefox and check the running build; a source fix alone does not prove a client received it. [Mozilla's ESR 115 follow-up](https://bugzilla.mozilla.org/show_bug.cgi?id=2086788).

## 7. What this incident teaches

**Engineering conclusions:** validate the key-generation workflow as a whole; use unambiguous key identities and independently check the public key selected for each CSR. Reject known weak-key patterns, while recognizing that a small-number scan cannot prove good randomness. Design trust updates to reach running applications, and test alternate chains.

eMudhra says its infrastructure and data were not breached, Indian DSC/eSign services run separately, and global TLS represents around 1% of revenue. These are company statements; they do not reduce the authentication risk for clients trusting the weak keys. [Company filing](https://emudhra.com/investor-assets/investors/esg-profile/fy2027/statement-on-distrust-of-global-tls-intermediate-and-root-ca.pdf). [CERT-In](https://www.cert-in.org.in/s2cMainServlet?CACODE=CICA-2026-3649&pageid=PUBADV01) also distinguishes the unaffected domestic services.

### Source context

Based on user-provided details, with material claims checked against primary disclosures. The [additional explainer](https://www.youtube.com/watch?v=ybUXY-c33i4) prompted this 31 October revalidation. Current status follows the company updates, browser/platform guidance and incident research linked above.

---

**Related:**
- [Linux Kernel ZDI Public Reports](Linux-Kernel-ZDI-Public-Reports-KSMBD-Oct-2026.md) — Another October disclosure with distinct affected components and mitigation.
- [PHP2Shell: History, UAF and ASLR](PHP2Shell-History-UAF-And-ASLR-Oct-2026.md) — Compare a serious primitive with the additional conditions needed for exploitation.
- [LiteLLM 1.107.0 Supply-Chain Compromise](LiteLLM-1.107.0-Supply-Chain-Compromise-Oct-2026.md) — LiteLLM delayed a release while removing this CA from its trust store, showing the downstream operational impact.
- [Notepad++ Targeted Attack](Notepad++-Targetted-Attach.md) — Compare software-update authenticity and failures in trusted delivery paths.
- [Wireless Devices and Apps](Security-Vulnerabilities-in-Wireless-Devices-and-Apps.md) — Compare certificate validation and implementation failures across client devices.
