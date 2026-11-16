#!/usr/bin/env python3
"""Cortes verticais (9:16) para Shorts/Reels a partir da linha do tempo do video longo.

Layout: fundo = quadro desfocado preenchendo 1080x1920; quadro 16:9 ampliado no
meio; gancho em texto no topo; legenda palavra a palavra grande embaixo.
Audio = trechos do mix final (render/mix.wav). Requer render.py audio ja rodado.
uso: shorts.py [n ...]
"""
import os, subprocess, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as r

VW, VH, FPS = 1080, 1920, 30

# no vertical, textos alinhados a esquerda seriam cortados: mantem so os centralizados
for _s in r.SH:
    if _s.get('ov'):
        _s['ov'] = [o for o in _s['ov'] if o[0] in ('stat', 'title', 'quote', 'chapter')]

def find(seg, word, nth=1, end=False):
    c = 0
    for w in r.words[seg]:
        if r.norm(w['text']) == r.norm(word):
            c += 1
            if c == nth:
                return w['end'] if end else w['start']
    raise KeyError((seg, word, nth))

# (nome, gancho, [(inicio_global, fim_global), ...])
SHORTS = [
    ('01_no_plane', 'THERE WAS NO PLANE ANYMORE.\nSHE WAS STILL FALLING.',
     [(find('s01', 'Somewhere') - 0.25, find('s01', 'told.', end=True) + 0.6)]),
    ('02_this_is_the_end', 'HER MOTHER SAID:\n"THIS IS THE END."',
     [(find('s06', 'Through') - 0.25, find('s07', 'green.', end=True) + 0.6)]),
    ('03_how_did_she_survive', 'NO ONE CAN SAY FOR CERTAIN\nHOW SHE SURVIVED THIS.',
     [(r.seg_start['s08'] - 0.2, find('s08', 'real.', end=True) + 0.7)]),
    ('04_fathers_rule', 'LOST IN THE AMAZON AT 17.\nHER DAD HAD TAUGHT HER ONE RULE.',
     [(find('s10', 'And') - 0.25, find('s10', 'walking.', end=True) + 0.7)]),
    ('05_they_couldnt_see_her', 'SHE COULD HEAR THE SEARCH PLANES.\nTHEY COULDN\'T SEE HER.',
     [(r.seg_start['s11'] - 0.2, find('s11', 'completely.', end=True) + 0.8)]),
    ('06_a_boat', 'DAY 10 ALONE IN THE AMAZON.\nTHEN SHE FOUND A BOAT.',
     [(r.seg_start['s14'] - 0.2, find('s14', 'here.', end=True) + 0.4),
      (find('s14', 'She', 1) - 0.2, find('s15', 'spirit.', end=True) + 0.7)]),
]

def clean_frame(gt, fi):
    act = [i for i, s in enumerate(r.SH) if s['w0'] <= gt < s['w1']] or [len(r.SH) - 1]
    if len(act) == 1:
        fr = r.shot_frame(act[0], gt)
    else:
        i, j = act[-2], act[-1]
        a = r.ease((gt - r.SH[j]['w0']) / max(r.SH[j]['x'], 0.01))
        fr = Image.blend(r.shot_frame(i, gt), r.shot_frame(j, gt), a)
    fr = r.hud(fr, gt)
    a = np.asarray(fr).astype(np.float32)
    a = (a - 128) * 1.07 + 125
    a = a * r.VIG + r.GRAIN[fi % len(r.GRAIN)]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def caption(d, gt, y):
    seg = None
    for s in r.SEGS:
        if r.seg_start[s] - 0.5 <= gt:
            seg = s
    ws = [w for w in r.words[seg] if not w['text'].startswith('[')]
    k = None
    for i, w in enumerate(ws):
        if w['start'] - 0.05 <= gt <= w['end'] + 0.25:
            k = i
    if k is None:
        return
    g0 = (k // 3) * 3
    grp = ws[g0:g0 + 3]
    f = r.font('bebas', 112)
    texts = [w['text'].upper() for w in grp]
    widths = [d.textlength(t, font=f) for t in texts]
    total = sum(widths) + 30 * (len(texts) - 1)
    x = VW / 2 - total / 2
    for t, wdt, w in zip(texts, widths, grp):
        on = w is ws[k]
        col = (255, 214, 0, 255) if on else (250, 250, 245, 255)
        d.text((x, y), t, font=f, fill=col, anchor='ls', stroke_width=7, stroke_fill=(0, 0, 0, 255))
        x += wdt + 30

def vframe(args):
    hook, gt, lt, fi, L = args
    fr = clean_frame(gt, fi)
    bg = fr.resize((VW * 2 // 3, VH * 2 // 3)).resize((VW, VH)) if False else None
    s = VH / r.H
    bg = fr.resize((int(r.W * s), VH), Image.BILINEAR)
    ox = (bg.width - VW) // 2
    bg = bg.crop((ox, 0, ox + VW, VH)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.eval(bg, lambda v: int(v * 0.45))
    fg_h = 1010
    fg_w = int(fg_h * r.W / r.H)
    fg = fr.resize((fg_w, fg_h), Image.BICUBIC)
    cx = (fg_w - VW) // 2
    fg = fg.crop((cx, 0, cx + VW, fg_h))
    img = bg.copy()
    img.paste(fg, (0, 470))
    d = ImageDraw.Draw(img, 'RGBA')
    pop = 1.0 + 0.18 * (1 - r.ease(lt / 0.25))
    f = r.font('bebas', int(84 * pop))
    lines = hook.split('\n')
    y = 190
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.rectangle([VW / 2 - tw / 2 - 22, y - 8, VW / 2 + tw / 2 + 22, y + 88 * pop], fill=(0, 0, 0, 200))
        d.text((VW / 2, y + 44 * pop), ln, font=f, fill=(255, 255, 255, 255), anchor='mm')
        y += int(100 * pop)
    caption(d, gt, 1640)
    d.text((VW / 2, VH - 120), 'FULL STORY ON THE CHANNEL', font=r.font('oswald', 34, 500), fill=(230, 230, 225, int(200 * r.ease((lt - 3) / 1))), anchor='mm')
    a = np.asarray(img)
    if lt < 0.15:
        a = np.clip(a.astype(np.float32) + 120 * (1 - lt / 0.15), 0, 255).astype(np.uint8)
    if L - lt < 0.4:
        a = (a * max(0, (L - lt) / 0.4)).astype(np.uint8)
    return a.tobytes()

def make(n, hook, ranges):
    out = os.path.join(r.OUT, 'shorts')
    os.makedirs(out, exist_ok=True)
    L = sum(b - a for a, b in ranges)
    jobs, lt = [], 0.0
    fi = 0
    for a, b in ranges:
        for k in range(int((b - a) * FPS)):
            jobs.append((hook, a + k / FPS, fi / FPS, fi, L))
            fi += 1
    vid = os.path.join(out, n + '_v.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{VW}x{VH}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
    with Pool(int(os.environ.get('PROCS', os.cpu_count()))) as pool:
        for buf in pool.imap(vframe, jobs, chunksize=30):
            enc.stdin.write(buf)
    enc.stdin.close(); enc.wait()
    mix = os.path.join(r.OUT, 'mix.wav')
    parts = []
    for k, (a, b) in enumerate(ranges):
        parts.append(f'[0:a]atrim={a:.3f}:{a + int((b - a) * FPS) / FPS:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.08,afade=t=out:st={int((b - a) * FPS) / FPS - 0.3:.3f}:d=0.3[p{k}]')
    fc = ';'.join(parts) + ';' + ''.join(f'[p{k}]' for k in range(len(ranges))) + f'concat=n={len(ranges)}:v=0:a=1[a]'
    final = os.path.join(out, f'Koepcke_short_{n}.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mix, '-i', vid, '-filter_complex', fc, '-map', '1:v', '-map', '[a]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final], check=True)
    os.remove(vid)
    print('ok', final, f'{L:.1f}s', flush=True)

if __name__ == '__main__':
    pick = sys.argv[1:]
    for n, hook, ranges in SHORTS:
        if not pick or any(n.startswith(p) for p in pick):
            make(n, hook, ranges)
