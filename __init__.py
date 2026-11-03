"""ODM Poser for ComfyUI: the node "ODM Poser", and the bridge between it and the editor.

This repository is all ComfyUI needs. The editor (ODM Poser, 立体人形装置) comes with it, built, in
`editor_html/` (a release of the editor, put there by tools/update_editor.py). The node's button
opens the editor in a window; "Confirm" hands the pose, the scene and two pictures (OpenPose, the
line-and-circle rough) back to the node.
"""

from __future__ import annotations

from .paths import HERE, editor_dir, editor_version


def _check_editor():
    d = editor_dir()
    if not (d / "index.html").is_file():
        print(f"[ODM Poser] the editor is missing at {d}. Update this folder ({HERE}) with git pull, "
              "or fix \"editor\" in config.json. The node loads, but its window stays empty.")
    elif editor_version():
        print(f"[ODM Poser] editor {editor_version()}")
    else:
        print(f"[ODM Poser] editor from config.json: {d}")


_check_editor()

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS  # noqa: E402
from . import routes  # noqa: E402,F401  (the editor's web routes)

WEB_DIRECTORY = "./web/js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
