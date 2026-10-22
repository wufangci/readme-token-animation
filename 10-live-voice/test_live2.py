from playwright.sync_api import sync_playwright
import os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'   # this version's folder
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DATA = ROOT + 'data/'
OUT = ROOT + 'out/'; os.makedirs(OUT, exist_ok=True)       # videos and stills are written here (git-ignored)
D = HERE
with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream', '--use-file-for-fake-audio-capture='+D+'fake_voice.wav%noloop', '--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 1440, 'height': 810})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + HERE + 'README_live.html')
    pg.click('#go')
    for i in range(36):
        pg.wait_for_timeout(500)
        r = pg.evaluate('[st.phase, +st.c.toFixed(1), +st.level.toFixed(4), +st.thrEff.toFixed(4), st.voiced]')
        print(i/2, r)
        if i == 2: pg.screenshot(path=D+'live2_listen.png')
        if i == 14: pg.screenshot(path=D+'live2_read.png')
    print('errors', errs)
    b.close()
