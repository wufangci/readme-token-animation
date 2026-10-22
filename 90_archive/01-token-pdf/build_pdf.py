import json, html
from weasyprint import HTML

import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.abspath(HERE + '../..') + '/'                # repo root (versions live in 04_active/ or 90_archive/)
DATA = ROOT + '01_source/data/'
TIMING = ROOT + '02_timeline/timing.json'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
toks = json.load(open(DATA + 'zh.json', encoding='utf-8'))
n = len(toks)
frag = sum(1 for t in toks if t['str'] is None)
chars = 5945


def show(t):
    if t['str'] is None:
        hx = ' '.join(f'{b:02X}' for b in t['bytes'])
        return f'<span class="frag">‹{hx}›</span>'
    s = t['str']
    out = []
    for ch in s:
        if ch == '\n':
            out.append('<span class="ws">↵</span>')
        elif ch == ' ':
            out.append('<span class="ws">␣</span>')
        else:
            out.append(html.escape(ch))
    return ''.join(out)


rows = []
for t in toks:
    rows.append(f'<div class="row"><span class="tk">[{show(t)}]</span> <span class="id">(ID: {t["id"]})</span></div>')

doc = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 16mm 14mm 16mm 14mm;
  @bottom-center {{ content: "README  ·  " counter(page); font-family: "DejaVu Sans Mono"; font-size: 6.5pt; letter-spacing: .1em; color: #888; }} }}
@page :first {{ @bottom-center {{ content: none; }} }}
body {{ margin: 0; color: #1a1a1a; }}
.cover {{ height: 265mm; display: flex; flex-direction: column; justify-content: center; page-break-after: always; padding: 0 8mm; }}
.cover h1 {{ font-family: "DejaVu Sans Mono"; font-weight: normal; font-size: 30pt; letter-spacing: .25em; margin: 0 0 8mm; }}
.cover .sub {{ font-family: "Noto Serif CJK TC"; font-size: 12pt; letter-spacing: .2em; margin: 0 0 18mm; }}
.stats {{ font-family: "DejaVu Sans Mono", "Noto Sans CJK TC"; font-size: 9pt; line-height: 2; color: #333; }}
.stats b {{ font-weight: normal; color: #000; }}
.note {{ margin-top: 14mm; font-family: "Noto Serif CJK TC"; font-size: 8.5pt; line-height: 1.9; color: #555; max-width: 120mm; }}
.list {{ column-count: 4; column-gap: 6mm; column-fill: auto; }}
.row {{ font-size: 7.4pt; line-height: 1.42; white-space: nowrap; break-inside: avoid; }}
.tk {{ font-family: "Noto Sans CJK TC"; }}
.id {{ font-family: "DejaVu Sans Mono"; font-size: 6.6pt; color: #666; }}
.ws {{ color: #aaa; }}
.frag {{ font-family: "DejaVu Sans Mono"; font-size: 6.4pt; color: #999; }}
</style></head><body>
<section class="cover">
  <h1>README</h1>
  <p class="sub">原始文本的 Token 化樣貌</p>
  <div class="stats">
    {chars:,} 個字元 → <b>{n:,} 個 token</b><br>
    其中 {frag:,} 個是無法單獨成字的位元組碎片 <span class="frag">‹E5 9F›</span><br>
    分詞器：o200k_base（GPT-4o 系列）
  </div>
  <p class="note">每一行是一個 token：方括號內是它代表的文字，ID 是它在詞表中的編號。↵ 代表換行，␣ 代表空格。有些中文字被切成兩片位元組，單獨一片無法顯示為字，以 ‹十六進位› 標示。</p>
</section>
<div class="list">{''.join(rows)}</div>
</body></html>'''
HTML(string=doc).write_pdf(OUT + 'README_tokens.pdf')
print('ok', n, frag)
