import json, base64, subprocess, sys
from playwright.sync_api import sync_playwright

import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DATA = ROOT + 'data/'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS, DUR = 30, 30.0
mode = sys.argv[1]            # stills | video
theme = sys.argv[2]           # dark | light
data = json.load(open(DATA + 'anim_v_data.json', encoding='utf-8'))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + D + 'anim_v.html')
    pg.evaluate('d => setData(d)', data)
    pg.evaluate(f'setTheme({str(theme == "light").lower()})')
    pg.evaluate('document.fonts.ready')
    if mode == 'stills':
        for t in [4.5, 10.5, 16.8, 23.6, 25.8]:
            pg.evaluate(f'draw({t})')
            pg.screenshot(path=OUT + f'v_{theme}_{t:04.1f}.png')
    else:
        out = OUT + f'README_token_prototype_vertical_{theme}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        for i in range(int(DUR * FPS)):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
        ff.stdin.close(); ff.wait()
        print('wrote', out)
    b.close()
