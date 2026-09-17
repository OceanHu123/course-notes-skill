# Material Index

Per-course map of **where the material lives**, so it never has to be rediscovered.

This file is a **cache, not a prerequisite**. Nothing here is required to use the skill — when a course is missing, resolve it live and append the result:

```bash
python3 scripts/discover_course.py <COURSE-CODE>
```

Kept deliberately thin: ids only, no course content.

## Template

```markdown
## <COURSE CODE> - <course name>

# school: <from the platform, never from the code>
- Canvas course id: <id>          # get_course_structure / download_course_file
- Ed course id: <id>              # /courses/<id>/lessons

### Lectures (Canvas modules -> PDFs)

| Week | File | Canvas file id |
|---|---|---|
| 1 | Week-1.pdf | 00000000 |

### Ed lessons

| Module | Lesson | Ed lesson id | Slides |
|---|---|---|---|
| + Labs | Lab 1 | 000000 | 24 |

### Notes

- <anything that surprised you, e.g. endpoints that 404>
```

---

## INFO1112 - Computing 1B OS and Network Platforms

# school: University of Sydney (Ed realm 1, sydney.edu.au)

- Canvas course id: `73745`
- Ed course id: `36385`

### Lectures (Canvas modules -> PDFs)

| Week | File | Canvas file id |
|---|---|---|
| 1 | Week-1.pdf | 51762520 |
| 1 | Week-1 - v2.pdf | 51861267 |
| 2 | Week-2.pdf | 52214029 |
| 3 | Week-3-A.pdf | 51975888 |
| 3 | Week-3-B.pdf | 51979469 |
| 4 | Week-4 - A.pdf | 52105980 |
| 5 | Week-5.pdf | 52239164 |
| 6 | Week-6-Git-v2.pdf | 52395079 |
| 7 | Week-7-Git-Part-B.pdf | 52561846 |
| 7 | Week-7 - Networking.pdf | 52564290 |

Assignment 1 spec: Canvas file `52519389`（也在 Ed 的 `Assignment 1 - 2026` → slide "Assignment Spec"）。

### Ed lessons

| Module | Lesson | Ed lesson id | Slides |
|---|---|---|---|
| + Labs | Lab 1: Introduction to Unix and Shell | 109422 | 24 |
| + Labs | Lab 2: More Bash-ing | 109423 | 14 |
| + Labs | Lab 3: Script, grep, conditionals, loop | 109424 | 8 |
| + Labs | Lab 4: Docker | 109425 | 3 |
| + Labs | Lab 5: Processes and Memory | 109426 | 12 |
| + Labs | Lab 6: Git | 109427 | 4 |
| + Labs | Lab 7: Git Merge, Git Branch | 109428 | 8 |
| 2- Homework | Homework 1 - S2 2026 | 116763 | 6 |
| 2- Homework | Homework 2 - S2 2026 | 117448 | 2 |
| 3- Assignments | Assignment 1 - 2026 | 118076 | 3 |
| Practice | Week 1–3 Bash Practice Exercises (non-examinable) | 117178 | 6 |
| - | Alpine Linux Virtual Machine (Non examinable) | 117272 | 1 |

### Notes

- `list_course_files` 和 `list_pages` 对这门课返回 **403/404** —— 走 `get_course_structure`。
- `/courses/36385/resources` 是空的；材料都在 lessons 里。
- 放在 Canvas module 里的 lecture PDF，通常在对应 Lab 的 slide 里也有链接。
- Week 6 的 deck 是 Git（通用 lecture-outline 表里写的是 networking —— 以 deck 为准）。
- Week 5 deck 的第 19–20、25–27 页是纯图片（memory layout / page table 图）→ 需要 OCR。
- Ed 会拦没有 `User-Agent` 的请求（403）；`scripts/_common.py` 已统一带上。
