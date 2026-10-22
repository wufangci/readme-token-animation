import json, base64, subprocess, sys, time
from playwright.sync_api import sync_playwright
import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.abspath(HERE + '../..') + '/'                # repo root (versions live in 04_active/ or 90_archive/)
DATA = ROOT + '01_source/data/'
TIMING = ROOT + '02_timeline/timing.json'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS = 30; mode = sys.argv[1]
data = json.load(open(DATA + 'zh.json', encoding='utf-8')); links = json.load(open(DATA + 'links.json', encoding='utf-8'))
with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type in ('error',) else None)
    pg.goto('file://' + D + 'nine3d.html')
    pg.evaluate('document.fonts.load("26px \\"Noto Sans CJK TC\\""); document.fonts.load("22px \\"DejaVu Sans Mono\\"")')
    pg.evaluate('document.fonts.ready')
    pg.evaluate('([d, l]) => setData(d, l)', [data, links])
    if mode == 'stills':
        for t in [float(x) for x in sys.argv[2].split(',')]:
            s = time.time(); pg.evaluate(f'draw({t})')
            url = pg.evaluate("document.getElementById('c').toDataURL('image/png')")
            open(OUT + f'd3_{t:05.1f}.png', 'wb').write(base64.b64decode(url.split(',', 1)[1]))
            print(t, round(time.time() - s, 2), 's')
        print('errors', errs[:5])
    else:
        out = OUT + 'README_nine_stages_3d_60s.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(60 * FPS):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
            if i % 300 == 0: print('frame', i, round(time.time() - t0), 's', flush=True)
        ff.stdin.close(); ff.wait(); print('wrote', out, errs[:3])
    b.close()
