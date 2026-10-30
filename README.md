# ODM Poser for ComfyUI（立体人形装置 ComfyUI 連携）

立体人形装置（英語名 ODM Poser：Omni-Directional Mannequin Poser）を、ComfyUI のノードとして使うためのリポジトリです。
**このリポジトリだけで ComfyUI への導入が終わります。** ポーズエディタ本体（[ODM-Poser](https://github.com/qwaxgo/ODM-Poser)）は、
git のサブモジュール `editor/` として一緒に入ります。

[English below](#english)

## できること

- ノード「ODM Poser」を置き、「Open ODM Poser」を押すと、ComfyUI の中でポーズエディタが開きます。
- エディタで「確定して閉じる」を押すと、ポーズ・アタリ画像・OpenPose 画像・画像の大きさがノードに渡ります。
- 次にエディタを開くと、前に確定したポーズから続けて編集できます（ワークフローに保存されます）。
- `user_presets/` に置いた自分のプリセットが、エディタの「ユーザープリセット」に並びます。
- `mods/` に置いた MOD が、エディタで読み込まれます。

## 入れ方

必要なもの：ComfyUI と git。追加の Python パッケージは要りません（ComfyUI の numpy・torch・Pillow・aiohttp だけを使います）。

### git で入れる

```
cd ComfyUI/custom_nodes
git clone --recursive https://github.com/qwaxgo/ODM-Poser-ComfyUIBridge
```

Windows のポータブル版なら、たとえば `C:\AI\ComfyUI_windows_portable\ComfyUI\custom_nodes` で実行します。
そのあと ComfyUI を再起動します。

`--recursive` を付け忘れても、ComfyUI の最初の起動時にエディタ本体を自動で取ってきます（git が必要です）。

### ComfyUI-Manager で入れる

ComfyUI-Manager の「Install via Git URL」に `https://github.com/qwaxgo/ODM-Poser-ComfyUIBridge` を入れ、ComfyUI を再起動します。

### 入れたあとのフォルダ

```
ComfyUI/custom_nodes/ODM-Poser-ComfyUIBridge/
  __init__.py  nodes.py  routes.py  paths.py   ノードと、エディタを ComfyUI に出す部分
  web/js/odm_poser.js                          ノードの「Open ODM Poser」ボタンと窓
  mod/comfyui.js                               エディタ側の受け渡し（「確定して閉じる」など）
  editor/                                      ポーズエディタ本体（サブモジュール）
  user_presets/                                自分のプリセット（git に入りません）
  mods/                                        自分の MOD（git に入りません）
```

## 入ったか確かめる

1. ComfyUI の起動時のコンソールに `[ODM Poser] the editor is missing` が出ていないこと。
2. キャンバスを右クリック →「Add Node」→「ODM Poser」→「ODM Poser」でノードを置く（ダブルクリックで「ODM Poser」を検索しても置けます）。
3. 「Open ODM Poser」を押すとエディタが開き、右側の欄のいちばん上に「ComfyUI」の欄（「確定して閉じる」「閉じる」）があれば完了です。

## 使い方

1. ノードを置き、「Open ODM Poser」を押す。
2. ポーズを作る。書き出しの「幅」「高さ」が、ノードが出す画像の大きさになります。
3. 「確定して閉じる」を押す（「閉じる」は渡さずに閉じます）。
4. ノードの出力を、ほかのノードにつなぐ。

| 出力 | 型 | 中身 |
|------|----|------|
| `pose_json` | STRING | 人物（19 関節の位置 cm、体の向き、ひねり、手の形、固定、カメラなど。複数の人物も） |
| `scene_json` | STRING | 小物、床・壁・天井、ワイヤー、物体 |
| `openpose` | IMAGE | OpenPose の画像（体 18 点＋両手 21 点ずつ、標準の色、黒い背景）。ControlNet（OpenPose）に |
| `atari` | IMAGE | アタリ画像（白地に線と丸、小物も簡単な形で）。下描きや img2img に |
| `width`、`height` | INT | エディタで決めた書き出しの大きさ |

`scene_json` は `{"items": [...], "env": {...}, "wire": {...}, "solids": [...]}` です。

## ユーザープリセット

`user_presets/` に `*.json` を置くと、エディタの「ユーザープリセット」に並びます（形式は `user_presets/README.md`）。
置いたあとはエディタを開き直すだけです。

## MOD

`mods/` に MOD（`*.js`、または MOD のリポジトリを clone したフォルダ）を置くと、エディタで読み込まれます。たとえばサンプル MOD：

```
cd ComfyUI/custom_nodes/ODM-Poser-ComfyUIBridge/mods
git clone https://github.com/qwaxgo/ODM-Poser-SampleMods
```

エディタの MOD 欄の「ファイルから入れる」「URLから追加」で入れた MOD も、そのブラウザでは使えます。
MOD はエディタの中で自由に動くプログラムなので、信頼できるものだけを入れてください。

## アプリとして使う

ブラウザのタブで `http://127.0.0.1:8188/odm_poser/editor/index.html` を開き、右上の「アプリとして追加」を押すと、
パソコンにアプリとして追加できます（Chrome・Edge など。ノードの窓の中からは追加できません）。

## 更新する

```
cd ComfyUI/custom_nodes/ODM-Poser-ComfyUIBridge
git pull
git submodule update --init --recursive
```

そのあと ComfyUI を再起動します。ComfyUI-Manager の「Update」でも更新できます。

## 設定（なくてもよい）

`config.json`（`config.example.json` が見本）で、エディタ本体の場所と、MOD のフォルダを足せます。エディタ本体を自分で手直しするときに、
そのフォルダを `"editor"` に書きます。`config.json` は git に入りません。

```json
{"editor": "C:/AI/ODM-Poser", "mods": ["C:/AI/ODM-Poser/mods"]}
```

## うまくいかないとき

| 症状 | 原因と対処 |
|------|-----------|
| ノードの窓が空白・コンソールに `the editor is missing` | エディタ本体がありません。このフォルダで `git submodule update --init` を実行して ComfyUI を再起動 |
| ノードの一覧に「ODM Poser」がない | ComfyUI を再起動する。コンソールに読み込みのエラーが出ていないか確かめる |
| 「確定して閉じる」がない | エディタのアドレスに `?nomods` が付いていると、この部分も止まります |
| 実行すると「ポーズがまだありません」 | エディタで一度も「確定して閉じる」を押していません |
| MOD 欄に ✗ が出る | その MOD にエラーがあります。✗ の行に理由が出ます |

以前の名前のノード（Symbolic Pose Editor）を使ったワークフローも、そのまま開いて実行できます。

## ComfyUI なしで使う

ポーズエディタ本体だけでも使えます（ブラウザ・アプリ・スマホ）：[ODM-Poser](https://github.com/qwaxgo/ODM-Poser)。

## Claude Code での実装について

このリポジトリのコードとドキュメントは、qwaxgo の設計と指示のもとで、Anthropic の AI コーディングツール
[Claude Code](https://claude.com/claude-code) が実装しました。

## ライセンス

MIT（c）2026 qwaxgo。`LICENSE` を見てください。

---

## English

The repository for using **ODM Poser** (Omni-Directional Mannequin Poser; Japanese name 立体人形装置) as
a ComfyUI node. **This repository alone installs it in ComfyUI**: the pose editor itself
([ODM-Poser](https://github.com/qwaxgo/ODM-Poser)) comes as the git submodule `editor/`.

**What it does.** Add the node "ODM Poser", press **Open ODM Poser** and the editor opens inside
ComfyUI. **確定して閉じる / Confirm** hands the pose, the rough and OpenPose pictures and the size to
the node, which keeps them in the workflow and reopens on them. Presets in `user_presets/` and mods
in `mods/` are loaded by the editor.

**Install.** You need ComfyUI and git; no extra Python packages.

```
cd ComfyUI/custom_nodes
git clone --recursive https://github.com/qwaxgo/ODM-Poser-ComfyUIBridge
```

Then restart ComfyUI. Without `--recursive` the editor is fetched at the first start. With
ComfyUI-Manager: **Install via Git URL** with the address above, then restart.

**Check.** No `[ODM Poser] the editor is missing` in the console; the node is under Add Node →
ODM Poser; its window starts with a "ComfyUI" section (Confirm / Cancel).

| output | type | what it is |
|--------|------|------------|
| `pose_json` | STRING | the figure(s): 19 joints (cm), body turn, twists, hand shapes, pins, camera |
| `scene_json` | STRING | props, floor / walls / ceiling, wire, solids |
| `openpose` | IMAGE | COCO-18 body + 2 × 21 hand points, standard colours, black background |
| `atari` | IMAGE | the rough: lines and circles on white |
| `width`, `height` | INT | the export size set in the editor |

**Presets and mods.** `user_presets/*.json` (format in `user_presets/README.md`) and mods in `mods/`
(e.g. `git clone https://github.com/qwaxgo/ODM-Poser-SampleMods` there); reopen the editor after adding.
Install only mods you trust.

**As an app.** Open `http://127.0.0.1:8188/odm_poser/editor/index.html` in a browser tab and press
**Install as an app**.

**Update.** `git pull` and `git submodule update --init --recursive` in this folder, then restart
ComfyUI (or ComfyUI-Manager's Update).

**Settings (optional).** `config.json` (see `config.example.json`) can name the editor's folder
(`"editor"`, for working on the editor) and more mod folders (`"mods"`). It is not committed.

**Troubleshooting.** An empty window or `the editor is missing`: run `git submodule update --init`
here and restart. No node: restart ComfyUI and check the console. No Confirm: `?nomods` in the
address turns it off. "no pose yet": press Confirm once. Workflows with the old node name
(Symbolic Pose Editor) still load.

**Built with Claude Code.** The code and documents of this repository were implemented by
[Claude Code](https://claude.com/claude-code), Anthropic's AI coding tool, under qwaxgo's design and
direction.

**License.** MIT, (c) 2026 qwaxgo.
