"""Prepare textures and patch statistics for img3d.html from img/src.jpg.
CLIP ViT-L/14-336 as used by LLaVA: pad to a square with the CLIP mean colour, resize to 336 x 336, cut 24 x 24 patches of 14 px."""
import os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img'))
src = Image.open('src.jpg').convert('RGB'); W, H = src.size
raw = open('src.jpg', 'rb').read()
src.resize((2048, round(2048 * H / W)), Image.LANCZOS).save('full.jpg', quality=92)
MEAN = (122, 116, 104)   # CLIP image mean * 255 (LLaVA expand2square)
S = max(W, H); sq = Image.new('RGB', (S, S), MEAN); sq.paste(src, (0, (S - H) // 2))
sq.resize((1344, 1344), Image.LANCZOS).save('hi_pad.png')
lo = sq.resize((336, 336), Image.BICUBIC); lo.save('lo_pad.png')
a = np.asarray(lo).astype(float) / 255
y0, y1 = (S - H) // 2 * 336 / S, ((S - H) // 2 + H) * 336 / S
feats = []
for r in range(24):
    for c in range(24):
        p = a[r*14:(r+1)*14, c*14:(c+1)*14].reshape(-1, 3)
        feats.append({'m': [round(x, 4) for x in p.mean(0)], 'v': round(float(p.std(0).mean()), 4),
                      'pad': bool((r+1)*14 <= y0 or r*14 >= y1)})
fw, fh = 4096, round(4096 * H / W)          # the real file bytes as a hex field
im = Image.new('L', (fw, fh), 255); d = ImageDraw.Draw(im)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 11)
cw, lh = 19.5, 13; per = int(fw // cw)
for rr in range(int(fh // lh)):
    for k, b in enumerate(raw[rr*per:(rr+1)*per]): d.text((2 + k*cw, rr*lh), f'{b:02X}', font=f, fill=40)
im.save('hex.png')
# caption ids: GPT-4o tokenizer on 「一條小路沒入茂密的綠色草叢裡。」
caption = [2432,140584,5820,14385,108738,8130,21290,224,23762,1616,14669,254,4472,16244,948,95,10410,94,788]
json.dump({'W': W, 'H': H, 'bytes': len(raw), 'feats': feats, 'mcu': [-(-W // 16), -(-H // 16)], 'caption': caption}, open('meta.json', 'w'))
print(W, H, len(raw), sum(x['pad'] for x in feats), 'padding patches')
