"""Web routes: the editor, its mods and the user's presets, for the node's window.

    /odm_poser/editor/<file>       the editor's files (paths.editor_dir())
    /odm_poser/user_presets.js     window.USER_POSE_PRESETS from user_presets/*.json
    /odm_poser/mods.js             window.ODM_POSER_MODS: this bridge's mod first, then the mod folders
    /odm_poser/mods/<path>         one of them
"""

from __future__ import annotations

import json
from pathlib import Path

from .paths import USER_PRESETS, editor_dir, mod_files

TYPES = {".html": "text/html", ".js": "application/javascript", ".webmanifest": "application/manifest+json",
         ".svg": "image/svg+xml", ".png": "image/png", ".json": "application/json"}


def user_presets():
    """Every preset of user_presets/*.json: each file is a list of {group, name, P} or
    {"presets": [...]}; a file's name becomes the group when a preset has none."""
    out = []
    for f in sorted(USER_PRESETS.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"[ODM Poser] skipped {f.name}: {exc}")
            continue
        items = data.get("presets", []) if isinstance(data, dict) else data
        for p in items if isinstance(items, list) else []:
            if isinstance(p, dict) and isinstance(p.get("P"), list):
                out.append({"group": str(p.get("group") or f.stem), "name": str(p.get("name") or ""),
                            "P": p["P"]})
    return out


try:
    from aiohttp import web
    from server import PromptServer

    routes = PromptServer.instance.routes

    def _js(text):
        return web.Response(text=text, content_type="application/javascript")

    @routes.get("/odm_poser/user_presets.js")
    async def _user_presets(request):
        return _js("window.USER_POSE_PRESETS = " + json.dumps(user_presets(), ensure_ascii=False,
                                                              separators=(",", ":")) + ";\n")

    @routes.get("/odm_poser/mods.js")
    async def _mods_list(request):
        return _js("window.ODM_POSER_MODS = " + json.dumps(list(mod_files())) + ";\n")

    @routes.get("/odm_poser/mods/{path:.+}")
    async def _mod_file(request):
        f = mod_files().get(request.match_info["path"])     # only the listed files
        if f is None:
            raise web.HTTPNotFound()
        return _js(f.read_text(encoding="utf-8"))

    @routes.get("/odm_poser/editor")
    async def _editor_root(request):
        raise web.HTTPFound("/odm_poser/editor/index.html" + (f"?{request.query_string}"
                                                              if request.query_string else ""))

    @routes.get("/odm_poser/editor/{name}")
    async def _editor_file(request):
        root = editor_dir().resolve()
        f = (root / request.match_info["name"]).resolve()
        if f.parent != root or f.suffix not in TYPES or not f.is_file():   # the editor's own files only
            raise web.HTTPNotFound()
        if f.suffix == ".png":
            return web.FileResponse(f)
        return web.Response(text=f.read_text(encoding="utf-8"), content_type=TYPES[f.suffix])
except Exception as exc:            # outside ComfyUI (tests, a plain import)
    print(f"[ODM Poser] web routes not registered: {exc}")
