from playwright.sync_api import sync_playwright
import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DATA = ROOT + 'data/'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream', '--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 1440, 'height': 810})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append('console ' + m.text) if m.type == 'error' else None)
    pg.goto('file://' + HERE + 'README_live.html')
    pg.screenshot(path=OUT + 'live_0.png')
    pg.click('#go')
    pg.wait_for_timeout(6000)
    c1 = pg.evaluate('st.c'); lvl = pg.evaluate('st.level'); mic = pg.evaluate('!!st.analyser')
    pg.keyboard.press('h')
    pg.keyboard.press('Space')
    c2 = pg.evaluate('st.c')
    # jump far ahead to check later stages render in real time
    pg.evaluate('st.c = 3600')
    pg.wait_for_timeout(1500)
    pg.screenshot(path=OUT + 'live_1.png')
    pg.evaluate('st.c = 4900')
    pg.wait_for_timeout(1200)
    pg.screenshot(path=OUT + 'live_2.png')
    fps = pg.evaluate('''() => new Promise(r => { let n = 0; const t0 = performance.now(); function f(){ n++; if (performance.now() - t0 < 2000) requestAnimationFrame(f); else r(n / 2); } requestAnimationFrame(f); })''')
    print('mic', mic, 'level', round(lvl, 4), 'cursor after 6s', round(c1, 1), 'after space', c2, 'anchors', pg.evaluate('ANCH.length'), 'fps(lines stage area)', fps)
    print('errors', errs[:5])
    b.close()
