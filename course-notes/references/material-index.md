# Material Index

Per-course map of **where the material lives**, so it never has to be rediscovered.

Kept deliberately thin: ids only, no course content.

## Template

```markdown
## <COURSE CODE> — <course name>

- Canvas course id: <id>          # get_course_structure / download_course_file
- Ed course id: <id>              # /courses/<id>/lessons

### Lectures (Canvas modules → PDFs)

| Week | File | Canvas file id |
|---|---|---|
| 1 | Week-1.pdf | 00000000 |

### Ed lessons

| Lesson | Ed lesson id | Slides |
|---|---|---|
| Lab 1 | 000000 | 24 |

### Notes

- <anything that surprised you, e.g. endpoints that 404>
```

---

## INFO1112 — Computing 1B OS and Network Platforms

- Canvas course id: `73745`
- Ed course id: `36385`

### Lectures (Canvas modules → PDFs)

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

Assignment 1 spec: Canvas file `52519389` (also on Ed as `Assignment 1 - 2026` → slide "Assignment Spec").

### Ed lessons

| Lesson | Ed lesson id | Slides |
|---|---|---|
| Lab 1: Introduction to Unix and Shell | 109422 | 24 |
| Lab 2: More Bash-ing | 109423 | 14 |
| Lab 3: Script, grep, conditionals, loop | 109424 | 8 |
| Lab 4: Docker | 109425 | 3 |
| Lab 5: Processes and Memory | 109426 | 12 |
| Lab 6: Git | 109427 | 4 |
| Lab 7: Git Merge, Git Branch | 109428 | 8 |
| Homework 1 - S2 2026 | 116763 | 6 |
| Homework 2 - S2 2026 | 117448 | 2 |
| Assignment 1 - 2026 | 118076 | 3 |
| Week 1–3 Bash Practice Exercises | 117178 | 6 |
| Alpine Linux Virtual Machine | 117272 | 1 |

### Notes

- `list_course_files` and `list_pages` return **403/404** for this course — go through `get_course_structure`.
- `/courses/36385/resources` is empty; everything is under lessons.
- Lecture PDFs placed in a Canvas **module** are often also linked from the matching Lab slide.
- Week 6 deck is Git (the generic lecture-outline table says "networking" — trust the deck).
- Week 5 deck pages 19–20 and 22–27 are image-only (memory layout / page table diagrams) → OCR.
