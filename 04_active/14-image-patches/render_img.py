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
meta = json.load(open(D + 'img/meta.json'))
with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto('file://' + D + 'img3d.html'); pg.evaluate('document.fonts.ready')
    pg.evaluate('(m) => init(m)', meta)
    if mode == 'stills':
        for t in [float(x) for x in sys.argv[2].split(',')]:
            url = pg.evaluate(f"(draw({t}), document.getElementById('c').toDataURL('image/png'))")
            open(OUT + f'i3_{t:05.1f}.png', 'wb').write(base64.b64decode(url.split(',', 1)[1]))
        print('errors', errs[:5])
    else:
        out = OUT + 'README_image_patches_3d_30s.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', out], stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(30 * FPS):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
            if i % 150 == 0: print('frame', i, round(time.time() - t0), flush=True)
        ff.stdin.close(); ff.wait(); print('wrote', out, errs[:3])
    b.close()
