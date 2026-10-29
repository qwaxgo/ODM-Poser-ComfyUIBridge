# SymbolicPoseEditor-ComfyUIBridge

The ComfyUI bridge for the Symbolic Pose Editor (ComfyUI-SymbolicPoseEditor), as a mod. Private.

`comfyui.js` connects the editor to the **Symbolic Pose Editor** node:

- Confirm / Cancel at the top of the side bar: Confirm sends the pose, the scene, the rough and
  OpenPose pictures and the export size to the node (`symbolic-pose-confirmed`); Cancel closes.
- When the node opens the editor, the pose it holds is loaded (`symbolic-pose-ready` →
  `symbolic-pose-load`).
- The user presets of the node's `user_presets/*.json` appear in the editor.

Messages go only to the page's own origin. Opened from disk (without ComfyUI) it does nothing.
The other side is `web/js/symbolic_pose_editor.js` in the node's repository.

## Install

Clone this repository into the node's `mods/` folder and restart ComfyUI once:

```
cd ComfyUI/custom_nodes/ComfyUI-SymbolicPoseEditor/mods
git clone git@github.com:qwaxgo/SymbolicPoseEditor-ComfyUIBridge.git
```

Without it the editor still opens in the node, but cannot hand the pose back (ComfyUI's console
says so at start). `?nomods` in the editor's address turns it off too.

Uses MOD API 1.1 (`api.io`, `api.ui.addSection({at: "top"})`, `api.presets`): see
`docs/MODDING.md` in the node's repository.

## 日本語

記号ポーズエディタを ComfyUI のノードとつなぐ MOD（非公開）。ノードの `mods/` にこのリポジトリを clone して ComfyUI を
一度再起動すると、エディタの上に「確定して閉じる／閉じる」が出て、確定したポーズ・アタリ画像・OpenPose 画像・書き出しの
大きさがノードに渡ります。ノードが持っていたポーズで開き、`user_presets/` のユーザープリセットも読み込みます。
これがないとエディタはノードの中で開きますが、ポーズをノードに返せません。
