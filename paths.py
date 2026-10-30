"""Where things are: the editor (ODM Poser), the mods, the user's presets.

The editor is the git submodule `editor/` unless config.json names another folder:

    {"editor": "C:/AI/ODM-Poser", "mods": ["C:/AI/ODM-Poser/mods"]}

("editor": a checkout of ODM-Poser, for working on the editor itself; "mods": more mod folders,
read after this bridge's own `mods/`.) config.json is optional and stays out of git.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config.json"
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


def editor_root() -> Path:
    p = settings().get("editor")
    return Path(p).expanduser() if p else HERE / "editor"


def editor_dir() -> Path:
    """The editor's page and scripts (web/editor/ of the editor's folder)."""
    return editor_root() / "web" / "editor"


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
