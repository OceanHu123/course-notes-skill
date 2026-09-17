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

## Step 1 — Locate the material

Read `references/material-index.md` first. If the course or week is missing, discover it once and **add a row**.

**Ed lessons/slides** — the Ed MCP has no lesson/slide tool, so call the API directly:

```bash
/Users/oakley/Projects/mcp/ed-mcp/.venv/bin/python - <<'PY'
from dotenv import load_dotenv; load_dotenv("/Users/oakley/Projects/mcp/ed-mcp/.env")
import os, httpx
h = {"Authorization": f"Bearer {os.environ['ED_API_TOKEN']}", "Accept": "application/json"}
c = httpx.Client(base_url="https://edstem.org/api", headers=h, timeout=60)
for l in c.get("/courses/<COURSE_ID>/lessons").json()["lessons"]:
    print(l["id"], l["title"], l["slide_count"])
print(c.get("/lessons/<LESSON_ID>").json()["lesson"]["slides"])   # 全量 slide 含 file_url
PY
```

Slide `type` 决定值不值得细看：`code`/`document` 有正文；`quiz`、`pdf` 看 `file_url`；纯 `<figure><image>` 的页要靠 OCR。Ed `/courses/<ID>/resources` 多为空，材料基本都在 lessons 里。

**Canvas PDFs** — `get_course_structure` 找 module → item 的 `content_id`，再用 `download_course_file`。`list_course_files` / `list_pages` 可能 403 或 404，失败就走 module 路线。

## Step 2 — Extract text

```bash
python3 <skill>/scripts/fetch_material.py <url-or-local-pdf> --out /tmp/material.txt
```

It also prints which pages are **image-only** — that's the OCR worklist.

## Step 3 — OCR the image-only pages

```bash
python3 <skill>/scripts/ocr_pages.py <pdf> <page-list|all> --dpi 200
```

Uses macOS Vision through the bundled `scripts/ocr.swift` (no install needed), or `tesseract` if it exists. Slide screenshots of terminals are usually plain text and OCR almost perfectly.

If neither engine works, write **"此页为图，未读"** for those pages and ask the user to paste the image. Never guess what a figure shows.

## Step 4 — Write the notes

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
- 把 token 或课程内容粘进 skill 文件
- 留下一次性文件（下载的 PDF、提取的 txt、渲染的 png）
