import json, os
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data') + '/'
# Estimated reading timeline. Replace with real timestamps once the recording exists.
T = json.load(open(DATA + 'zh.json', encoding='utf-8'))
R0, R1 = 3.0, 1173.0
def dec(b):
    try: return bytes(b).decode('utf-8')
    except: return None
groups = []; cur = []
for i, t in enumerate(T):
    cur.append(i); s = dec(sum((T[k]['bytes'] for k in cur), []))
    if s is not None: groups.append((list(cur), s)); cur = []
text = ''.join(s for _, s in groups)
# weight per group: chars read aloud + pauses after punctuation and paragraphs
W = []
pos = 0
for toks, s in groups:
    w = 0
    for j, ch in enumerate(s):
        k = pos + j
        if ch not in ' \n*#-': w += 1
        if ch in '，、；：': w += .5
        if ch in '。？！': w += 1.2
        if text[k:k+2] == '\n\n': w += 3
    W.append(w); pos += len(s)
tot = sum(W)
tok_time = [0.0] * len(T)
acc = 0.0
for (toks, s), w in zip(groups, W):
    t = R0 + (R1 - R0) * acc / tot
    for k in toks: tok_time[k] = round(t, 3)
    acc += w
secs = [0, 732, 1468, 2414, 3492, 4343, 5278, len(T)]
json.dump({'tok_time': tok_time, 'secs': secs, 'R0': R0, 'R1': R1}, open(DATA + 'timing.json', 'w'))
print('sections start at', [round(tok_time[k] / 60, 2) if k < len(T) else round(R1 / 60, 2) for k in secs], 'min')
