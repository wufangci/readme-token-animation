import json, base64, subprocess, sys, time
from playwright.sync_api import sync_playwright
import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DATA = ROOT + 'data/'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS = 30
mode, theme = sys.argv[1], sys.argv[2]
data = json.load(open(DATA + 'zh.json', encoding='utf-8'))
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + D + 'read_full.html')
    pg.evaluate('d => setData(d)', data)
    pg.evaluate(f'setTheme({str(theme == "light").lower()})')
    pg.evaluate('document.fonts.ready')
    pg.evaluate('draw(0)')
    dur = pg.evaluate('totalDuration()')
    if mode == 'stills':
        print('duration', dur)
        for t in [30.0, 120.0, 400.0, dur - 12, dur - 6.5]:
            pg.evaluate(f'draw({t})'); pg.screenshot(path=OUT + f'full_{theme}_{t:07.1f}.png')
    elif mode == 'bench':
        t0 = time.time()
        for i in range(150):
            pg.evaluate(f"(draw({300 + i / FPS}), document.getElementById('c').toDataURL('image/png'))")
        print('png fps', 150 / (time.time() - t0))
    else:
        out = OUT + f'README_token_read_full_{theme}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
        n = int(dur * FPS)
        for i in range(n):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
        ff.stdin.close(); ff.wait()
        print('wrote', out, n, 'frames', dur, 's')
    b.close()
