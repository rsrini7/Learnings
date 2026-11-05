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

Read the relevant reference before drafting. Apply this pattern across topics;
adapt section names and omit sections that do not help explain the subject.

### Article structure

1. **Title and date:** a descriptive title, then `Daily learning · <date>` with
   verification status or an investigation qualifier where relevant.
2. **Core idea:** a short blockquote explaining what happened and why it matters
   in one or two plain-language sentences.
3. **Foundations:** first explain in plain language what each main product or
   organization does, why the parties are connected, and what normal use looks
   like. Add a familiar product comparison when it helps, and state how the
   products differ. Then define essential terms before the detailed mechanism;
   use a compact term/meaning or party/role table when readers need one.
4. **Mechanism:** explain what changed or broke, step by step. Distinguish the
   underlying technology from its implementation, workflow or operational use.
5. **Impact and limits:** explain prerequisites and practical consequences;
   separate demonstrated results from possible outcomes. For incidents,
   identify the supplier, affected platform and end users separately; state
   who was exposed, who was demonstrably harmed, and what remains unknown.
   Distinguish a compromised delivery path from a flaw in the supplier's
   normal product, and a platform incident from an underlying protocol failure.
   Use a claim/correction or question/answer table for common misconceptions.
6. **Timeline and current state:** include meaningful dates, fixes and rollout
   status when they clarify the story. Label time zones and distinguish announced,
   scheduled and deployed changes as of the note's date.
7. **Practical response and lessons:** give concrete actions and explain how to
   verify the result. Search for relevant open-source code, tools or scripts
   that help readers inspect, reproduce, detect or mitigate the topic. Include
   useful finds with a source link, what each does, how to start and its limits;
   omit a tool list when none helps. For incidents, give exact retrospective
   search terms, logs or hashes where available, and explain what a hit, a
   changed hash or missing evidence does and does not establish. For
   non-incident topics, cover applications and trade-offs.
8. **Source context and Related:** when the user supplies background material,
   describe it briefly as "user-provided details" and identify the primary
   sources used to check material claims. Then end with the required Related links.

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
  - **Custom Architecture SVGs:** For deep educational notes or complex multi-stage systems (e.g., end-to-end storage tiering, hardware memory layouts, side-by-side comparative flows, or multi-panel infographics), provide a dedicated SVG diagram. It is not mandatory for every note, but strongly recommended when visual richness enhances understanding.
    - Always store the `.svg` in the nearest category-level `assets/` folder (e.g. `AI-ML/LLMs/assets/<Name>.svg`) and reference it with a relative path (`![Title](../assets/<Name>.svg)`).
    - Keep SVGs dark-theme native (`#0b0f19` / `#111827` background, slate containers `#1e293b`, cyan `#38bdf8`, emerald `#4ade80`, amber `#fbbf24`, muted text `#94a3b8`) with a responsive `viewBox`.
    - **Strict XML validation:** All text nodes must escape ampersands as `&amp;` and angle brackets as `&lt;` / `&gt;`. Always validate SVG syntax before delivery (e.g., via `python3 -c "import xml.etree.ElementTree as ET; ET.parse('path/to.svg')"`).
    - **Text Boundary & Overflow Clamping:** Unlike HTML, SVG `<text>` elements **do not auto-wrap**. Furthermore, GitHub's image sanitizer and `camo` proxy strip `<foreignObject>` blocks for security reasons. Never write single uninterrupted text lines exceeding 55–60 characters inside standard card containers (~450–500px width at font-size 11–12px). Manually wrap sentences across multiple `<text>` lines with controlled vertical spacing (16–18px offsets).
    - **Automated SVG Verification:** Always validate diagrams using `python3 Scripts/check-svg.py path/to/diagram.svg` (or `python3 Scripts/check-markdown.py path/to/note.md`) to catch text boundary overflows, tight margins (<5px), and invalid viewBox dimensions before delivery.
    - When helpful, pair the SVG (high-level visual infographic) with focused in-line Mermaid diagrams for specific sub-mechanisms (e.g. request sequence or attention projection).
- **LaTeX Math and KaTeX Rendering on GitHub:**
  - **Subscripts outside `\text{}`:** In KaTeX/LaTeX, `\text{...}` operates in text mode. An unescaped underscore `_` is illegal in text mode and throws the KaTeX error `'_' allowed only in math mode`. Move subscripts outside `\text{}` into math mode (e.g., write `\text{Score}_{\text{RRF}}(d)` instead of `\text{RRF_Score}(d)`).
  - **Flush-left display math (column 0, NO list indentation):** Never indent display math blocks (`$$...$$`) inside Markdown lists (`1.`, `2.`, `-`). When indented inside a list item, GitHub Flavored Markdown (GFM) parses `$$` as plain paragraph text inside the list rather than as a KaTeX display math block. The Markdown parser then interprets math subscript underscores `_` as Markdown *italics* syntax (`_italic_`), corrupting the equation and dumping raw unrendered LaTeX on screen. Always place display math blocks (`$$...$$`) at column 0 (flush-left) separated by blank lines before and after.
- Use tables for genuine comparisons.
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
- [ ] SVGs validated for well-formed XML and container text overflows (`python3 Scripts/check-svg.py path/to.svg`)
- [ ] Mermaid diagrams checked for statement semicolons, edge delimiter collisions (`||`), nested colons, and bidirectional label overlaps
- [ ] Math display blocks (`$$...$$`) placed flush-left (column 0, no list indentation) with subscripts outside `\text{}` (`\text{Score}_{\text{sub}}`)
- [ ] Relative links inside moved files fixed
- [ ] Relative image/asset paths fixed
- [ ] New `.md` file ends with a `**Related:**` section (3–5 links + reasons)
- [ ] Back-links added in the closest existing sibling doc(s)
- [ ] Moved/renamed file: own Related links fixed + old references updated
- [ ] `python3 Scripts/check-markdown.py path/to/file.md` (or `--recent`) clean
- [ ] `python3 Scripts/generate-readme.py` run (never hand-edit `README.md`)
- [ ] `python3 Scripts/github-repos.py links` clean
- [ ] Leave changes uncommitted for user review; commit only after explicit approval
