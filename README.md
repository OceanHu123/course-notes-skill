# course-notes

**Turn Canvas / Ed course material into structured study notes** — an Agent Skill for Trae, Cursor, and similar hosts.

Not another PDF summarizer. It locks in the full loop: find material → fetch → OCR image pages → fixed note template → delete temp files. After install, just say `wk7 总结` / `summarize week 7`.

[English demo notes](examples/demo/after-notes.md) · [中文说明](README.zh-CN.md) · [MIT License](LICENSE)

---

## 30-second pitch

| You give | You get |
|---|---|
| `INFO1112 wk5 总结` (or drop a PDF) | Overview → sectioned notes with page ids → comparison tables → cheat sheet → exam traps → homework links |
| Pure diagram pages | Marked **unread** — **never invented** |
| Temp PDF / png | Deleted after read; notes only under `~/notes/` |

**Before → After** (real Tier-0 run on [OSTEP Ch.4](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf) — denser textbook left, structured notes right):

![Before: OSTEP PDF · After: course-notes output](examples/demo/before-after.jpg)

Full notes: [`examples/demo/after-notes.md`](examples/demo/after-notes.md) · how to reproduce: [`examples/demo/`](examples/demo/)

## Modes

| Mode | Trigger | Output |
|---|---|---|
| **summary** | `wk5 总结` / `summarize Lab 6` | Structured notes for that week |
| **explain** | `explain <slide URL>` | Page / slide walkthrough |
| **answer** | `回答每个问题并解释代码` | Per-question answers + line-by-line code |
| **quiz** | `出题考我` / `quiz me` | Practice questions + answers |

## Setup (≤ 3 steps)

```
Step 1 (required) install skill  →  works immediately on a dropped PDF
Step 2 (optional) add tokens     →  auto-fetch from Canvas / Ed
Step 3            just talk      →  "INFO1112 wk5 总结"
```

| Tier | What you do | What you get |
|---|---|---|
| **Tier 0** local | Install skill only | Summarize / explain / answer from files you provide |
| **Tier 1** half-auto | Canvas **or** Ed token | Auto-fetch that side |
| **Tier 2** full-auto | Both tokens | Course discovery + fetch + notes |

**Tier 0 is real:** structured notes, OCR, and temp cleanup need no tokens.

### Step 1 — Install the skill

```bash
git clone https://github.com/OceanHu123/course-notes-skill.git ~/Projects/course-notes-skill
```

Link or copy the `course-notes/` folder into your skills path:

| Host | Skills directory | Example |
|---|---|---|
| **Trae CN** | `~/.trae-cn/skills/` | `ln -s ~/Projects/course-notes-skill/course-notes ~/.trae-cn/skills/course-notes` |
| **Trae** | `~/.trae/skills/` | same, different path |
| **Cursor** | `~/.cursor/skills/` (or project `.cursor/skills/`) | `ln -s ~/Projects/course-notes-skill/course-notes ~/.cursor/skills/course-notes` |
| **Other Agent Skill hosts** | see product docs | folder must contain `SKILL.md` |

```bash
# symlink (live updates from the repo)
ln -s ~/Projects/course-notes-skill/course-notes ~/.trae-cn/skills/course-notes

# or copy (decoupled)
cp -R ~/Projects/course-notes-skill/course-notes ~/.trae-cn/skills/
```

Restart the IDE / agent. The `description` in `SKILL.md` is the trigger. If a symlink is ignored, use copy.

### Step 2 (optional) — Tokens

Credentials stay in MCP servers (not in this skill), so the repo can stay public:

| Goal | Need | Where |
|---|---|---|
| Canvas modules / lecture PDFs | `CANVAS_API_URL` + `CANVAS_API_TOKEN` | Canvas → Account → Settings → **+ New Access Token**. URL like `https://<school>.instructure.com/api/v1` |
| Ed lessons / slides | `ED_API_TOKEN` | see [ed-mcp](https://github.com/januarharianto/ed-mcp) |

MCP projects:

- Canvas → [vishalsachdev/canvas-mcp](https://github.com/vishalsachdev/canvas-mcp)
- Ed → [januarharianto/ed-mcp](https://github.com/januarharianto/ed-mcp)

Put tokens in each project's `.env`, register MCP in your IDE (Trae example: `~/Library/Application Support/Trae CN/User/mcp.json`):

```json
{
  "mcpServers": {
    "canvas": { "command": "/absolute/path/run-canvas-mcp.sh", "args": [], "env": {} },
    "ed":     { "command": "/absolute/path/run-ed-mcp.sh",     "args": [], "env": {} }
  }
}
```

Default credential paths: `~/Projects/mcp/{canvas-mcp,ed-mcp}/.env`. Override with `MCP_DIR` — do not edit the skill.

**Sanity check** (also lists courses on your account):

```bash
python3 ~/.trae-cn/skills/course-notes/scripts/check_env.py
```

(Cursor: `~/.cursor/skills/course-notes/...`.) Prints your Tier and what is missing.

### Step 3 — Use it

```
INFO1112 wk5 总结
wk7 总结
explain https://edstem.org/au/courses/36385/lessons/109426/slides/808037
https://edstem.org/au/courses/36385/lessons/109426/slides/809827 回答每个问题并解释代码
出题考我 Week 5 的内容
```

Notes land in `~/notes/<course-code>/<topic>.md` (outside your code repos). Temp files under `/tmp` are deleted after use.

## Dependencies

| Use | Requirement |
|---|---|
| Read PDF | `python3` + **PyMuPDF** (`import fitz`). `python3 -m pip install --user pymupdf` if needed |
| OCR image pages | **tesseract** if present → else **macOS Vision** (`swiftc`) → else mark unread |
| Auto-fetch (optional) | Canvas / Ed MCP + tokens |

## Teaching the skill your courses

The material index is a **cache, not a prerequisite**. Say `INFO1112 wk5 总结`; the skill matches against **your** Canvas / Ed enrollments and appends the index.

Index file: [`course-notes/references/material-index.md`](course-notes/references/material-index.md) (ids only). A USYD INFO1112 sample is included for reference — your ids come from your account.

```bash
python3 ~/.trae-cn/skills/course-notes/scripts/discover_course.py <COURSE-CODE>
```

Prints a paste-ready Markdown block. Course codes do **not** encode the school; school comes from the platform (`realm` / Canvas host). No match → say so; never invent ids.

## How it works

```
check_env → resolve course → fetch → extract text → OCR → write notes → cleanup
```

See [`README.zh-CN.md`](README.zh-CN.md) for the detailed Chinese walkthrough of each script, or browse `course-notes/scripts/`.

## Layout

```
course-notes-skill/
├── LICENSE
├── README.md                 ← you are here (English)
├── README.zh-CN.md
├── examples/
│   ├── demo/                 ← OSTEP before/after for screenshots
│   └── notes/                ← extra anonymized sample
└── course-notes/             ← install this folder into skills/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

## Limits

- Only courses on **your** account (no global catalog).
- Pure diagrams: OCR is weak; skill marks unread instead of guessing.
- Fully scanned PDFs → all pages image-only; OCR is slow and noisy.
- Canvas API coverage varies (`403/404` common); module → `download_course_file` is the reliable path.
- Ed rejects requests without `User-Agent` (scripts already set one).

## License

[MIT](LICENSE). Demo PDF is from OSTEP (not redistributed in git) — https://pages.cs.wisc.edu/~remzi/OSTEP/
