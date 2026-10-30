# SymbolicPoseEditor-ComfyUIBridge

記号ポーズエディタを ComfyUI のノードとして使うための部品です（非公開）。

## これは何か

ポーズエディタ本体は、ComfyUI がなくても動く単体の道具です。このリポジトリの `comfyui.js` は、
エディタとノード「Symbolic Pose Editor」の間をつなぐ部品（MOD）です。入れると、次のことができるようになります。

- ノードから開いたエディタに「確定して閉じる」「閉じる」ボタンが出る
- 「確定して閉じる」を押すと、作ったポーズ・アタリ画像・OpenPose 画像・画像の大きさがノードに送られる
- 次にノードからエディタを開くと、前に確定したポーズから続けられる
- ノードの `user_presets/` に置いたプリセットが、エディタの一覧に出る

入れないと、ノードからエディタは開きますが、ボタンが出ず、ポーズをノードに送れません。
ComfyUI を使わずにエディタを直接開いたときは、この部品は何もしません。

## 入れ方

導入の手順はノードのリポジトリの **`docs/COMFYUI-JA.md`** にまとめてあります。要点だけ書くと：

```
cd ComfyUI/custom_nodes/ComfyUI-SymbolicPoseEditor/mods
git clone git@github.com:qwaxgo/SymbolicPoseEditor-ComfyUIBridge.git
```

そのあと ComfyUI を一度再起動します。

## English

The piece that connects the Symbolic Pose Editor to its ComfyUI node (private). With it, the editor
opened from the node gets Confirm / Cancel buttons; Confirm sends the pose, the rough and OpenPose
pictures and the size to the node, the editor reopens on the confirmed pose, and the node's
`user_presets/` appear in the editor. Without it the editor opens but cannot send anything back.
Install: clone this repository into the node's `mods/` folder and restart ComfyUI once; the full
guide is `docs/COMFYUI.md` in the node's repository. It uses MOD API 1.1 (`api.io`, `api.ui`,
`api.presets`); messages go only to the page's own origin.
