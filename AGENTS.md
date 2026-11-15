# 🤖 Agents Guide (Repository Root)

> Read this first. It captures the rules that are easy to miss when adding or
> moving content in this repository.

---

## ⛔ The #1 Rule: `README.md` is auto-generated

**Do NOT hand-edit `README.md`.** It is regenerated from the directory structure
by `Scripts/generate-readme.py`. Any manual edits will be overwritten.

To change what appears in the README:

1. Add / move / rename the actual files.
2. If you introduced a **new folder/section**, register it in
   `Scripts/generate-readme.py` (add a `get_md_files(...)` block and, if
   relevant, a line in the structure diagram inside that script).
3. Regenerate:
   ```bash
   python3 Scripts/generate-readme.py
   ```
4. Verify links after any reorganization:
   ```bash
   python3 Scripts/github-repos.py links
   ```

---

## 📥 Adding a new note / article

1. Place the `.md` file in the most fitting category folder under
   `AI-ML/`, `Engineering/`, `Blockchain/`, `Papers/`, `News/`, etc.
   Create a new subfolder if none fits semantically.
2. **File naming convention:** Use **Title-Case-With-Hyphens** and append
   the **year** (and month if needed). Examples:
   - `Sarvam-AI-Deep-Review-2026.md`
   - `Google-Gemma-Family-Models-Jan-2026.md`
   - `Chinese-AI-Trifecta-2025-2026.md`
3. Put any linked images/SVGs/PDFs in the nearest `assets/` folder
   (e.g. `AI-ML/assets/` or `AI-ML/LLMs/assets/`) and reference them with a
   correct **relative** path.
   **Do NOT put images/SVGs alongside the `.md` file.**
   **Do NOT put images/SVGs in the root-level `assets/`** — always use the
   category-level `assets/` folder closest to the `.md` file.
   When relocating assets, use `git mv` to preserve history:
   ```bash
   git mv assets/image.png AI-ML/assets/image.png
   ```
3. **Add a `**Related:**` cross-reference section** to the new file, and add a
   back-link to it from the most relevant sibling docs (see next section).
4. Regenerate the README and run the link check (see above).
   The generator now **auto-discovers** subfolders, so a new folder will still
   appear (worst case under an "Uncategorized" section) — but add a curated
   title in `Scripts/generate-readme.py` for a clean section.

---

## 📝 Default structure for daily updates and deep reviews

For every new daily learning note, news update or deep review, use the structure
and readable depth demonstrated by these references unless the user requests
another format:
- [eMudhra: Weak CA Keys and PKI Trust](News/Security/EMudhra-Weak-CA-Keys-And-PKI-Trust-Oct-2026.md)
- [PHP2Shell: History, UAF and ASLR](News/Security/PHP2Shell-History-UAF-And-ASLR-Oct-2026.md)
- [Polymarket: Compromised Monitoring Script](News/Security/Polymarket-DebugBear-Supply-Chain-Attack-Oct-2026.md)
- [Java: Next-Gen Programming Models (Babylon & Panama)](Engineering/JVM/Java-Next-Gen-Programming-Models-Babylon-Panama-Nov-2026.md)
- [RFC 10008: HTTP QUERY Method](Engineering/Architecture/HTTP-QUERY-Method-RFC-10008-Nov-2026.md)

Read the relevant reference before drafting. Apply this pattern across topics;
adapt section names and scale depth to thoroughly explain the subject.

### Do NOT Trim Useful, Verified Information (Depth + Readability)

Restructuring is **NOT** an exercise in aggressive truncation or deleting technical depth. Its purpose is to eliminate unverified speculation, conversational filler, and broken formatting—while **amplifying verified technical mechanisms, concrete code implementations, production configurations, and practical takeaways**.

Keep the document deeply educational, engaging, and directly useful to practicing engineers:
- If an existing note has verified technical details, benchmark configurations, or architectural edge cases, **preserve and structure them** rather than discarding them.
- Always explain the "why" and "how" behind the physics, protocols, and memory structures.
- Strive for high reader value: an engineer reading the document should walk away with actionable code, architecture trade-offs, and failure mode awareness.

### Article structure

1. **Title, date, and author attribution:** a descriptive title, then `Daily learning · <date>` (for new daily notes) or `Learning note · Revised <date> · <qualifier>` (for restructured/revised deep reviews), followed by the author attribution line `*By Srinivasan Ragothaman ([@rsrini7](https://github.com/rsrini7))*`.
2. **Core idea:** a short blockquote explaining what happened and why it matters in one or two plain-language sentences.
3. **Foundations:** explain what each main product or organization does, why the parties are connected, and what normal use looks like. Add a familiar product comparison when it helps. Define essential terms before detailed mechanisms using a compact term/meaning or party/role table.
4. **Deep Technical Mechanism:** explain what changed, broke, or how the system operates under the hood, step by step. Distinguish underlying concepts from specific implementation details. Cover wire protocols, byte/memory layouts, CPU/cache interactions, and data structures where relevant.
5. **Architectural Visuals (SVGs & Mermaid):** Pair high-level custom architecture SVGs with focused in-line Mermaid sequence diagrams, state lifecycles, or decision trees.
6. **Production Implementations & Code Recipes:** Include concrete, runnable, idiomatic code examples across relevant ecosystems (e.g. Go, Java, Rust, Python, C++, SQL, Envoy, Nginx, Linux sysctl). Show realistic implementations with error handling, memory pooling, and boundaries—not trivial toy snippets.
7. **Impact, Real-World Edge Cases & Gotchas:** Explain prerequisites and practical failure modes (e.g. supernodes, cache stampedes, false sharing, WAF stripping, carrier thread pinning, network partitions). Use a **Common Claims vs. Technical Realities** table to debunk frequent industry misconceptions.
8. **Practical Adoption Blueprint & Verification Checklist:** Give concrete actions to benchmark, adopt, or verify. Include exact diagnostic commands (`ethtool`, `vmstat`, `wrk2`, `pg_stat_statements`, `jcmd`), test methodologies (open vs closed loops, coordinated omission), and measurable SLO criteria.
9. **Timeline and Current State:** include meaningful dates, fixes, and rollout milestones when they clarify the evolution.
10. **Primary Sources, References and Evidence:** Provide a dedicated `## Primary Sources & References` list containing curated, high-value external links (specifications, whitepapers, official repos, foundational articles, key conference presentations, and explainer videos) with descriptive titles and 1-line annotations. Pair this with a `## Source Context` or evidence table with dates and citations (RFCs, CVE advisories, GitHub PRs, academic papers). Attribute company claims and state observational limits.
11. **Supplementary Visuals (Keep Existing PNGs Intact):** Always retain existing valid repository diagrams/PNGs/GIFs in a dedicated `## Supplementary visuals` section with descriptive captions contextualizing how the revised text governs the technical claims.
12. **Related Cross-References:** End with the required `**Related:**` section containing 3–5 bidirectional relative links with clear, concise reasons.

### Curating External References & Primary Sources (No Blind Deletions)

- **Never discard valid, meaningful external links:** When an existing note contains `Ref:` links, author disclosures, arXiv papers, GitHub repositories, or conference/video explainers, do NOT blindly delete them.
- **Elevate and Format:** Transform unformatted links, bare URLs, or footnote dumps into a clean, annotated markdown reference list:
  ```markdown
  ## Primary Sources & References

  1. [Author / Organization: Document Title](https://...) — Concise 1-line annotation explaining what this source covers and why it matters.
  2. [GitHub: Org/Repo-Name](https://github.com/...) — Official open-source implementation, source code, and release notes.
  3. [Speaker / Conference: Presentation Title](https://...) — Primary talk or technical explainer introducing the core system architecture.
  ```
- **Filter Low-Signal Noise:** Omit broken URLs, social media spam/echoes, and tangential meme videos, but preserve the original foundational author posts, primary papers, and authoritative technical explainers.

### Editorial and verification standard

- Keep the writing simplified, concise and readable while preserving technical
  depth. Define jargon at first use; keep paragraphs short and sections numbered.
  Scale length to the topic rather than filling every section.
- Before delivery, check that a new reader can answer: "What is this?", "Why
  are these parties connected?", and "Who was affected?" Revise the opening if
  those answers require reading the technical mechanism first.
- **Diagrams and Visuals:**
  - **Mermaid:** Use Mermaid for in-line sequence diagrams, decision trees, lifecycles, and simple architectural flowcharts where native markdown rendering and git diffability are preferred.
    - **Avoid statement semicolons in sequence diagrams:** In `sequenceDiagram`, a semicolon (`;`) functions as a statement terminator. Never use semicolons in messages (e.g. use `and` or commas instead of `Write Step 1; Step 2`).
    - **Avoid edge delimiter collisions in flowcharts:** Edge labels in `flowchart` are enclosed in pipes `|...|`. Never use raw double vertical bars `||` inside edge labels (e.g., `-->|Score = softmax(-||v - μ||² / τ)|` breaks parsing). Quote the label `-->|"Score = exp(-dist² / τ)"|` or avoid raw `||` delimiters.
    - **Avoid nested colons in stateDiagram-v2 labels:** In `stateDiagram-v2`, `:` separates transition arrows from their labels (`StateA --> StateB: Label`). Colons inside the label (e.g., `StateA --> StateB: Shiva (:heal:) Fixes Code`) break the transition lexer.
    - **Prevent bidirectional label overlaps in state diagrams:** When two states in `stateDiagram-v2` have bidirectional transitions (`A --> B` and `B --> A`), Dagre centers both edge labels at the exact same midpoint $(x, y)$ coordinate, causing overlapping text. Prefer `flowchart TD` / `flowchart LR` with an explicit convergence/resume node (or subgraphs) so that return arrows follow distinct spatial trajectories.
    - **Quote special characters in node labels:** Node labels containing parentheses, brackets, or math symbols must be enclosed in double quotes (e.g., `id["Label (Extra Info)"]`). Avoid HTML tags in labels.
    - **Prevent subgraph title wrapping collisions:** Keep `subgraph` titles concise (<= 24 characters) and avoid `<br>` inside subgraph titles. Dagre allocates a fixed single-line (24px) header box; wrapped text overflows downward directly into the topmost child node.
    - **Avoid direct cluster-to-cluster edges:** Avoid edges directly between subgraph cluster IDs (e.g. `ClusterA --> ClusterB`), which causes Dagre to anchor the arrow directly across the cluster title label. Connect node-to-node across subgraphs instead.
  - **Custom Architecture SVGs:** For deep educational notes or complex multi-stage systems (e.g., end-to-end storage tiering, hardware memory layouts, side-by-side comparative flows, or multi-panel infographics), provide a dedicated SVG diagram. It is not mandatory for every note, but strongly recommended when visual richness enhances understanding.
    - Always store the `.svg` in the nearest category-level `assets/` folder (e.g. `AI-ML/LLMs/assets/<Name>.svg`) and reference it with a relative path (`![Title](../assets/<Name>.svg)`).
    - Keep SVGs dark-theme native (`#0b0f19` / `#111827` background, slate containers `#1e293b`, cyan `#38bdf8`, emerald `#4ade80`, amber `#fbbf24`, muted text `#94a3b8`) with a responsive `viewBox`.
    - **Strict XML validation:** All text nodes must escape ampersands as `&amp;` and angle brackets as `&lt;` / `&gt;`. Always validate SVG syntax before delivery (e.g., via `python3 -c "import xml.etree.ElementTree as ET; ET.parse('path/to.svg')"`).
    - **Text Boundary & Overflow Clamping:** Unlike HTML, SVG `<text>` elements **do not auto-wrap**. Furthermore, GitHub's image sanitizer and `camo` proxy strip `<foreignObject>` blocks for security reasons. Never write single uninterrupted text lines exceeding 55–60 characters inside standard card containers (~450–500px width at font-size 11–12px). Manually wrap sentences across multiple `<text>` lines with controlled vertical spacing (16–18px offsets).
    - **Automated SVG Verification:** Always validate diagrams using `python3 Scripts/check-svg.py path/to/diagram.svg` (or `python3 Scripts/check-markdown.py path/to/note.md`) to catch text boundary overflows, tight margins (<5px), text-on-text collisions, border straddles, connector piercing, empty bottom dead space, and invalid viewBox dimensions before delivery.
    - When helpful, pair the SVG (high-level visual infographic) with focused in-line Mermaid diagrams for specific sub-mechanisms (e.g. request sequence or attention projection).
- **LaTeX Math and KaTeX Rendering on GitHub:**
  - **Subscripts outside `\text{}`:** In KaTeX/LaTeX, `\text{...}` operates in text mode. An unescaped underscore `_` is illegal in text mode and throws the KaTeX error `'_' allowed only in math mode`. Move subscripts outside `\text{}` into math mode (e.g., write `\text{Score}_{\text{RRF}}(d)` instead of `\text{RRF_Score}(d)`).
  - **Flush-left display math (column 0, NO list indentation):** Never indent display math blocks (`$$...$$`) inside Markdown lists (`1.`, `2.`, `-`). When indented inside a list item, GitHub Flavored Markdown (GFM) parses `$$` as plain paragraph text inside the list rather than as a KaTeX display math block. The Markdown parser then interprets math subscript underscores `_` as Markdown *italics* syntax (`_italic_`), corrupting the equation and dumping raw unrendered LaTeX on screen. Always place display math blocks (`$$...$$`) at column 0 (flush-left) separated by blank lines before and after.
  - **Literal comparison operators (NO HTML entities inside math):** In KaTeX math expressions (`$...$` or `$$...$$`), never write HTML entities like `&lt;`, `&gt;`, `&le;`, `&ge;`, or `&amp;`. KaTeX interprets `&` as a tabular alignment separator and throws `ParseError: KaTeX parse error: Expected 'EOF', got '&'`. Always use literal `<` (or `\lt`), `>` (or `\gt`), `\le`, `\ge`, or `\&`. Run `python3 Scripts/check-markdown.py` (or `--fix`) to detect and auto-repair them.
- Use tables for genuine comparisons.
- **User-Provided Videos and Third-Party Media:**
  - **Never create a play-by-play video timeline or chapter recap:** When the user shares a video link (e.g. YouTube, conference talk, podcast), do NOT structure the document around the video chapters or produce a timestamped narrative breakdown.
  - **Treat video as preliminary context, not ground truth:** Videos are shared for conceptual orientation and high-level knowledge. Never treat video claims, benchmark numbers, or creator assertions as 100% valid or verified facts.
  - **Conduct rigorous independent research:** Always look past the video to locate primary sources—academic papers (e.g. arXiv), official technical documentation, standards, source code repositories, and empirical benchmarks. Base the article's structure, technical mechanisms, and numbers on primary literature.
  - **Omit video-specific narration by default:** Avoid video-centric framing (e.g. "In this video the creator shows...", "Chapter 4 covers..."). Explain the underlying technology, system architecture, and empirical findings directly. Only include video-specific commentary if the user explicitly requests details about the video itself.
- **User Feelings, Workplace Frustrations, and Organizational Anonymity:**
  - **Never transcribe personal venting or interpersonal friction literally:** When the user shares personal emotions, frustrations, workplace conflicts, or references to authority figures (e.g., "my manager said...", "my boss argued...", "leadership thinks..."), NEVER echo or reproduce these statements verbatim. Never include colloquial dialogue or subjective labels (e.g., "Addressing the manager's argument", "The user's manager believes", "Why leadership is wrong") in article titles, section headings, body prose, diagrams, SVGs, artifacts, or chat responses.
  - **Strictly anonymize employers and organizations:** If the user mentions their current employer, company name, workplace affiliations, or internal team identities, NEVER include or disclose those names. Abstract them into generic industry archetypes (e.g., "enterprise environments", "teams migrating legacy services", "large-scale transactional systems").
  - **Translate workplace debates into objective technical trade-offs:** Reframe subjective claims or interpersonal disputes into detached, professional engineering evaluations (e.g., "Architectural Evaluation: Shared-Nothing vs. Persistent Runtimes", "Structural Risks in Server-Side JavaScript", "Inherent Failure Modes in Legacy Frameworks"). Address the underlying technical mechanisms and trade-offs rigorously without attributing them to personal personalities.
  - **Universal application across all artifacts:** Enforce this abstraction across every output: Markdown documents, Mermaid diagrams, SVG text and containers, code comments, commit messages, and final user-facing responses.
- Verify material claims against current primary sources and cite them inline
  near the relevant explanation. Trace claims in user-provided details back to
  disclosures, official documentation, standards or first-person research.
- Attribute preliminary root causes and company statements. State uncertainties,
  scope evidence of non-exploitation to the observer, and distinguish a local
  demonstration from compromise of a real service. Describe provenance simply:
  for example, "Based on user-provided details, with material claims checked
  against primary disclosures." Name a video, transcript or other input format
  only when that provenance affects a claim or the user asks. Reserve verification
  claims for material actually checked; mention access limitations only when they
  affect a material conclusion or the user asks about verification.
- Keep unrelated concurrent incidents separate. Include business context only
  when it helps interpret the technical impact. Explain meaningful limitations
  without sensationalism or unsupported assurances.
- Before delivery, check factual consistency, source URLs, dates, diagram labels
  and internal links; complete the repository validation and commit rules below.

---

## 🔗 REQUIRED: Internal `**Related:**` cross-references (manual)

> There is **NO script** for this. It is authored manually (by a human or LLM)
> and is easy to forget. ~200 files already follow this convention — every new
> or moved `.md` file MUST participate.

Every content `.md` file should end with a Related section that links to a few
of the most relevant sibling docs, each with a short reason. Format (note the
inline entries on one line, matching existing files):

```markdown
---

**Related:**
- [Doc-Name](../relative/path/Doc-Name.md) — one-line reason this is related.
- [Another-Doc](../../path/Another-Doc.md) — why it connects to this topic.
```

Rules:
- Use **relative paths** from the current file's location (count the `../`).
- Add **3–5** genuinely relevant links with a concise `— reason` each.
- **Put each link on its own line** (a markdown list), with `**Related:**` on
  its own line above them — NOT all crammed onto one paragraph line.
  Correct:
  ```
  **Related:**
  - [Doc-Name](path.md) — reason.
  - [Other](path2.md) — reason.
  ```
  Wrong (paragraph, hard to read):
  ```
  **Related:**- [Doc-Name](path.md) — reason.- [Other](path2.md) — reason.
  ```
- Prefer making links **bidirectional**: when Doc A → Doc B, add Doc B → Doc A
  where it makes sense, so the reference web stays connected.
- Verify the paths resolve (`python3 Scripts/github-repos.py links`).

When **adding** a file: write its Related section AND add a back-link from the
closest existing doc(s).
When **moving/renaming** a file: fix its own Related paths (depth changed) AND
update any other files that linked to it.

---

## 🗂️ Moving / renaming files

1. **Always use `git mv`** (not plain `mv`) to move or rename files so Git
   tracks the rename and preserves history. Example:
   ```bash
   git mv old-path/File.md new-path/File.md
   ```
   Plain `mv` creates an untracked new file + a deletion, losing rename tracking.
2. Move the file and its linked assets.
3. Fix the relative image/link paths **inside** the moved file (the number of
   `../` changes with folder depth).
4. Fix the file's own `**Related:**` links and update any **other** files that
   referenced it (grep for the old filename).
5. Regenerate the README and run the link check.

---

## 📚 More detail

See [`Scripts/AGENTS.md`](Scripts/AGENTS.md) for full documentation of the
utility scripts (`github-repos.py`, `generate-readme.py`, link/TOC fixing,
GitHub repo management, and common workflows).

---

## Commit approval

After creating or editing files, complete validation and leave the changes
uncommitted for user review. **Do not commit without the user's explicit approval
after they have reviewed the changes.** Creating an `.md` file does not authorize
a commit.

## ⚠️ Quick Checklist

- [ ] Files named in **Title-Case-Year** format (e.g. `Sarvam-AI-Deep-Review-2026.md`)
- [ ] Files (and assets) placed in the right folder
- [ ] Moved/renamed files via `git mv` (not plain `mv`)
- [ ] Images/SVGs/PDFs in nearest `assets/` folder, **NOT** alongside the `.md` file
- [ ] **Do NOT put images/SVGs in the root-level `assets/`** — use category-level `assets/`
- [ ] User-provided videos treated as preliminary context (no chapter timelines, primary sources independently researched, no video-specific commentary unless requested)
- [ ] User feelings, workplace frustrations, manager quotes, and employer/organization names generalized and anonymized (no literal quotes of internal workplace dynamics or employer identities; framed objectively as generic architectural/engineering trade-offs)
- [ ] Existing valid PNGs/diagrams retained intact in `## Supplementary visuals` with explanatory captions
- [ ] Verified technical depth preserved (no aggressive truncation; includes concrete code recipes and real-world edge cases)
- [ ] SVGs validated for well-formed XML, container text overflows, text-on-text collisions, border straddles, connector piercing, and empty bottom dead space (`python3 Scripts/check-svg.py path/to.svg`)
- [ ] Mermaid diagrams checked for statement semicolons, edge delimiter collisions (`||`), nested colons, bidirectional label overlaps, subgraph title wrapping (<=24 chars), and cluster-to-cluster edges
- [ ] Math display blocks (`$$...$$`) placed flush-left (column 0, no list indentation) with subscripts outside `\text{}` (`\text{Score}_{\text{sub}}`) and literal comparison operators (no `&lt;` / `&gt;` entities)
- [ ] Relative links inside moved files fixed
- [ ] Relative image/asset paths fixed
- [ ] New `.md` file ends with a `**Related:**` section (3–5 links + reasons)
- [ ] Back-links added in the closest existing sibling doc(s)
- [ ] Moved/renamed file: own Related links fixed + old references updated
- [ ] `python3 Scripts/check-markdown.py path/to/file.md` (or `--recent`) clean
- [ ] `python3 Scripts/generate-readme.py` run (never hand-edit `README.md`)
- [ ] `python3 Scripts/github-repos.py links` clean
- [ ] Leave changes uncommitted for user review; commit only after explicit approval
