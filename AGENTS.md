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
3. Put any linked images/PDFs in the nearest `assets/` folder
   (e.g. `AI-ML/assets/`) and reference them with a correct **relative** path.
   **Do NOT put images alongside the `.md` file.**
   **Do NOT put images in the root-level `assets/`** — always use the
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

## ⚠️ Quick Checklist

- [ ] Files named in **Title-Case-Year** format (e.g. `Sarvam-AI-Deep-Review-2026.md`)
- [ ] Files (and assets) placed in the right folder
- [ ] Moved/renamed files via `git mv` (not plain `mv`)
- [ ] Images/PDFs in `assets/` folder, **NOT** alongside the `.md` file
- [ ] **Do NOT put images in the root-level `assets/`** — use category-level `assets/`
- [ ] Relative links inside moved files fixed
- [ ] Relative image/asset paths fixed
- [ ] New `.md` file ends with a `**Related:**` section (3–5 links + reasons)
- [ ] Back-links added in the closest existing sibling doc(s)
- [ ] Moved/renamed file: own Related links fixed + old references updated
- [ ] `python3 Scripts/generate-readme.py` run (never hand-edit `README.md`)
- [ ] `python3 Scripts/github-repos.py links` clean
- [ ] Commit changes
