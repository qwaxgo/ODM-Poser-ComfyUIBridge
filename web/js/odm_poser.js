// ODM Poser: the node's button opens the editor in a modal; "Confirm" in the
// editor sends the pose, the scene and the two pictures back into the node's hidden values.
import { app } from "../../scripts/app.js";

const NODES = new Set(["ODMPoser", "SymbolicPoseEditor"]);   // the old name: saved workflows
const EDITOR = "/odm_poser/editor/index.html";
const MODAL = "odm-poser-modal";
const VALUES = ["pose_json", "scene_json", "openpose_image", "atari_image"];

function hiddenValue(node, name) {
  let w = node.widgets?.find((x) => x.name === name);
  if (!w) w = node.addWidget("text", name, "", () => {}, { serialize: true });
  w.type = "hidden";
  w.serialize = true;
  w.computeSize = () => [0, -4];
  w.draw = () => {};
  return w;
}

function statusText(node) {
  const pose = node.__spe.pose_json.value || "";
  if (!pose) return "(未確定 / not confirmed)";
  try {
    JSON.parse(pose);
    const items = JSON.parse(node.__spe.scene_json.value || "{}").items || [];
    return `確定済み / confirmed${items.length ? ` · ${items.length} props` : ""}`;
  } catch (e) {
    return "confirmed";
  }
}

function setup(node) {
  if (node.__spe) return;
  node.__spe = {};
  for (const name of VALUES) node.__spe[name] = hiddenValue(node, name);
  const status = node.addWidget("text", "status", "", () => {}, { serialize: false });
  status.disabled = true;
  node.__spe.status = status;
  node.addWidget("button", "Open ODM Poser", null, () => openEditor(node));
  node.__spe.refresh = () => {
    status.value = statusText(node);
    node.setDirtyCanvas?.(true, true);
  };
  node.__spe.refresh();
  const configure = node.onConfigure;
  node.onConfigure = function () {
    const r = configure?.apply(this, arguments);
    node.__spe.refresh();
    return r;
  };
  if (node.size?.[0] < 260) node.size[0] = 280;
}

// The modal in melta UI's values (design/melta-ui: components/modal.md, foundations/elevation.md):
// a black/50 backdrop, a rounded-xl frame with a slate-200 border and the overlay shadow, a 40px
// icon button to close it (Charcoal "Close", aria-label, a primary focus ring). It lives in ComfyUI's
// page, where Tailwind would reach ComfyUI's own UI, so these few rules stay scoped CSS (spe-*).
function styles() {
  if (document.getElementById("spe-styles")) return;
  const s = document.createElement("style");
  s.id = "spe-styles";
  s.textContent = `
.spe-backdrop{position:fixed;inset:0;background:rgb(0 0 0 / .5);z-index:99999;display:flex;align-items:center;justify-content:center}
.spe-frame{position:relative;width:96vw;height:94vh;background:#f9fafb;border:1px solid #e2e8f0;border-radius:.75rem;overflow:hidden;
  box-shadow:0 20px 25px -5px rgb(0 0 0 / .1),0 8px 10px -6px rgb(0 0 0 / .1)}
.spe-frame>iframe{width:100%;height:100%;border:0;display:block}
.spe-close{position:absolute;top:8px;right:8px;z-index:2;width:40px;height:40px;display:inline-flex;align-items:center;justify-content:center;
  border:1px solid #e2e8f0;border-radius:.5rem;background:#fff;color:#64748b;cursor:pointer;transition:color .15s,background-color .15s}
.spe-close:hover{color:#3d4b5f;background:#f9fafb}
.spe-close:focus-visible{outline:none;box-shadow:0 0 0 2px rgb(43 112 239 / .5)}
.spe-close svg{width:20px;height:20px}
@media (prefers-color-scheme:dark){
  .spe-frame{background:#161718;border-color:#373839}
  .spe-close{background:#1b1c1d;border-color:#373839;color:#a3a3a3}
  .spe-close:hover{color:#eee;background:#232525}
}
@media (prefers-reduced-motion:reduce){.spe-close{transition:none}}`;
  document.head.appendChild(s);
}
const CLOSE_ICON = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8.414 5.586a2 2 0 10-2.828 2.828L9.172 12l-3.586 3.586a2 2 0 102.828 2.828L12 14.828l3.586 3.586a2 2 0 102.828-2.828L14.828 12l3.586-3.586a2 2 0 10-2.828-2.828L12 9.172 8.414 5.586z" fill="currentColor"/></svg>';

function closeEditor() {
  document.getElementById(MODAL)?.remove();
}

function openEditor(node) {
  styles();
  closeEditor();
  const back = document.createElement("div");
  back.className = "spe-backdrop";
  back.id = MODAL;
  back.setAttribute("role", "dialog"); back.setAttribute("aria-modal", "true"); back.setAttribute("aria-label", "ODM Poser");
  back.innerHTML = `<div class="spe-frame"><button type="button" class="spe-close" aria-label="Close (Esc)" title="Close (Esc)">${CLOSE_ICON}</button>
    <iframe src="${EDITOR}?node_id=${encodeURIComponent(node.id)}&_t=${Date.now()}"></iframe></div>`;
  back.querySelector(".spe-close").addEventListener("click", closeEditor);
  back.addEventListener("keydown", (e) => { if (e.key === "Escape") closeEditor(); });
  document.body.appendChild(back);
  back.tabIndex = -1;
  back.focus();
}

window.addEventListener("message", (e) => {
  const d = e.data || {};
  if (e.origin !== window.location.origin || typeof d.type !== "string" || !d.type.startsWith("odm-poser-")) return;
  const node = app.graph?.getNodeById?.(Number(d.node_id));
  if (!node || !NODES.has(node.comfyClass) || !node.__spe) return;
  if (d.type === "odm-poser-ready") {
    // open on what was confirmed last time
    const frame = document.querySelector(`#${MODAL} iframe`);
    frame?.contentWindow?.postMessage({ type: "odm-poser-load",
      pose_json: node.__spe.pose_json.value || "" }, window.location.origin);
    return;
  }
  if (d.type === "odm-poser-cancelled") { closeEditor(); return; }
  if (d.type !== "odm-poser-confirmed" || typeof d.pose_json !== "string") return;
  node.__spe.pose_json.value = d.pose_json;
  node.__spe.scene_json.value = d.scene_json || "{}";
  node.__spe.openpose_image.value = d.openpose || "";
  node.__spe.atari_image.value = d.atari || "";
  node.__spe.refresh();
  app.graph?.setDirtyCanvas?.(true, true);
  closeEditor();
});

app.registerExtension({
  name: "ODMPoser.node",
  async nodeCreated(node) {
    if (NODES.has(node.comfyClass)) setup(node);
  },
  async loadedGraphNode(node) {
    if (NODES.has(node.comfyClass)) {
      setup(node);
      node.__spe.refresh();
    }
  },
});
