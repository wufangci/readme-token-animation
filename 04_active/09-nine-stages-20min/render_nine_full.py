import json, base64, subprocess, sys, time
from playwright.sync_api import sync_playwright
import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.abspath(HERE + '../..') + '/'                # repo root (versions live in 04_active/ or 90_archive/)
DATA = ROOT + '01_source/data/'
TIMING = ROOT + '02_timeline/timing.json'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS = 30
mode = sys.argv[1]
data = json.load(open(DATA + 'zh.json', encoding='utf-8'))
timing = json.load(open(TIMING, encoding='utf-8'))
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto('file://' + D + 'nine_full.html')
    pg.evaluate('([d, tm]) => setData(d, tm)', [data, timing])
    pg.evaluate('document.fonts.ready')
    pg.evaluate('draw(0)')
    if mode == 'stills':
        for t in [float(x) for x in sys.argv[2].split(',')]:
            pg.evaluate(f'draw({t})'); pg.screenshot(path=OUT + f'nf_{t:07.1f}.png')
        print('ok')
    elif mode == 'bench':
        for t0 in [60, 400, 800, 1000]:
            s = time.time()
            for i in range(60):
                pg.evaluate(f"(draw({t0 + i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            print(t0, 'fps', round(60 / (time.time() - s), 1))
    else:
        out = OUT + 'README_nine_stages_full_light.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
        n = int(1200 * FPS)
        t0 = time.time()
        for i in range(n):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
            if i % 3000 == 0: print('frame', i, round(time.time() - t0), 's', flush=True)
        ff.stdin.close(); ff.wait()
        print('wrote', out)
    b.close()
