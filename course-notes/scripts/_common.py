"""Shared helpers for locating credentials and talking to Canvas / Ed.

The skill never stores tokens.  Credentials live where the MCP servers keep
them, and this module only reads that location:

    <MCP_DIR>/canvas-mcp/.env   -> CANVAS_API_URL, CANVAS_API_TOKEN
    <MCP_DIR>/ed-mcp/.env       -> ED_API_TOKEN, ED_BASE_URL

Environment variables win over the .env files, so a user can point the skill
somewhere else without editing anything:

    MCP_DIR=/path/to/mcp
    CANVAS_ENV=/path/to/.env
    ED_ENV=/path/to/.env
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_MCP_DIR = pathlib.Path.home() / "Projects" / "mcp"
DEFAULT_ED_BASE = "https://edstem.org/api"
USER_AGENT = "course-notes-skill/1.0"

CANVAS_HINT = "Canvas: Account -> Settings -> + New Access Token"
ED_HINT = "Ed: see the ed-mcp README for ED_API_TOKEN"


class ApiError(Exception):
    """Raised when a Canvas or Ed request fails."""


def _base_headers() -> dict:
    """Ed rejects requests that arrive without a User-Agent, so always send one."""
    return {"Accept": "application/json", "User-Agent": USER_AGENT}


# ----------------------------------------------------------------------
# credential discovery
# ----------------------------------------------------------------------


def mcp_dir() -> pathlib.Path:
    return pathlib.Path(os.environ.get("MCP_DIR", str(DEFAULT_MCP_DIR))).expanduser()


def read_env_file(path: pathlib.Path) -> dict:
    """Parse a shell-style .env file. Missing file -> empty dict."""
    values: dict = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return values
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export "):].strip()
        value = value.strip().strip("'\"")
        if key:
            values[key] = value
    return values


def canvas_credentials() -> tuple:
    """Return (api_url, token) or None. URL already stripped of trailing slash."""
    url = os.environ.get("CANVAS_API_URL")
    token = os.environ.get("CANVAS_API_TOKEN")
    if not (url and token):
        env_path = os.environ.get("CANVAS_ENV")
        path = pathlib.Path(env_path).expanduser() if env_path else mcp_dir() / "canvas-mcp" / ".env"
        env = read_env_file(path)
        url = url or env.get("CANVAS_API_URL")
        token = token or env.get("CANVAS_API_TOKEN")
    if not (url and token):
        return None
    return url.rstrip("/"), token


def ed_credentials() -> tuple:
    """Return (api_base, token) or None."""
    token = os.environ.get("ED_API_TOKEN")
    base = os.environ.get("ED_BASE_URL")
    if not token:
        env_path = os.environ.get("ED_ENV")
        path = pathlib.Path(env_path).expanduser() if env_path else mcp_dir() / "ed-mcp" / ".env"
        env = read_env_file(path)
        token = token or env.get("ED_API_TOKEN")
        base = base or env.get("ED_BASE_URL")
    if not token:
        return None
    return (base or DEFAULT_ED_BASE).rstrip("/"), token


# ----------------------------------------------------------------------
# http
# ----------------------------------------------------------------------


def get_json(url: str, headers: dict = None, timeout: int = 60):
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ApiError("HTTP {} for {}".format(exc.code, url)) from exc
    except urllib.error.URLError as exc:
        raise ApiError("cannot reach {} ({})".format(url, exc.reason)) from exc


def canvas_get(credentials: tuple, path: str, params: dict = None):
    base, token = credentials
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    headers = _base_headers()
    headers["Authorization"] = "Bearer " + token
    return get_json(base + path + query, headers)


def ed_get(credentials: tuple, path: str, params: dict = None):
    base, token = credentials
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    headers = _base_headers()
    headers["Authorization"] = "Bearer " + token
    return get_json(base + path + query, headers)


# ----------------------------------------------------------------------
# course codes
# ----------------------------------------------------------------------


def norm_code(code: str) -> str:
    """Normalise a course code for matching.

    Canvas appends section suffixes such as ' (ND)', and codes may contain
    spaces or slashes ('DATA1001/1901'), so compare on a stripped form.
    """
    text = re.sub(r"\([^)]*\)", "", code or "")
    return re.sub(r"\s+", "", text).upper()


def code_matches(needle: str, code: str) -> bool:
    """True when the user's code matches, exactly or as one side of a pair."""
    want, have = norm_code(needle), norm_code(code)
    if not want or not have:
        return False
    if want == have:
        return True
    return want in have.split("/") or have in want.split("/")
