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

## 上手（最多 3 步）

```
第 1 步（必须）装 skill  ──►  立刻可用：给个 PDF 就能出笔记
第 2 步（可选）配 token  ──►  能自动抓课件
第 3 步        直接说话  ──►  "INFO1112 wk5 总结"
```

| Tier | 你要做什么 | 能得到什么 |
|---|---|---|
| **Tier 0** 本地模式 | 只装 skill | 总结 / 讲解 / 答题 —— 材料自己给（拖 PDF、贴截图） |
| **Tier 1** 半自动 | 再配 Canvas **或** Ed 其中一个 token | 自动抓那一侧的材料 |
| **Tier 2** 全自动 | 两个 token 都配 | 课程自动发现 + 材料自动抓取 + 出笔记 |

**Tier 0 是真能用的**：结构化笔记、图片 OCR、临时文件清理全都不依赖 token。所以第 1 步做完就有价值。

### 第 1 步：装 skill（必须）

```bash
git clone https://github.com/OceanHu123/course-notes-skill.git ~/Projects/course-notes-skill

# 方式一：软链接（改仓库即时生效）
ln -s ~/Projects/course-notes-skill/course-notes ~/.trae-cn/skills/course-notes

# 方式二：直接复制（最稳，和仓库解耦）
cp -R ~/Projects/course-notes-skill/course-notes ~/.trae-cn/skills/
```

路径说明：

- **Trae CN** → `~/.trae-cn/skills/`
- **Trae 国际版** → `~/.trae/skills/`

装好后重启 Trae，skill 会自动被识别（`SKILL.md` 的 `description` 就是触发器）。软链接没被识别的话换成方式二。

### 第 2 步（可选）：配 token

凭据**不放在 skill 里**（所以这个仓库可以公开），而是交给两个 MCP 服务器：

| 想要什么 | 需要什么 | 从哪拿 |
|---|---|---|
| Canvas 课表 / 课件 PDF | `CANVAS_API_URL` + `CANVAS_API_TOKEN` | Canvas → Account → Settings → **+ New Access Token**。URL 形如 `https://<你学校>.instructure.com/api/v1` |
| Ed lessons / slides | `ED_API_TOKEN` | 见 [ed-mcp](https://github.com/januarharianto/ed-mcp) 的 README |

两个服务器都是公开项目：

- Canvas → [vishalsachdev/canvas-mcp](https://github.com/vishalsachdev/canvas-mcp)
- Ed → [januarharianto/ed-mcp](https://github.com/januarharianto/ed-mcp)

各自把 token 写进自己仓库的 `.env`，然后在 Trae 里注册（`~/Library/Application Support/Trae CN/User/mcp.json`）：

```json
{
  "mcpServers": {
    "canvas": { "command": "/绝对路径/run-canvas-mcp.sh", "args": [], "env": {} },
    "ed":     { "command": "/绝对路径/run-ed-mcp.sh",     "args": [], "env": {} }
  }
}
```

skill 默认去 `~/Projects/mcp/{canvas-mcp,ed-mcp}/.env` 读凭据；路径不一样就设 `MCP_DIR`，别改代码。

**验证配好了没**（顺便列出你账号里的所有课程）：

```bash
python3 ~/.trae-cn/skills/course-notes/scripts/check_env.py
```

它会告诉你现在是 Tier 几，以及哪一侧还缺。

### 第 3 步：直接用

```
INFO1112 wk5 总结
wk7 总结
explain https://edstem.org/au/courses/36385/lessons/109426/slides/808037
https://edstem.org/au/courses/36385/lessons/109426/slides/809827 回答每个问题并解释代码
出题考我 Week 5 的内容
```

笔记会落到 `~/notes/<course-code>/<topic>.md`（**项目外独立目录**，不污染你的代码仓库）；`/tmp` 下的 PDF、提取的 txt、渲染的 png 用完即删。

## 依赖

| 用途 | 要求 |
|---|---|
| 读 PDF | `python3` + **PyMuPDF**（`import fitz`）。macOS 自带 python3 通常已有；没有就 `python3 -m pip install --user pymupdf` |
| OCR 图片页 | 优先级：**tesseract**（装了就用）→ **macOS Vision**（自带 `swiftc` 即可，零安装）→ 都没有则标注"此页为图，未读" |
| 自动取材料（可选） | Canvas / Ed 的 MCP 服务器 + token，见第 2 步 |

## 让它认识你的课程

**索引是缓存，不是前置条件。** 新用户一个 id 都不用填 —— 直接说 `INFO1112 wk5 总结`，skill 会先在**你自己账号的** Canvas / Ed 课表里匹配，再把结果写进索引，下次就不用再查了。

索引在 [`course-notes/references/material-index.md`](course-notes/references/material-index.md)，只存 id，不存课程内容。仓库里附带了一份 **INFO1112（USYD）** 的现成样例：Canvas course `73745`、Ed course `36385`、Week 1–7 全部 lecture PDF 的 file id、12 个 lesson id。

加一门课不用手填，跑一条命令，输出可直接粘贴：

```bash
python3 ~/.trae-cn/skills/course-notes/scripts/discover_course.py <COURSE-CODE>
```

```markdown
## INFO1112 - INFO1112 Computing 1B OS and Network Platforms

# school: University of Sydney (Ed realm)
- Canvas course id: 73745
- Ed course id: 36385

### Lectures (Canvas modules -> PDFs)

| Week | File | Canvas file id |
|---|---|---|
| 5 | Week-5.pdf | 52239164 |

### Ed lessons

| Module | Lesson | Ed lesson id | Slides |
|---|---|---|---|
| + Labs | Lab 5: Processes and Memory | 109426 | 12 |
```

> 课程代码本身**不含学校信息** —— `INFO1112` 只在**你的账号**里有意义。学校由平台给出（Ed 的 `realm`、Canvas 实例的域名），skill 不会从代码去猜；匹配不到就明说，不编 id。

## 工作原理

```
check_env ──► 解析课程 ──► 找材料 ──► 抽文字 ──► OCR 图片页 ──► 写笔记 ──► 清理
```

1. **`scripts/check_env.py`**：探当前处于哪个 Tier，列出账号里实际可见的课程
2. **`scripts/discover_course.py`**：课程代码 → Canvas/Ed id + 周次文件表 + lesson 表，输出可粘贴的索引段落
3. **找材料**
   - **Ed lessons/slides**：Ed MCP 没有 lesson/slide 接口，直接调 `/courses/{id}/lessons` 和 `/lessons/{id}`（能拿到 slide 全文和 `file_url`）
   - **Canvas PDF**：`get_course_structure` 找 module item 的 `content_id` → `download_course_file`（`list_course_files` / `list_pages` 对某些课程会 403/404）
4. **抽文字**：`scripts/fetch_material.py` 按页输出，并**列出没有文字的页**（OCR 工作清单）
5. **OCR**：`scripts/ocr_pages.py` 渲染指定页并识别；`scripts/ocr.swift` 是 macOS Vision 的实现，首次运行编译并缓存到 `~/.cache/course-notes/`
6. **写笔记**：按固定模板，中文讲解 + 技术术语保留英文原词（container / process / image / branch…），每条要点带页码或 slide id
7. **清理**：`/tmp` 下的一次性文件全部删掉

`scripts/_common.py` 是共用的凭据定位与 API 封装。它只**读** MCP 的 `.env`，自己从不存 token；环境变量优先，所以可以用 `MCP_DIR` / `CANVAS_ENV` / `ED_ENV` 指向别处。

## 目录结构

```
course-notes-skill/
├── README.md
└── course-notes/              ← 这个目录就是要装进 skills/ 的 skill
    ├── SKILL.md
    ├── references/
    │   └── material-index.md
    └── scripts/
        ├── _common.py          # 凭据定位 + Canvas/Ed API 封装
        ├── check_env.py        # 自检：Tier 判定 + 列出账号课程
        ├── discover_course.py  # 课程代码 → 可粘贴的索引段落
        ├── fetch_material.py   # PDF → 按页文字 + 图片页清单
        ├── ocr_pages.py        # 指定页 OCR
        └── ocr.swift           # macOS Vision OCR
```

## 已知限制

- **只认你自己账号里的课**：skill 没有全局课程库，匹配范围就是你的 Canvas / Ed 选课列表。
- **纯示意图读不了**：折线图、拓扑图这类 OCR 出来是零散文字。终端截图、文字型 slide 效果很好。遇到读不了的图会明确标注"此页为图，未读"，**不会编造内容**。
- **扫描版 PDF**：整本都没有文字层，会被全部报成图片页，只能整页 OCR，慢且容易出错。
- **Canvas 权限**：不同课程的 API 开放程度不一样，`403/404` 是常见情况，走 module 路线更稳。
- **Ed 会拦没有 `User-Agent` 的请求**（返回 403），脚本里已经带上。
