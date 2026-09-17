#!/usr/bin/env python3
"""Resolve a course code into a paste-ready block for references/material-index.md.

usage:
    python3 discover_course.py <COURSE-CODE>

Looks the code up in the account's own Canvas and Ed course lists - it never
guesses an institution from the code itself.  Prints a markdown block that can
be appended to the index as-is.
"""

from __future__ import annotations

import re
import sys

import _common as c


def pick(rows: list, code: str) -> list:
    """Rows are (code, name, id). Return exact matches, else partial ones."""
    exact = [r for r in rows if c.norm_code(r[0]) == c.norm_code(code)]
    if exact:
        return exact
    return [r for r in rows if c.code_matches(code, r[0])]


# ----------------------------------------------------------------------
# Canvas
# ----------------------------------------------------------------------


def canvas_blocks(course_id: int) -> tuple:
    creds = c.canvas_credentials()
    if not creds:
        return [], "Canvas not configured (" + c.CANVAS_HINT + ")"
    try:
        modules = c.canvas_get(creds, "/courses/{}/modules".format(course_id),
                               {"include[]": "items", "per_page": 100})
    except c.ApiError as exc:
        return [], "Canvas modules failed: {}".format(exc)

    lectures, other = [], []
    for module in modules if isinstance(modules, list) else []:
        name = module.get("name") or ""
        week = re.search(r"\bweek\s*(\d+)", name, re.I)
        week_label = week.group(1) if week else "-"
        for item in module.get("items") or []:
            if item.get("type") != "File":
                continue
            title = item.get("title") or ""
            row = (week_label, title, item.get("content_id"))
            if title.lower().endswith(".pdf"):
                lectures.append(row)
            else:
                other.append(row)
    return (lectures, other), None


# ----------------------------------------------------------------------
# Ed
# ----------------------------------------------------------------------


def ed_block(course_id: int) -> tuple:
    """Return (lines, error). Lessons are grouped by module."""
    creds = c.ed_credentials()
    if not creds:
        return [], "Ed not configured (" + c.ED_HINT + ")"
    try:
        data = c.ed_get(creds, "/courses/{}/lessons".format(course_id))
    except c.ApiError as exc:
        return [], "Ed lessons failed: {}".format(exc)

    modules = data.get("modules") or []
    order = {m.get("id"): i for i, m in enumerate(modules)}
    names = {m.get("id"): m.get("name") for m in modules}

    lessons = data.get("lessons") or []
    lessons.sort(key=lambda l: (order.get(l.get("module_id"), len(order)), l.get("index") or 0))
    if not lessons:
        return [], "Ed returned no lessons for course {}".format(course_id)

    lines = ["### Ed lessons", "", "| Module | Lesson | Ed lesson id | Slides |", "|---|---|---|---|"]
    for lesson in lessons:
        lines.append("| {} | {} | {} | {} |".format(
            names.get(lesson.get("module_id"), "-"),
            lesson.get("title") or "",
            lesson.get("id"),
            lesson.get("slide_count"),
        ))
    return lines, None


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    code = sys.argv[1]

    canvas_rows, canvas_err = [], None
    creds = c.canvas_credentials()
    if creds:
        try:
            data = c.canvas_get(creds, "/courses", {"per_page": 100})
            canvas_rows = [(x.get("course_code") or "", x.get("name") or "", x.get("id"))
                           for x in (data if isinstance(data, list) else [])]
        except c.ApiError as exc:
            canvas_err = str(exc)
    else:
        canvas_err = "Canvas not configured (" + c.CANVAS_HINT + ")"

    ed_rows, ed_school, ed_err = [], None, None
    creds = c.ed_credentials()
    if creds:
        try:
            data = c.ed_get(creds, "/user")
            realms = {r.get("id"): r.get("name") for r in (data.get("realms") or [])}
            for entry in data.get("courses") or []:
                course = entry.get("course", entry)
                ed_rows.append((course.get("code") or "", course.get("name") or "", course.get("id")))
                if ed_school is None and course.get("realm_id") in realms:
                    ed_school = realms[course["realm_id"]]
        except c.ApiError as exc:
            ed_err = str(exc)
    else:
        ed_err = "Ed not configured (" + c.ED_HINT + ")"

    canvas_hits, ed_hits = pick(canvas_rows, code), pick(ed_rows, code)

    print("# resolved from the account's own course lists (nothing was guessed)")
    print()
    if canvas_err:
        print("# Canvas: {}".format(canvas_err))
    if ed_err:
        print("# Ed:     {}".format(ed_err))
    print()

    if not canvas_hits and not ed_hits:
        print("No course matching '{}' in this account.".format(code))
        print()
        print("Canvas courses: {}".format(", ".join(r[0] for r in canvas_rows) or "(none)"))
        print("Ed courses:     {}".format(", ".join(r[0] for r in ed_rows) or "(none)"))
        print()
        print("Do not guess the institution from the code - ask the user instead.")
        return 1

    name = (canvas_hits or ed_hits)[0][1]
    print("## {} - {}".format(code, name))
    print()
    if ed_school:
        print("# school: {} (Ed realm)".format(ed_school))
    if canvas_hits:
        print("- Canvas course id: {}".format(canvas_hits[0][2]))
    else:
        print("- Canvas course id: (not in this account)")
    if ed_hits:
        print("- Ed course id: {}".format(ed_hits[0][2]))
    else:
        print("- Ed course id: (not in this account)")
    print()

    if canvas_hits:
        blocks, error = canvas_blocks(canvas_hits[0][2])
        if error:
            print("# {}".format(error))
        else:
            lectures, other = blocks
            print("### Lectures (Canvas modules -> PDFs)")
            print()
            print("| Week | File | Canvas file id |")
            print("|---|---|---|")
            for week, title, identifier in lectures:
                print("| {} | {} | {} |".format(week, title, identifier))
            if other:
                print()
                print("### Other module files")
                print()
                print("| Week | File | Canvas file id |")
                print("|---|---|---|")
                for week, title, identifier in other:
                    print("| {} | {} | {} |".format(week, title, identifier))
        print()

    if ed_hits:
        lines, error = ed_block(ed_hits[0][2])
        if error:
            print("# {}".format(error))
        else:
            print("\n".join(lines))
        print()

    print("### Notes")
    print()
    print("- Paste this block into references/material-index.md")
    print("- Add anything that surprised you here (endpoints that 404, image-only pages, ...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
