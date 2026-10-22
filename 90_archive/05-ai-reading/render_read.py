import json, base64, subprocess, sys
from playwright.sync_api import sync_playwright

import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.abspath(HERE + '../..') + '/'                # repo root (versions live in 04_active/ or 90_archive/)
DATA = ROOT + '01_source/data/'
TIMING = ROOT + '02_timeline/timing.json'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS, DUR = 30, 44.0
mode = sys.argv[1]            # stills | video
theme = sys.argv[2]           # dark | light
data = json.load(open(DATA + 'zh.json', encoding='utf-8'))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + D + 'read.html')
    pg.evaluate('d => setData(d)', data)
    pg.evaluate(f'setTheme({str(theme == "light").lower()})')
    pg.evaluate('document.fonts.ready')
    if mode == 'stills':
        for t in [4.0, 10.0, 17.0, 26.4, 38.0]:
            pg.evaluate(f'draw({t})')
            pg.screenshot(path=OUT + f'r_{theme}_{t:04.1f}.png')
    else:
        out = OUT + f'README_token_read_{theme}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        for i in range(int(DUR * FPS)):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
        ff.stdin.close(); ff.wait()
        print('wrote', out)
    b.close()
