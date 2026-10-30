// The ComfyUI hand-off, as a mod (its own repository, cloned into the editor's mods/). Inside
// ComfyUI the node serves it with the other mods; opened from disk it does nothing (no node_id).
//   - user presets: user_presets/*.json, merged by the node into /odm_poser/user_presets.js
//   - the node's modal (?node_id=... in an iframe): it sends the pose it has ("odm-poser-load")
//     once the editor says "odm-poser-ready"; "Confirm" sends the pose, the scene, both
//     pictures and the size ("odm-poser-confirmed"), "Cancel" closes ("odm-poser-cancelled").
//     web/js/odm_poser.js is the other side. Messages go only to this page's origin.
ODMPoser.registerMod({
  id: "comfyui",
  name: "ComfyUI bridge",
  version: "1.0.0",
  api: 1,
  init(api){
    // user presets from the node
    const s = document.createElement("script");
    s.src = "../user_presets.js";
    s.onload = () => { if (Array.isArray(window.USER_POSE_PRESETS) && window.USER_POSE_PRESETS.length) api.presets.add(window.USER_POSE_PRESETS); };
    document.head.appendChild(s);

    // the node's modal
    const nodeId = new URLSearchParams(location.search).get("node_id");
    if (nodeId === null || window.parent === window) return;
    const post = msg => window.parent.postMessage(Object.assign({node_id: nodeId}, msg), location.origin);
    api.i18n.add({"ノードのポーズを読めませんでした。": "Could not read the node's pose.",
      "確定すると、ポーズ・アタリ画像・OpenPose 画像と書き出しの大きさがノードに渡ります。":
        "Confirm hands the pose, the rough and OpenPose pictures and the export size to the node."});
    const sec = api.ui.addSection({title: "ComfyUI", at: "top", html: `
      <div class="btns"><button class="primary" id="comfyui-confirm">確定して閉じる / Confirm</button>
        <button id="comfyui-cancel">閉じる / Cancel</button></div>
      <div class="hint">確定すると、ポーズ・アタリ画像・OpenPose 画像と書き出しの大きさがノードに渡ります。</div>`});
    sec.querySelector("#comfyui-confirm").addEventListener("click", () => {
      const [W, H] = api.io.exportSize();
      post({type: "odm-poser-confirmed", pose_json: api.io.poseJSON(), scene_json: api.io.sceneJSON(),
            openpose: api.io.render("openpose"), atari: api.io.render("atari"), width: W, height: H});
    });
    sec.querySelector("#comfyui-cancel").addEventListener("click", () => post({type: "odm-poser-cancelled"}));
    // the node hands back what was confirmed last time, so the editor opens on it
    window.addEventListener("message", e => {
      const d = e.data || {};
      if (e.origin !== location.origin || d.type !== "odm-poser-load") return;
      try { if (d.pose_json) api.io.loadPose(d.pose_json); } catch (err) { api.say("ノードのポーズを読めませんでした。", true); }
      api.io.setExportSize(d.width, d.height);
    });
    post({type: "odm-poser-ready"});
  },
});
