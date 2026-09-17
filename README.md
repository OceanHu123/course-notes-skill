# course-notes

一个给 **Trae** 用的 skill：把 Canvas / Ed 上的课程材料（lecture PDF、lesson、slide）整理成结构化学习笔记。

不是又一个 PDF 摘要工具 —— 它把「材料在哪、怎么取、图片怎么读、笔记什么格式、临时文件什么时候删」这一整套流程固化下来，下次直接说 "wk7 总结" 就行。

## 它能做什么

| 模式 | 触发说法 | 产出 |
|---|---|---|
| **summary** | `wk5 总结` / `总结 Lab 6` | 该周课件的结构化笔记 |
| **explain** | `explain <slide 链接>` | 逐页 / 逐 slide 详解 |
| **answer** | `回答每个问题并解释代码` | 逐题作答 + 代码逐行解释 |
| **quiz** | `出题考我` | 自测题 + 答案 |

笔记固定包含：总览 → 分部分详解（带页码）→ 对比表格 → 速查表 → 易混点 → 与作业/考试的关联 → 未读图页清单。

## 安装

```bash
git clone https://github.com/OceanHu123/course-notes-skill.git ~/Projects/course-notes-skill

# 方式一：软链接（推荐，改仓库即时生效）
ln -s ~/Projects/course-notes-skill/course-notes ~/.trae-cn/skills/course-notes

# 方式二：直接复制
cp -R ~/Projects/course-notes-skill/course-notes ~/.trae-cn/skills/
```

路径说明：

- **Trae CN** → `~/.trae-cn/skills/`
- **Trae 国际版** → `~/.trae/skills/`

装好后重启 Trae，skill 会自动被识别（`SKILL.md` 的 `description` 就是触发器）。

## 使用

直接用自然语言，不需要点名 skill：

```
wk7 总结
https://edstem.org/au/courses/36385/lessons/109426/slides/809827 回答每个问题并解释代码
explain https://edstem.org/au/courses/36385/lessons/109426/slides/808037
出题考我 Week 5 的内容
```

笔记会落到 `~/notes/<course-code>/<topic>.md`（**项目外独立目录**，不污染你的代码仓库）；`/tmp` 下的 PDF、提取的 txt、渲染的 png 用完即删。

## 依赖

| 用途 | 要求 |
|---|---|
| 读 PDF | `python3` + **PyMuPDF**（`import fitz`）。macOS 自带 python3 通常已有；没有就 `python3 -m pip install --user pymupdf` |
| OCR 图片页 | 优先级：**tesseract**（装了就用）→ **macOS Vision**（自带 `swiftc` 即可，零安装）→ 都没有则标注"此页为图，未读" |
| 取材料 | Canvas / Ed 的 MCP 或 API 凭据（见下） |

## 让它认识你的课程

课程 ID、课件 file id、lesson id 全部写在 [`course-notes/references/material-index.md`](course-notes/references/material-index.md)，只有 id，没有课程内容。

仓库里附带了一份 **INFO1112（USYD）** 的现成索引作为样例：Canvas course `73745`、Ed course `36385`、Week 1–7 的全部 lecture PDF file id、12 个 lesson id。

换一门课，照着模板加一段即可：

```markdown
## <COURSE CODE> — <course name>

- Canvas course id: <id>
- Ed course id: <id>

### Lectures (Canvas modules → PDFs)

| Week | File | Canvas file id |
|---|---|---|
| 1 | Week-1.pdf | 00000000 |

### Ed lessons

| Lesson | Ed lesson id | Slides |
|---|---|---|
| Lab 1 | 000000 | 24 |
```

## 工作原理

```
找材料 ──► 抽文字 ──► OCR 图片页 ──► 写笔记 ──► 清理临时文件
```

1. **找材料**
   - **Ed lessons/slides**：Ed MCP 没有 lesson/slide 接口，直接调 `/courses/{id}/lessons` 和 `/lessons/{id}`（拿得到 slide 全文和 `file_url`）
   - **Canvas PDF**：`get_course_structure` 找 module item 的 `content_id` → `download_course_file`（`list_course_files` / `list_pages` 对某些课程会 403/404）
2. **抽文字**：`scripts/fetch_material.py` 按页输出，并**列出没有文字的页**（OCR 工作清单）
3. **OCR**：`scripts/ocr_pages.py` 渲染指定页并识别；`scripts/ocr.swift` 是 macOS Vision 的实现，首次运行时编译并缓存到 `~/.cache/course-notes/`
4. **写笔记**：按固定模板，中文讲解 + 技术术语保留英文原词（container / process / image / branch…），每条要点带页码或 slide id
5. **清理**：`/tmp` 下的一次性文件全部删掉

## 目录结构

```
course-notes-skill/
├── README.md
└── course-notes/              ← 这个目录就是要装进 skills/ 的 skill
    ├── SKILL.md
    ├── references/
    │   └── material-index.md
    └── scripts/
        ├── fetch_material.py
        ├── ocr_pages.py
        └── ocr.swift
```

## 已知限制

- **纯示意图读不了**：折线图、拓扑图这类 OCR 出来是零散文字。终端截图、文字型 slide 效果很好。遇到读不了的图会明确标注"此页为图，未读"，**不会编造内容**。
- **扫描版 PDF**：整本都没有文字层，会被全部报成图片页，只能整页 OCR，慢且容易出错。
- **Canvas 权限**：不同课程的 API 开放程度不一样，`403/404` 是常见情况，走 module 路线更稳。
- **只在有 Canvas/Ed 凭据的环境下能取材料**；没有凭据时可以让用户直接贴文件。
