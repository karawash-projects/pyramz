"""Builds a self-contained, interactive HTML gallery of every icon."""

from __future__ import annotations

import json

import pyramz
from pyramz._paths import sharpen
from pyramz._registry import registry


def _icon_data():
    data = []
    for name in pyramz.names():
        d = registry()[name]
        shapes = []
        for s in d.shapes:
            item = {"tag": s.tag, "a": s.attr_dict(), "tone": s.tone, "solid": s.solid, "toneOnly": s.tone_only}
            if s.tag == "path":
                sharp = sharpen(item["a"]["d"])
                if sharp != item["a"]["d"]:
                    item["sd"] = sharp  # corners="sharp" variant, identical to the Python renderer
            shapes.append(item)
        data.append({"name": name, "cat": d.category, "tags": list(d.tags), "shapes": shapes})
    return data


_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pyramz icons</title>
<style>
:root{--bg:#fafaf9;--panel:#fff;--ink:#1c1917;--muted:#78716c;--line:#e7e5e4;--hi:#4f46e5}
@media (prefers-color-scheme:dark){:root{--bg:#0c0a09;--panel:#1c1917;--ink:#f5f5f4;--muted:#a8a29e;--line:#292524;--hi:#818cf8}}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--ink)}
header{padding:28px 32px 8px}h1{margin:0;font-size:22px;letter-spacing:-.01em}header p{margin:4px 0 0;color:var(--muted)}
.bar{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:14px;align-items:center;padding:14px 32px;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar input[type=search]{flex:1 1 220px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink);font:inherit}
.bar label{display:flex;align-items:center;gap:6px;color:var(--muted);font-size:13px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:9px;overflow:hidden}
.seg button{border:0;background:var(--panel);color:var(--muted);padding:7px 11px;font:inherit;font-size:13px;cursor:pointer}
.seg button.on{background:var(--ink);color:var(--bg)}
input[type=color]{width:28px;height:24px;border:0;padding:0;background:none}
main{padding:20px 32px 48px}.cat{margin:22px 0 10px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:10px}
.cell{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 8px 10px;display:flex;flex-direction:column;align-items:center;gap:10px;cursor:pointer;transition:border-color .15s,transform .15s}
.cell:hover{border-color:var(--hi);transform:translateY(-1px)}.cell span{font-size:12px;color:var(--muted);text-align:center;word-break:break-word}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:9px 14px;border-radius:10px;font-size:13px;opacity:0;transition:opacity .2s;pointer-events:none}
.toast.show{opacity:1}.empty{color:var(--muted);padding:40px 0}
</style></head><body>
<header><h1>Pyramz icons</h1><p>__COUNT__ original icons · outline &amp; duotone · click any icon to copy its Python call</p></header>
<div class="bar">
 <input type="search" id="q" placeholder="Search icons, e.g. arrow, money, chat…" autofocus>
 <div class="seg" id="style"><button data-v="outline" class="on">Outline</button><button data-v="duotone">Duotone</button></div>
 <div class="seg" id="corners"><button data-v="round" class="on">Round</button><button data-v="sharp">Sharp</button></div>
 <label>Stroke <input type="range" id="sw" min="1" max="3" step="0.25" value="1.75"><b id="swv">1.75</b></label>
 <label>Size <input type="range" id="sz" min="16" max="48" step="4" value="32"></label>
 <label>Color <input type="color" id="col" value="#1c1917"></label>
 <label>Accent <input type="color" id="acc" value="#4f46e5"></label>
</div>
<main id="out"></main><div class="toast" id="toast"></div>
<script>
const ICONS=__DATA__;
const st={style:"outline",corners:"round",sw:1.75,size:32,color:null,accent:"#4f46e5",q:""};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function svg(ic){const col=st.color||"currentColor",duo=st.style==="duotone",tone=[],line=[];
 for(const s of ic.shapes){const a={...s.a};if(st.corners==="sharp"){if(s.tag==="rect"&&a.rx)a.rx=Math.min(+a.rx,.75);if(s.sd)a.d=s.sd}
  const at=Object.entries(a).map(([k,v])=>` ${k}="${esc(v)}"`).join("");
  if(s.toneOnly){if(duo)tone.push(`<${s.tag}${at} fill="${st.accent}" fill-opacity=".22" stroke="none"/>`);continue}
  if(s.solid){line.push(`<${s.tag}${at} fill="${col}" stroke="none"/>`);continue}
  if(duo&&s.tone)tone.push(`<${s.tag}${at} fill="${st.accent}" fill-opacity=".22" stroke="none"/>`);
  line.push(`<${s.tag}${at}/>`)}
 const r=st.corners==="round";
 return `<svg xmlns="http://www.w3.org/2000/svg" width="${st.size}" height="${st.size}" viewBox="0 0 24 24" fill="none" stroke="${col}" stroke-width="${st.sw}" stroke-linecap="${r?"round":"square"}" stroke-linejoin="${r?"round":"miter"}"${r?"":' stroke-miterlimit="4"'}>${tone.join("")}${line.join("")}</svg>`}
function score(ic,q){if(!q)return 1;if(ic.name===q)return 100;if(ic.name.startsWith(q))return 80;if(ic.name.includes(q))return 60;
 if(ic.tags.includes(q))return 50;if(ic.tags.some(t=>t.startsWith(q)))return 35;if(ic.cat===q)return 20;return 0}
function draw(){const q=st.q.trim().toLowerCase().replace(/[ _]/g,"-"),out=document.getElementById("out");
 const hits=ICONS.map(i=>[score(i,q),i]).filter(x=>x[0]>0);
 if(!hits.length){out.innerHTML='<p class="empty">No icons match that search.</p>';return}
 const groups={};for(const [,i] of hits)(groups[i.cat]??=[]).push(i);
 out.innerHTML=Object.keys(groups).sort().map(c=>`<div class="cat">${c}</div><div class="grid">${groups[c].map(i=>`<div class="cell" data-n="${i.name}" title="${i.tags.join(", ")}">${svg(i)}<span>${i.name}</span></div>`).join("")}</div>`).join("")}
function call(n){const p=[`"${n}"`];if(st.size!==24)p.push(`size=${st.size}`);if(st.sw!==1.75)p.push(`stroke_width=${st.sw}`);
 if(st.style!=="outline")p.push(`style="duotone"`,`accent="${st.accent}"`);if(st.corners!=="round")p.push(`corners="sharp"`);
 if(st.color)p.push(`color="${st.color}"`);return `pyramz.icon(${p.join(", ")})`}
function toast(t){const e=document.getElementById("toast");e.textContent=t;e.classList.add("show");clearTimeout(toast.t);toast.t=setTimeout(()=>e.classList.remove("show"),1600)}
document.getElementById("out").addEventListener("click",e=>{const c=e.target.closest(".cell");if(!c)return;const s=call(c.dataset.n);
 (navigator.clipboard?navigator.clipboard.writeText(s):Promise.reject()).then(()=>toast("Copied: "+s),()=>toast(s))});
for(const id of ["style","corners"])document.getElementById(id).addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;
 st[id]=b.dataset.v;for(const x of b.parentNode.children)x.classList.toggle("on",x===b);draw()});
const on=(id,f)=>document.getElementById(id).addEventListener("input",e=>{f(e.target.value);draw()});
on("q",v=>st.q=v);on("sw",v=>{st.sw=+v;document.getElementById("swv").textContent=v});on("sz",v=>st.size=+v);
on("col",v=>st.color=v);on("acc",v=>st.accent=v);draw();
</script></body></html>"""


def build_gallery() -> str:
    data = _icon_data()
    return _TEMPLATE.replace("__COUNT__", str(len(data))).replace("__DATA__", json.dumps(data, separators=(",", ":")))
