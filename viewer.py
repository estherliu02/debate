"""Dialogue viewer — generates a self-contained HTML page and opens it in the browser.

Usage:
    python viewer.py
"""

import json
import webbrowser
from pathlib import Path

ACCEPTED_DIR = Path(__file__).parent / "outputs" / "accepted"
OUT_HTML = Path(__file__).parent / "outputs" / "viewer.html"


def load_dialogues() -> list[dict]:
    files = sorted(ACCEPTED_DIR.glob("*_accepted_dialogue.json"))
    dialogues = []
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        data["_filename"] = f.name
        dialogues.append(data)
    return dialogues


def build_html(dialogues: list[dict]) -> str:
    data_json = json.dumps(dialogues, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Debate Viewer</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: #f0f2f5; min-height: 100vh; }}

  /* ── top bar ── */
  header {{ background: #1c1c2e; color: #fff; padding: 14px 28px;
            display: flex; align-items: center; justify-content: space-between;
            position: sticky; top: 0; z-index: 10; box-shadow: 0 2px 8px rgba(0,0,0,.3); }}
  header h1 {{ font-size: 16px; font-weight: 600; letter-spacing: .5px; }}
  .nav {{ display: flex; align-items: center; gap: 10px; }}
  .nav button {{ background: #e94560; border: none; color: #fff;
                 padding: 7px 18px; border-radius: 20px; cursor: pointer;
                 font-size: 13px; font-weight: 500; transition: opacity .15s; }}
  .nav button:disabled {{ opacity: .35; cursor: default; }}
  .nav button:not(:disabled):hover {{ opacity: .85; }}
  .nav .counter {{ font-size: 13px; color: #aaa; min-width: 60px; text-align: center; }}

  /* ── meta card ── */
  .meta {{ margin: 24px 28px 0; background: #fff; border-radius: 12px;
           padding: 18px 22px; box-shadow: 0 1px 4px rgba(0,0,0,.07); }}
  .meta h2 {{ font-size: 15px; color: #1c1c2e; line-height: 1.4; margin-bottom: 10px; }}
  .tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .tag {{ background: #f0f2f5; border-radius: 20px; padding: 3px 12px;
          font-size: 12px; color: #555; }}
  .tag b {{ color: #1c1c2e; }}
  .filename {{ margin-top: 8px; font-size: 11px; color: #bbb; }}

  /* ── chat ── */
  .chat {{ margin: 16px 28px 40px; display: flex; flex-direction: column; gap: 14px; }}
  .turn {{ display: flex; gap: 10px; align-items: flex-start; }}
  .turn.B {{ flex-direction: row-reverse; }}
  .avatar {{ width: 34px; height: 34px; border-radius: 50%;
             display: flex; align-items: center; justify-content: center;
             font-weight: 700; font-size: 14px; flex-shrink: 0; margin-top: 2px; }}
  .turn.A .avatar {{ background: #e94560; color: #fff; }}
  .turn.B .avatar {{ background: #1c1c2e; color: #fff; }}
  .bubble-wrap {{ display: flex; flex-direction: column; max-width: 62%; }}
  .turn.B .bubble-wrap {{ align-items: flex-end; }}
  .turn-label {{ font-size: 11px; color: #aaa; margin-bottom: 4px; }}
  .bubble {{ background: #fff; border-radius: 14px; padding: 11px 15px;
             line-height: 1.65; font-size: 14px; color: #333;
             box-shadow: 0 1px 4px rgba(0,0,0,.07); }}
  .turn.B .bubble {{ background: #1c1c2e; color: #e8e8e8; }}
</style>
</head>
<body>

<header>
  <h1>Debate Viewer</h1>
  <div class="nav">
    <button id="btn-prev" onclick="go(-1)">&#8592; Prev</button>
    <span class="counter" id="counter"></span>
    <button id="btn-next" onclick="go(1)">Next &#8594;</button>
  </div>
</header>

<div class="meta" id="meta"></div>
<div class="chat" id="chat"></div>

<script>
const DATA = {data_json};
let idx = 0;

function go(dir) {{
  idx = Math.max(0, Math.min(DATA.length - 1, idx + dir));
  render();
}}

function render() {{
  const d = DATA[idx];
  document.getElementById('counter').textContent = (idx + 1) + ' / ' + DATA.length;
  document.getElementById('btn-prev').disabled = idx === 0;
  document.getElementById('btn-next').disabled = idx === DATA.length - 1;

  document.getElementById('meta').innerHTML = `
    <h2>${{d.topic}}</h2>
    <div class="tags">
      <span class="tag"><b>Trait:</b> ${{d.trait_name}}</span>
      <span class="tag"><b>Variant A:</b> ${{d.variant_name_a}}</span>
      <span class="tag"><b>Variant B:</b> ${{d.variant_name_b ?? '—'}}</span>
      <span class="tag"><b>Turns:</b> ${{d.turns.length}}</span>
    </div>
    <div class="filename">${{d._filename}}</div>
  `;

  document.getElementById('chat').innerHTML = d.turns.map(t => `
    <div class="turn ${{t.speaker}}">
      <div class="avatar">${{t.speaker}}</div>
      <div class="bubble-wrap">
        <div class="turn-label">Turn ${{t.turn_id}}</div>
        <div class="bubble">${{t.utterance}}</div>
      </div>
    </div>
  `).join('');

  window.scrollTo(0, 0);
}}

render();
</script>
</body>
</html>"""


if __name__ == "__main__":
    dialogues = load_dialogues()
    if not dialogues:
        print("No accepted dialogues found in outputs/accepted/")
        raise SystemExit(1)

    OUT_HTML.write_text(build_html(dialogues), encoding="utf-8")
    print(f"Loaded {len(dialogues)} dialogue(s). Opening viewer...")
    webbrowser.open(OUT_HTML.as_uri())
