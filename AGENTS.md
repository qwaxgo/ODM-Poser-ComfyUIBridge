# ODM-Poser-ComfyUIBridge — notes for AI coding agents

The UI follows **melta UI** (`design/melta-ui`, a git submodule; read `design/melta-ui/DESIGN.md`).

- The editor itself (the `editor/` submodule, ODM-Poser) carries its own melta setup (its
  `AGENTS.md`, `web/editor/ui.js`, `ui.css`): change the editor's look there, not here.
- This repository's own UI is the node's modal (`web/js/odm_poser.js`): it lives in ComfyUI's page,
  where Tailwind would reach ComfyUI's own UI, so it keeps a few scoped rules (`spe-*`) written in
  melta's values (black/50 backdrop, rounded-xl frame with a slate-200 border and the overlay
  shadow, a 40px icon button with aria-label and a primary-500/50 focus ring; dark values follow
  `prefers-color-scheme`). Keep new UI in those values and scoped.
- ComfyUI's own node widgets (the button on the node) are ComfyUI's look and stay so.
