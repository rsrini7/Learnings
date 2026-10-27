# PHP2Shell and the Steal My Bitcoin Challenge

**Daily learning · 27 October 2026 · Challenge and solver accounts cross-checked**

> **Core idea:** A public challenge using unpatched PHP 8.4.26 was solved after its operator exposed a real PHP script. The result demonstrates code execution on that particular nginx-to-PHP CLI-server setup. Its long initial timer and later solve say little about the reliability of attacks against other PHP applications.

## 1. Foundations: the target and the bug

| Term | Meaning here |
|---|---|
| PHP SAPI | The interface by which PHP serves requests, such as FPM, Apache `mod_php`, or the built-in CLI web server. |
| `php -S` | PHP's built-in development server. An image tagged `fpm` can still run this server if its command starts `php -S`. |
| Worker | A process that handles requests; the exploit needs an out-of-memory request and later use of stale state in a reused worker. |
| WIF | Wallet Import Format, an encoding of a Bitcoin private key. A valid WIF does not by itself prove control of a particular funded address. |

The [challenge operator's released source](https://github.com/pavja2/smbc-source-oct-2026) shows nginx proxying to **`php -S`** with eight workers, serving PHP 8.4.26 in a container. The `php:8.4.26-fpm-alpine` base-image name did **not** make the live request path PHP-FPM. The image and helper arrangement let a PHP process execute a restricted `print-flag` binary to retrieve the challenge secret. PHP's own [manual](https://www.php.net/manual/en/features.commandline.webserver.php) calls this server a development tool, not a production web server. That limits how far this challenge can represent typical FPM or `mod_php` deployments.

The exploit concerns PHP's request-memory handling and session upload progress. Official [PHP release guidance](https://www.php.net/archive/2026.php#2026-10-21-1) identifies **CVE-2026-109618** (out-of-memory corruption) and **CVE-2026-109619** (stale global state), fixed in PHP 8.4.27 and corresponding maintained branches. The challenge intentionally used the prior 8.4.26 release.

## 2. Timeline: when was there a reachable PHP script?

All times below are **UTC on 25 October 2026** unless otherwise stated.

| When | Observed or first-person account | What it means |
|---|---|---|
| **24 Oct** | The [operator launched the challenge](https://news.ycombinator.com/item?id=50224916) with an initially roughly $500 prize; others added funds. | A running unpatched PHP binary alone did not establish that the intended exploit path was reachable. |
| **Before ~13:00** | The [operator says](https://news.ycombinator.com/item?id=50224916) the server was serving only `index.html` through PHP's web server. LiveOverflow's [first-person investigation in the same thread](https://news.ycombinator.com/item?id=50224916) concluded that the intended PHP-script path could not be reached then. | A static response and a PHP server header were insufficient to trigger this reported chain. The operator did not rule out every theoretical bug in the HTTP server itself. |
| **~13:00** | The operator [added `php-version.php`](https://news.ycombinator.com/item?id=50224916), an executable PHP page, while the server was under heavy traffic. | This provided a PHP request path for the challenge-specific exploit. The operator gave an approximate time, not a timestamped deployment record. |
| **15:47:38** | The [solver's preserved run summary](https://github.com/KillaBoi/StealMyBitcoin-PoC) records a response containing a checksum-valid WIF after leak and final-request stages. | Roughly **2 hours 47 minutes after the operator's approximate change**, rather than the full public challenge duration. |
| **After the run** | The [operator reported](https://news.ycombinator.com/item?id=50224916) that his logs showed the first and only successful `print-flag` execution and exfiltration. He acknowledged putting the wrong wallet-branch WIF on the server and said he transferred the prize to the solver. | The wrong WIF did not control the advertised funded address; the award followed the operator's validation of the server compromise. |

The video's “about two hours” is an approximation. The best first-person timing available here is **about 13:00** for the page addition and **15:47:38** for the solver's run. The public timer measures the whole challenge and should not be read as time spent exploiting a reachable PHP script.

## 3. What the solver demonstrated

The solver's [first-person write-up and PoC](https://github.com/KillaBoi/StealMyBitcoin-PoC) describe a three-stage chain: a session-upload-progress memory-limit condition; leak responses that exposed a heap address and PHP code address through cookies; and a final forged PHP structure that led cleanup to call PHP's `system` handler. The live run returned a WIF through the HTTP connection. The operator's own report of a matching `print-flag` execution strengthens the code-execution conclusion. [Solver account](https://github.com/KillaBoi/StealMyBitcoin-PoC), [operator confirmation](https://news.ycombinator.com/item?id=50224916).

This evidence has limits. The solver says the original live run did **not** retain complete outgoing HTTP bytes or response headers; later source and a local lab reconstruct the sequence. The published single-file PoC uses **up to 20 HTTP requests**, including leak batches, and its offsets are calibrated for an **Alpine PHP 8.4.26 CLI-server build**. The solver's local lab used **four workers**, while the operator's original kit used **eight**. In that quiet local lab, **7 of 10** consecutive runs verified execution. That small, controlled result does not measure success against busy production systems or other binaries. [Solver's evidence and lab results](https://github.com/KillaBoi/StealMyBitcoin-PoC), [operator's released source](https://github.com/pavja2/smbc-source-oct-2026).

The [user-shared LiveOverflow video](https://www.youtube.com/watch?v=VhNiMWtOutw) presents a separate **four-request design**, using two requests for a leak and two for command execution, plus last-byte synchronization and request fanout for timing. The supplied transcript says LiveOverflow demonstrated this on a later challenge-like endpoint and adjusted output delivery because outbound callbacks were blocked. It also says his own run did **not** solve the original prize challenge. These are his first-person experiments, not measurements of the solver's 20-request PoC or evidence of a universal exploit across PHP builds.

## 4. Claim check and practical lesson

| Claim | What the original accounts support |
|---|---|
| “Nobody could exploit PHP2Shell for almost a day.” | For much of the initial challenge period, this setup lacked a real PHP script. Heavy traffic and crashes also interfered with attempts. The timer cannot measure exploit difficulty by itself. |
| “An `fpm` Docker tag proves PHP-FPM was targeted.” | The operator's source starts `php -S`; the process command and SAPI determine the request path. |
| “The recovered WIF drained the displayed wallet.” | No. The operator placed a different wallet-branch WIF on the server, then transferred the prize after verifying execution. |
| “One successful challenge proves every PHP site can be exploited.” | No. It proves this vulnerable build and configuration were exploitable. Worker reuse, application path, binary layout and load affect a chain's success. |
| “A PHP version string is enough to select exploit offsets.” | No. The solver says another build reporting the same PHP version has a different binary layout; a leaked pointer and matching profile matter. |

For defenders, the challenge does not alter the [official update requirement](https://www.php.net/archive/2026.php#2026-10-21-1): install a fixed PHP build, ensure the web-serving workers restart on it, and verify the version and SAPI actually serving HTTP. Assess the separate [23 October session-upload-progress notice](https://www.php.net/archive/2026.php#2026-10-23-1) against the application's configuration. A challenge-specific static page is not a replacement for those fixes.

## 5. Source context

Based on the user-provided transcript of [LiveOverflow's video](https://www.youtube.com/watch?v=VhNiMWtOutw), cross-checked with the [challenge operator's source](https://github.com/pavja2/smbc-source-oct-2026), his [public updates](https://news.ycombinator.com/item?id=50224916), the [solver's write-up](https://github.com/KillaBoi/StealMyBitcoin-PoC), and [PHP's official advisory](https://www.php.net/archive/2026.php#2026-10-21-1). The live site was unavailable to the research reader, so the timeline rests on those first-person records rather than an independent server-log audit.

---

**Related:**
- [PHP2Shell: History, UAF and ASLR](PHP2Shell-History-UAF-And-ASLR-Oct-2026.md) — Original vulnerabilities, attack prerequisites, fixed releases and operational checks.
- [PHP2Shell Exploit Debate](PHP2Shell-Exploit-Debate-Threat-Models-And-Patch-Status-Oct-2026.md) — How to judge exploit demonstrations and avoid overgeneralizing from one setup.
- [PHP Migration Guide](../../Engineering/Architecture/PHP-Migration-Static-React-Java-And-Go-Oct-2026.md) — Broader PHP architecture decisions beyond this challenge.
- [Node.js Brotli Decoder](Node.js-Brotli-Node2Shell-RCE-Oct-2026.md) — Another runtime-level flaw whose exposure depends on a reachable application path.
