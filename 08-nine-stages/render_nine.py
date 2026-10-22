import json, base64, subprocess, sys
from playwright.sync_api import sync_playwright
import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DATA = ROOT + 'data/'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
FPS = 30
mode, theme = sys.argv[1], sys.argv[2]
limit = float(sys.argv[3]) if len(sys.argv) > 3 else None
data = json.load(open(DATA + 'zh.json', encoding='utf-8'))
links = json.load(open(DATA + 'links.json', encoding='utf-8'))
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto('file://' + D + 'nine.html')
    pg.evaluate('d => setData(d)', data)
    
    pg.evaluate('document.fonts.ready')
    dur = 60.0
    if mode == 'stills':
        times = [float(x) for x in sys.argv[4].split(',')]
        for t in times:
            pg.evaluate(f'draw({t})'); pg.screenshot(path=OUT + f'land_{t:06.1f}.png')
        print('ok')
    else:
        d = min(dur, limit) if limit else dur
        out = OUT + f'README_nine_stages_{theme}' + (f'_{int(d)}s' if limit else '') + '.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', out], stdin=subprocess.PIPE)
        for i in range(int(d * FPS)):
            url = pg.evaluate(f"(draw({i / FPS}), document.getElementById('c').toDataURL('image/png'))")
            ff.stdin.write(base64.b64decode(url.split(',', 1)[1]))
        ff.stdin.close(); ff.wait()
        print('wrote', out, d)
    b.close()
