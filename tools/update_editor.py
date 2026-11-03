"""Put a release of the editor (ODM Poser) into editor_html/, the copy this bridge serves.

The editor's page is built (Astro), so the bridge keeps the built files of a release: the editor/
folder of the HTML release zip on GitHub Releases, and its version in editor_html/VERSION.
Commit editor_html/ after running this.

    python tools/update_editor.py 0.2.0              the release v0.2.0 from GitHub
    python tools/update_editor.py latest             the newest release
    python tools/update_editor.py --from <zip or folder>
                                                     a zip made by the editor's tools/make_release_html.py,
                                                     or a built folder (holding editor/index.html, as dist/
                                                     after npm run build, or index.html itself)
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "editor_html"
REPO = "qwaxgo/ODM-Poser"


def latest() -> str:
    with urllib.request.urlopen(f"https://api.github.com/repos/{REPO}/releases/latest", timeout=60) as r:
        return json.load(r)["tag_name"].lstrip("v")


def from_zip(data: bytes) -> dict[str, bytes]:
    """The files under <top>/editor/ of a release zip, by their name."""
    out = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in z.namelist():
            parts = name.split("/")
            if len(parts) == 3 and parts[1] == "editor" and parts[2]:
                out[parts[2]] = z.read(name)
    return out


def from_folder(root: Path) -> dict[str, bytes]:
    d = root / "editor" if (root / "editor" / "index.html").is_file() else root
    return {f.name: f.read_bytes() for f in d.iterdir() if f.is_file()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("version", nargs="?", help='a release version such as 0.2.0, or "latest"')
    ap.add_argument("--from", dest="src", help="a release zip or a built folder instead of GitHub")
    a = ap.parse_args()
    if a.src:
        src = Path(a.src)
        files = from_zip(src.read_bytes()) if src.is_file() else from_folder(src)
        version = a.version or f"local ({src.name})"
    elif a.version:
        version = latest() if a.version == "latest" else a.version.lstrip("v")
        url = f"https://github.com/{REPO}/releases/download/v{version}/ODM-Poser-v{version}-html.zip"
        print(f"downloading {url}")
        with urllib.request.urlopen(url, timeout=120) as r:
            files = from_zip(r.read())
    else:
        ap.error("give a version, latest, or --from")
    if "index.html" not in files:
        sys.exit("no editor/index.html there: not a release zip or a built editor")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name, data in sorted(files.items()):
        (OUT / name).write_bytes(data)
    (OUT / "VERSION").write_text(version + "\n", encoding="utf-8", newline="\n")
    print(f"{len(files)} files of the editor {version} -> {OUT.relative_to(HERE)}/")


if __name__ == "__main__":
    main()
