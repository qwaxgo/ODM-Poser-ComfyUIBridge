"""Where things are: the editor (ODM Poser), the mods, the user's presets.

The editor is the built release in `editor_html/` (tools/update_editor.py puts it there) unless
config.json names another folder:

    {"editor": "C:/AI/ODM-Poser/dist", "mods": ["C:/AI/ODM-Poser/mods"]}

("editor": a built editor, for working on the editor itself: a checkout's dist/ after npm run build,
an unzipped HTML release, or the folder holding index.html; "mods": more mod folders, read after
this bridge's own `mods/`.) config.json is optional and stays out of git.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config.json"
EDITOR_HTML = HERE / "editor_html"
USER_PRESETS = HERE / "user_presets"
BRIDGE_MOD = HERE / "mod" / "comfyui.js"
BRIDGE_NAME = "_bridge/comfyui.js"            # how the editor's list calls it (loaded first)
MOD_PART = re.compile(r"^[\w.-]+$")


def settings() -> dict:
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def editor_dir() -> Path:
    """The editor's page and scripts: editor_html/, or the built editor config.json names (its
    editor/ first, as dist/ and an unzipped release both have an index.html of their own beside it;
    then a checkout's dist/editor/, then the folder itself)."""
    p = settings().get("editor")
    if not p:
        return EDITOR_HTML
    root = Path(p).expanduser()
    for d in (root / "editor", root / "dist" / "editor", root):
        if (d / "index.html").is_file():
            return d
    return root


def editor_version() -> str:
    """The version in editor_html/VERSION ("" for an editor named in config.json)."""
    if settings().get("editor"):
        return ""
    try:
        return (EDITOR_HTML / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def mod_dirs() -> list[Path]:
    return [HERE / "mods"] + [Path(p).expanduser() for p in settings().get("mods", []) if isinstance(p, str)]


def mod_files() -> dict[str, Path]:
    """The mods the editor loads, in order: this bridge's own, then *.js and <folder>/*.js of each
    mod folder (a name starting with "_" or "." is left out; the first of a name wins)."""
    out = {BRIDGE_NAME: BRIDGE_MOD} if BRIDGE_MOD.is_file() else {}
    for root in mod_dirs():
        if not root.is_dir():
            continue
        found = []
        for f in root.rglob("*.js"):
            parts = f.relative_to(root).parts
            if len(parts) <= 2 and all(MOD_PART.match(p) and not p.startswith(("_", ".")) for p in parts):
                found.append(("/".join(parts), f))
        for name, f in sorted(found):
            out.setdefault(name, f)
    return out
