#!/usr/bin/env python3
"""Check which parts of the skill can work right now.

usage:
    python3 check_env.py

Reports the tier, lists the courses actually visible to the account, and says
what to do next.  Nothing here is required for the offline (local PDF) mode.
"""

from __future__ import annotations

import sys

import _common as c


def canvas_courses() -> tuple:
    """Return (courses, error). courses is a list of (code, name, id)."""
    creds = c.canvas_credentials()
    if not creds:
        return [], "no credentials (" + c.CANVAS_HINT + ")"
    try:
        data = c.canvas_get(creds, "/courses", {"per_page": 100})
    except c.ApiError as exc:
        return [], str(exc)
    rows = []
    for course in data if isinstance(data, list) else []:
        rows.append((course.get("course_code") or "", course.get("name") or "", course.get("id")))
    rows.sort(key=lambda r: r[0])
    return rows, None


def ed_courses() -> tuple:
    """Return (courses, school, error). courses is a list of (code, name, id)."""
    creds = c.ed_credentials()
    if not creds:
        return [], None, "no credentials (" + c.ED_HINT + ")"
    try:
        data = c.ed_get(creds, "/user")
    except c.ApiError as exc:
        return [], None, str(exc)

    realms = {r.get("id"): r.get("name") for r in (data.get("realms") or [])}
    rows, school = [], None
    for entry in data.get("courses") or []:
        course = entry.get("course", entry)
        rows.append((course.get("code") or "", course.get("name") or "", course.get("id")))
        if school is None and course.get("realm_id") in realms:
            school = realms[course["realm_id"]]
    rows.sort(key=lambda r: r[0])
    return rows, school, None


def main() -> int:
    print("skill: course-notes")
    print("mcp dir: {}".format(c.mcp_dir()))
    print()

    canvas_rows, canvas_err = canvas_courses()
    ed_rows, school, ed_err = ed_courses()

    print("=== Canvas ===")
    if canvas_err:
        print("  unavailable: {}".format(canvas_err))
    else:
        print("  {} courses".format(len(canvas_rows)))
        for code, name, identifier in canvas_rows:
            print("  {:>7}  {:<28} {}".format(identifier, code, name))

    print()
    print("=== Ed ===")
    if ed_err:
        print("  unavailable: {}".format(ed_err))
    else:
        if school:
            print("  school: {} (from realm)".format(school))
        print("  {} courses".format(len(ed_rows)))
        for code, name, identifier in ed_rows:
            print("  {:>7}  {:<28} {}".format(identifier, code, name))

    print()
    print("=== tier ===")
    if canvas_rows or ed_rows:
        missing = []
        if not canvas_rows:
            missing.append("Canvas")
        if not ed_rows:
            missing.append("Ed")
        if missing:
            print("  Tier 1 (half automatic) - missing: {}".format(", ".join(missing)))
            print("  Lesson PDFs come from Canvas, slides and posts from Ed;")
            print("  with only one side configured, the other has to be supplied by hand.")
        else:
            print("  Tier 2 (fully automatic) - course discovery + material fetching + notes")
    else:
        print("  Tier 0 (local mode) - drop a PDF or paste a screenshot and it still works")

    print()
    print("Tier 0 always works. Tokens only add automatic material fetching.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
