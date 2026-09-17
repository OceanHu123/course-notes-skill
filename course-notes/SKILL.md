---
name: course-notes
description: Summarize and explain Canvas/Ed course material (lecture PDFs, lessons, slides) into structured study notes. Use when asked to summarize or explain a week, lab, slide, or assignment. Not for non-course documents.
---

# Course Notes

Turn course material into study notes, page-by-page explanations, or answers.

## Modes

| Mode | Trigger | Output |
|---|---|---|
| summary | 总结某周 / "wkN 总结" | 该周课件的结构化笔记 |
| explain | "explain" / 逐页讲解 | 按页/slide 详解 |
| answer | "回答每个问题" / 做题 | 逐题作答 + 代码逐行解释 |
| quiz | "出题考我" | 自测题 + 答案 |

## Step 0 — Know what you can do

Run once per session when the setup is unknown:

```bash
python3 <skill>/scripts/check_env.py
```

It prints the tier, so pick the matching path below. **Never assume credentials exist.**

| Tier | Meaning | How to get material |
|---|---|---|
| 2 | Canvas + Ed both reachable | fully automatic |
| 1 | only one side reachable | use that side, ask the user for the rest |
| 0 | no credentials | **ask the user to drop the PDF or paste screenshots** — everything downstream still works |

## Step 1 — Resolve the course

Read `references/material-index.md`. If the course is there, use it. Otherwise resolve it once:

```bash
python3 <skill>/scripts/discover_course.py <COURSE-CODE>
```

It prints a paste-ready block — append it to the index so the next run is instant.

Resolution rules:

- Match the code against **the account's own course lists** (Canvas and Ed). Never infer the institution from the code: `INFO1112` carries no school information.
- The school comes from the platform, not the code: an Ed course has a `realm` (e.g. `1 -> University of Sydney`), a Canvas MCP instance is bound to one institution.
- Not found → say so plainly and list what the account does have. Do not guess, do not invent an id.
- Canvas codes carry suffixes like `INFO1112 (ND)`, and some are pairs like `DATA1001/1901` — normalise before comparing.

Course material is split across two platforms, so check both: lecture PDFs usually live in Canvas modules, lessons and slides in Ed.

## Step 2 — Fetch the material

**Ed lessons/slides** — the Ed MCP has no lesson/slide tool, so call the API through the shared helper:

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "<skill>/scripts")
import _common as c
creds = c.ed_credentials()
print(c.ed_get(creds, "/courses/<COURSE_ID>/lessons")["lessons"])
det = c.ed_get(creds, "/lessons/<LESSON_ID>")["lesson"]
for s in det["slides"]:
    print(s["id"], s["type"], s["title"], s.get("file_url", ""))
print([s["content"] for s in det["slides"]])
PY
```

Slide `type` decides how much is readable: `code` / `document` carry the body text; `quiz` and `pdf` point at `file_url`; a slide that is only `<figure><image>` needs OCR. Ed `/courses/<ID>/resources` is usually empty — the material is in lessons.

**Canvas PDFs** — `get_course_structure` for module → item `content_id`, then `download_course_file`. `list_course_files` / `list_pages` return 403 or 404 on some courses; the module route is the reliable one.

Credentials are read from `MCP_DIR/canvas-mcp/.env` and `MCP_DIR/ed-mcp/.env` (default `~/Projects/mcp`). If the user's layout differs, set `MCP_DIR` instead of editing code. **Never copy a token into the skill or into a note.**

## Step 3 — Extract text

```bash
python3 <skill>/scripts/fetch_material.py <url-or-local-pdf> --out /tmp/material.txt
```

It also prints which pages are **image-only** — that's the OCR worklist.

## Step 4 — OCR the image-only pages

```bash
python3 <skill>/scripts/ocr_pages.py <pdf> <page-list|all> --dpi 200
```

Uses macOS Vision through the bundled `scripts/ocr.swift` (no install needed), or `tesseract` if it exists. Screenshots of terminals are usually plain text and OCR almost perfectly.

If neither engine works, write **"此页为图，未读"** for those pages and ask the user to paste the image. Never guess what a figure shows.

## Step 5 — Write the notes

Template, in this order:

1. **总览** — 主题、页码范围、对应周次
2. **分部分详解** — 带页码/slide id
3. **对比表格** — 容易混的概念
4. **速查表** — 命令/术语一览
5. **易混点** — 成对区分
6. **与作业或考试的关联**
7. **未读图页清单** — 如有

Save to `~/notes/<course-code>/<topic>.md`（项目外独立目录）。**只有笔记落盘；`/tmp` 下的临时文件读完即删。**

## Style

- 中文讲解释，技术术语保留英文原词：container, image, process, signal, PID, branch, repository，不要翻译成"容器/镜像"混着写
- 每条要点标页码或 slide id，方便回查
- 别太"AI 味"：先给结论，再举具体例子，允许啰嗦一点
- 结尾列出可选的下一步（深入某几页 / 做题 / 预习下次 lab）

## Do not

- 编造图片内容
- 从课程代码推断学校
- 凭据不可用时硬撑 —— 退到 Tier 0，让用户给文件
- 把 token 或课程内容粘进 skill 文件
- 留下一次性文件（下载的 PDF、提取的 txt、渲染的 png）
