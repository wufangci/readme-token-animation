import json, base64, subprocess, sys
from playwright.sync_api import sync_playwright

import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.abspath(HERE + '../..') + '/'                # repo root (versions live in 04_active/ or 90_archive/)
DATA = ROOT + '01_source/data/'
TIMING = ROOT + '02_timeline/timing.json'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS, DUR, RATE = 30, 60.0, 6
mode = sys.argv[1] if len(sys.argv) > 1 else 'video'
toks = json.load(open(DATA + 'zh.json', encoding='utf-8'))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + D + 'list.html')
    pg.evaluate('([d, r]) => setData(d, r)', [toks, RATE])
    pg.evaluate('document.fonts.ready')
    if mode == 'stills':
        for t in [2.0, 30.0]:
            pg.evaluate(f'draw({t})')
            pg.screenshot(path=OUT + f'list_{t:04.1f}.png')
    else:
        out = OUT + 'README_token_vertical.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        n = int(DUR * FPS)
        for i in range(n):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
        ff.stdin.close(); ff.wait()
        print('wrote', out, n, 'frames')
    b.close()
