import json, base64, subprocess, sys, time
from playwright.sync_api import sync_playwright
import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DATA = ROOT + 'data/'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS = 30; mode = sys.argv[1]
data = json.load(open(DATA + 'zh.json')); links = json.load(open(DATA + 'links.json'))
tm = json.load(open(DATA + 'timing.json')); tt = tm['tok_time']; sec = [tt[s] for s in tm['secs'][:-1]]
cfg = {'END': 1200, 'turns': 2,
       'TS': [0.5, sec[1], sec[2], (sec[2] + sec[3]) / 2, sec[3], sec[5], sec[5] + (tm['R1'] - sec[5]) * .3, sec[5] + (tm['R1'] - sec[5]) * .6, tm['R1']]}
def page(pw):
    b = pw.chromium.launch(args=['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + D + 'nine3d_full.html'); pg.evaluate('document.fonts.ready')
    pg.evaluate('(c) => configure(c)', cfg)
    pg.evaluate('([d, l]) => setData(d, l)', [data, links])
    return b, pg, errs
with sync_playwright() as pw:
    b, pg, errs = page(pw)
    if mode == 'stills':
        for t in [float(x) for x in sys.argv[2].split(',')]:
            s = time.time(); url = pg.evaluate(f"(draw({t}), document.getElementById('c').toDataURL('image/png'))")
            open(OUT + f'f3_{t:06.1f}.png', 'wb').write(base64.b64decode(url.split(',', 1)[1])); print(t, round(time.time() - s, 2))
        print(cfg['TS'], errs[:3])
    elif mode == 'bench':
        for t0 in [60, 300, 450, 700, 980, 1050, 1120, 1185]:
            s = time.time()
            for i in range(20): pg.evaluate(f"(draw({t0 + i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            print(t0, round((time.time() - s) / 20, 3), 's/frame')
    else:  # video a b  -> part file
        a, z = int(sys.argv[2]), int(sys.argv[3])
        out = OUT + f'part_{a:05d}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-preset', 'medium', out], stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(a, z):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
            if i % 1500 == 0: print('frame', i, round(time.time() - t0), 's', flush=True)
        ff.stdin.close(); ff.wait(); print('wrote', out, errs[:3], flush=True)
    b.close()
