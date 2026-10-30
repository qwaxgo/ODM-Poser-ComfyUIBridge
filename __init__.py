"""ODM Poser for ComfyUI: the node "ODM Poser", and the bridge between it and the editor.

This repository is all ComfyUI needs. The editor (ODM Poser, 立体人形装置) comes with it as the git
submodule `editor/`; when a clone left it out, it is fetched here at the first start. The node's
button opens the editor in a window; "Confirm" hands the pose, the scene and two pictures (OpenPose,
the line-and-circle rough) back to the node.
"""

from __future__ import annotations

import shutil
import subprocess

from .paths import HERE, editor_dir


def _ensure_editor():
    if (editor_dir() / "index.html").is_file():
        return
    if (HERE / ".gitmodules").is_file() and shutil.which("git"):
        print("[ODM Poser] fetching the editor: git submodule update --init --recursive")
        try:
            subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=HERE, timeout=600, check=False)
        except (OSError, subprocess.SubprocessError) as exc:
            print(f"[ODM Poser] could not fetch the editor: {exc}")
    if not (editor_dir() / "index.html").is_file():
        print(f"[ODM Poser] the editor is missing. In {HERE} run: git submodule update --init "
              "(or name an editor folder in config.json). The node loads, but its window stays empty.")


_ensure_editor()

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS  # noqa: E402
from . import routes  # noqa: E402,F401  (the editor's web routes)

WEB_DIRECTORY = "./web/js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
