# Railway, Zeabur and the Hunt for AI Provider Keys

**Daily learning · 24 October 2026 · Primary-source review · Attribution unresolved**

> **Core idea:** Developer platforms are concentrated stores of long-lived cloud and AI credentials. Within eight days, Railway warned that some customer environment variables may have been decrypted, Zeabur disclosed a far larger read of its platform database, and OpenCode disclosed a Console breach. The common target was inference keys that bill the victim's account.

> **If you store secrets on a platform:** revoke them **at the provider**, not only in the platform. Rotating a platform integration or deleting a stored variable does not invalidate a copy an attacker already holds.

## 1. Three incidents, one credential class

| Platform | Dates | What is established | Scope and limits |
|---|---|---|---|
| **Railway** | 21 Oct 2026 | Unauthorised access to systems storing customer environment variables; some encrypted variables may have been decrypted. Deployments paused; all users advised to rotate secrets. | Railway says impact may be limited to a subset; no confirmed count or entry vector was published. |
| **Zeabur** | 14–15 Oct 2026, disclosed 19 Oct | Attacker used leaked internal credentials to read the platform database: 3,218,965 environment-variable records and 321,810 accounts; 865 database services were accessed. | Confirmed reads; some data “cannot be confirmed” and is treated as leaked. |
| **OpenCode** | 16–17 Oct 2026 | Console legacy system accessed; 1.4% of Console users with external providers linked were notified. | Separate incident, already reviewed in the linked note. |

Railway said it believes the activity is part of a series of attacks on platform companies **“with the aim of compromising AI inference providers”**, and that it asked upstream providers to revoke keys proactively. [Railway disclosure](https://blog.railway.com/p/security-disclosure-wednesday-october-21st). Zeabur's logs show the attacker searching for API keys, “especially keys for AI services”, reading n8n and new-api/one-api credentials at scale, and attempting to call Amazon Bedrock with Zeabur's AWS keys. [Zeabur incident report](https://zeabur.com/blogs/october-2026-security-incident).

The shared label **distillation** describes training a cheaper model on a larger model's outputs. Stolen inference credentials make someone else pay for those outputs. The reviewed disclosures establish credential theft and attacker intent; they do not establish a completed distillation dataset, a trained model, or one actor behind all three incidents.

## 2. Why platform environment variables are a high-value target

```mermaid
flowchart LR
    A["Customer stores<br/>provider key"] --> B["Platform database<br/>encrypted at rest"]
    B --> C["Platform runtime<br/>decrypts for use"]
    C --> D["Attacker gains platform<br/>or admin access"]
    D --> E["Reads variables<br/>or decrypted values"]
    E --> F["Calls provider directly<br/>with the stolen key"]
    F --> G["Usage billed to<br/>the key owner"]
```

Encryption at rest protects a stolen database backup only if the decryption keys remain separate and inaccessible. A platform that must decrypt customer secrets to run workloads creates a runtime path to plaintext. Zeabur's report describes plaintext long-lived admin credentials, an admin interface reachable from the public internet, and tokens that had not expired since January 2024. Railway's notice says some encrypted variables may have been decrypted, which implies access to the decryption path rather than only a database dump.

A second problem is **credential concentration**. One environment-variable store may hold a customer's OpenAI key, Anthropic key, cloud role, database password, and registry token. A single platform compromise therefore becomes many independent provider incidents.

## 3. What Zeabur's numbers add

Zeabur's preliminary report is unusually detailed and is the best public evidence for how far this class of incident can go:

- **3,218,965** environment-variable records and **321,810** accounts were read from the platform database.
- **11,536** platform access tokens (stored as hashes) were revoked; **566** zSend API keys stored in plaintext were revoked.
- The attacker ran commands inside **865** database services; the report separately lists **736** n8n PostgreSQL instances, **211** PostgreSQL databases, **10** new-api/one-api instances, **1** Redis, and **1** each MongoDB and MariaDB. Output was not always logged, so the exact data taken is uncertain.
- **101** GCP Dedicated Servers were accessed as root, and **50** had attacker-controlled SSH keys added.
- An OpenAI key stored by one user was used for about **1,107 image-generation requests**; Zeabur labels the link to this leak a hypothesis, not a confirmed source.
- The August incident's rotation did not cover the cluster admin tokens and AWS keys used in October. Zeabur says its earlier statement that “all internal admin keys have been disabled or rotated” was incomplete. [Zeabur report](https://zeabur.com/blogs/october-2026-security-incident).

Zeabur also announced it will shut down on **31 December 2026**, an operational decision separate from the security incident. [Zeabur shutdown notice](https://zeabur.com/blogs/zeabur-is-shutting-down).

## 4. Impact and limits

| Claim | What the evidence supports |
|---|---|
| “Only Railway customers are affected.” | No. Zeabur and OpenCode disclosed separate incidents; the common pattern is platform-held credentials, not one shared breach. |
| “Encrypted variables are safe.” | Not necessarily. Railway says some may have been decrypted; encryption at rest does not protect a runtime that can decrypt. |
| “Rotating the platform token fixes it.” | No. Revoke the upstream provider key at the provider; a copied bearer key remains valid otherwise. |
| “Every stolen key was used.” | Not established. Zeabur confirmed reads but not use for every key; Railway published no key-level accounting. |
| “All three are one campaign.” | Unproven. The timing and intent overlap, but no reviewed source attributes them to a single actor. |

## 5. Practical response

1. **Inventory where keys live.** Include platform environment variables, CI secrets, database rows, container images, and local `.env` files.
2. **Revoke at the issuer.** For each provider, delete or rotate the key in the provider console, then create a replacement. Check project scope: an OpenAI key may be project-scoped rather than organisation-wide.
3. **Rotate dependent secrets too.** Database passwords, registry credentials, SSH keys, and signing keys may sit in the same store. For Zeabur, changing a platform variable does not change the password inside the database.
4. **Reconcile usage.** Compare provider billing and request logs against your baseline from at least 14 October, preserving UTC timestamps and invoice IDs.
5. **Treat compromised hosts as rebuilds, not cleanups.** Zeabur recommends rebuilding affected GCP servers; for Railway, redeploy commits pushed during the deployment pause and recreate CLI/CI credentials. [Railway recovery guidance](https://blog.railway.com/p/security-disclosure-recommendation-recover-failing-deploys).
6. **Use short-lived, scoped credentials** where supported. A provider key that expires or is limited to one project bounds the value of a stolen copy.

---

**Related:**
- [OpenCode Console API-Key Breach](OpenCode-Console-API-Key-Breach-And-Distillation-Oct-2026.md) — The third platform incident in this cluster, with the credential-revocation boundary explained in depth.
- [LiteLLM 1.107.0 Supply-Chain Compromise](LiteLLM-1.107.0-Supply-Chain-Compromise-Oct-2026.md) — A package-based path to the same class of cloud and AI credentials.
- [Banks and Unvetted AI Agents](Banks-Third-Party-AI-Agents-Oct-2026.md) — Another case where possession of a user's credential is mistaken for authorised delegation.
- [OpenAI's Agents Disabled Their Own Monitoring](../../AI-ML/Agents/analysis/OpenAI-Agents-Disabled-Misalignment-Monitoring-Oct-2026.md) — Agent control failures that matter when agents can reach credentials and billing.
