#!/usr/bin/env python3
"""Monta a amostra do documentario D.B. Cooper (PT-BR).

Pipeline: linha do tempo ancorada nas palavras da narracao -> cada plano
renderizado em mp4 (Ken Burns / clipe, graficos, grao, vinheta, letterbox)
-> uniao com dissolves (xfade) -> legendas ASS -> mixagem de audio.
"""
import json, math, os, re, subprocess, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, *p)
W, H, FPS = 1920, 1080, 30
BAR = 92  # letterbox
FONT = {
    'bebas': A('assets/BebasNeue.ttf'), 'oswald': A('assets/Oswald.ttf'),
    'type': A('assets/SpecialElite.ttf'), 'hand': A('assets/Caveat.ttf'),
    'inter': A('assets/Inter.ttf'),
}

def font(name, size, weight=None):
    f = ImageFont.truetype(FONT[name], size)
    if weight:
        try:
            f.set_variation_by_axes([weight] if name != 'inter' else [14, weight])
        except Exception:
            pass
    return f

# ------------------------------------------------------------------ timeline
SEGS = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
GAP_AFTER = {'s1': 1.1, 's2': 0.7, 's3': 0.9, 's4': 0.7, 's5': 0.8, 's6': 1.3, 's7': 1.0}
T0 = 2.4  # abertura com tempestade antes da voz

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))

seg_start, words = {}, {}
t = T0
for s in SEGS:
    seg_start[s] = t
    ws = [w for w in json.load(open(A('words', s + '.json')))['words'] if w['type'] == 'word' and not w['text'].startswith('[')]
    words[s] = [dict(w, start=w['start'] + t, end=w['end'] + t) for w in ws]
    t += dur(A('audio', s + '.mp3')) + GAP_AFTER.get(s, 0)
NARR_END = t
END = NARR_END + 0.6 + 5.0

def norm(x):
    return re.sub(r'[^\w]', '', x.lower())

def at(seg, key, nth=1):
    """tempo de inicio da n-esima palavra `key` no segmento."""
    c = 0
    for w in words[seg]:
        if norm(w['text']) == norm(key):
            c += 1
            if c == nth:
                return w['start']
    raise KeyError((seg, key, nth))

def segin(seg):  # inicio visual do segmento (metade do respiro anterior)
    i = SEGS.index(seg)
    if i == 0:
        return seg_start[seg]
    prev = SEGS[i - 1]
    return seg_start[seg] - GAP_AFTER[prev] * 0.5

# Cada plano: (inicio, tipo, fonte, opcoes)
SH = []
def shot(t, kind, src=None, **o):
    SH.append(dict(t=t, kind=kind, src=src, **o))

shot(0.0, 'video', 'v01')
shot(at('s1', 'Vinte') - 0.15, 'img', 'img02', ov=[('type', '24 DE NOVEMBRO DE 1971\nPORTLAND, OREGON')], move='in')
shot(at('s1', 'Um'), 'img', 'img03', move='in_l')
shot(at('s1', 'Poucas'), 'video', 'v04')
shot(at('s1', 'nunca'), 'img', 'img05', move='out')
shot(at('s1', 'Mais'), 'img', 'img06', ov=[('title', 'D.B. COOPER', 'O ÚNICO SEQUESTRO AÉREO NUNCA RESOLVIDO DOS EUA')], move='in', dim=0.55, x_in=0.8)
shot(segin('s2'), 'img', 'img07', ov=[('stamp', 'NOME NA PASSAGEM: "DAN COOPER"', at('s2', 'Dan'))], move='in_r', x_in=0.8)
shot(at('s2', 'Voo'), 'map', 'map1', ov=[('label', 'VOO 305 · NORTHWEST ORIENT')])
shot(at('s2', 'Sentou'), 'img', 'img09', move='in')
shot(at('s2', 'bourbon'), 'img', 'img10', move='in_r')
shot(segin('s3'), 'img', 'img11', move='in')
shot(at('s3', 'bilhete'), 'img', 'img12', move='in')
shot(at('s3', 'Então'), 'img', 'img09', move='push', focus=(0.62, 0.45))
shot(at('s3', 'Senhorita') - 0.2, 'img', 'img14', ov=[('note', 'MISS —\nI HAVE A BOMB', 'Bilhete entregue à comissária (reconstituição)')], move='in', x_out=0.04)
shot(segin('s4'), 'img', 'img15', move='push', focus=(0.5, 0.55), x_in=0.04)
shot(at('s4', 'exigências'), 'img', 'img22', ov=[('stat', 'US$ 200.000', 'EM NOTAS DE 20 DÓLARES', at('s4', 'Duzentos'))], move='in', dim=0.45, blur=3)
shot(at('s4', 'Quatro'), 'img', 'img17', ov=[('stat', '4', 'PARAQUEDAS', None)], move='in_l', dim=0.75)
shot(at('s4', 'caminhão'), 'img', 'img18', move='in_r')
shot(at('s4', 'valores') - 0.25, 'img', 'img22', ov=[('stat', '≈ US$ 1,5 MI', 'EM VALORES DE HOJE', None)], move='out', dim=0.4, blur=6)
shot(segin('s5'), 'video', 'v20')
shot(at('s5', 'Os'), 'img', 'img21', ov=[('label', '10.000 NOTAS FOTOGRAFADAS PELO FBI')], move='in')
shot(at('s5', 'Às'), 'img', 'img23', ov=[('type', '17:40\nAEROPORTO SEATTLE-TACOMA'), ('label_at', '36 PASSAGEIROS LIBERTADOS', at('s5', 'libertou'))], move='in_l')
shot(at('s5', 'Mas'), 'img', 'img24', move='push', focus=(0.5, 0.42))
shot(segin('s6'), 'img', 'img26', move='in')
shot(at('s6', 'Voar'), 'map', 'map2')
shot(at('s6', 'Trem'), 'img', 'img27', move='in_r')
shot(at('s6', 'escada'), 'video', 'v28')
shot(at('s6', 'Aquele'), 'img', 'img29', ov=[('label', 'BOEING 727 · ESCADA TRASEIRA VENTRAL')], move='in_l')
shot(segin('s7'), 'img', 'img31', ov=[('type', '20:13')], move='push', focus=(0.5, 0.5))
shot(at('s7', 'tranco'), 'img', 'img05', move='shake', flash=True, x_in=0.04)
shot(at('s7', 'Quando'), 'img', 'img32', ov=[('type', 'RENO, NEVADA')], move='in')
shot(at('s7', 'Estava'), 'img', 'img33', move='push', focus=(0.47, 0.6), x_in=0.04)
shot(at('s7', 'Dan'), 'img', 'img05', move='out', dim=0.8)
shot(segin('s8'), 'video', 'v35')
shot(at('s8', 'Centenas'), 'img', 'img36', move='in_r')
shot(at('s8', 'Nada'), 'card', None, text='NADA.', x_in=0.04)
shot(at('s8', 'Nem', 1), 'card', None, text='NEM CORPO.', x_in=0.04)
shot(at('s8', 'Nem', 2), 'card', None, text='NEM PARAQUEDAS.', x_in=0.04)
shot(at('s8', 'Nem', 3), 'card', None, text='NEM UMA ÚNICA NOTA.', x_in=0.04)
shot(at('s8', 'Até'), 'img', 'img38', ov=[('type', 'FEVEREIRO DE 1980\nMARGEM DO RIO COLUMBIA')], move='in', x_in=0.8)
shot(at('s8', 'encontrou'), 'img', 'img39', move='push', focus=(0.5, 0.55))
shot(NARR_END + 0.2, 'end', None, x_in=1.0)

for i, s in enumerate(SH):
    s['end'] = SH[i + 1]['t'] if i + 1 < len(SH) else END
    s.setdefault('x_in', 0.45)
for i, s in enumerate(SH):
    xin = s['x_in'] if i > 0 else 0
    xout = SH[i + 1]['x_in'] if i + 1 < len(SH) else 0
    s['xin'], s['xout'] = xin, xout
    s['render_start'] = s['t'] - xin / 2
    s['len'] = (s['end'] + xout / 2) - s['render_start']
SH[0]['render_start'] = 0.0
SH[0]['len'] = SH[1]['t'] + SH[1]['x_in'] / 2

# ------------------------------------------------------------------ look
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 9, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
GRAIN = [np.asarray(Image.fromarray(g).resize((W, H), Image.BILINEAR))[..., None] for g in GRAIN]
yy, xx = np.mgrid[0:H, 0:W]
VIG = 1 - 0.45 * np.clip(((xx - W / 2) / (W / 2)) ** 2 * 0.6 + ((yy - H / 2) / (H / 2)) ** 2 * 0.9, 0, 1) ** 1.3
VIG = VIG[..., None].astype(np.float32)

def finish(frame, fi, dim=1.0):
    a = np.asarray(frame, dtype=np.float32)
    a = (a - 128) * 1.06 + 124  # contraste leve
    a[..., 2] *= 1.02           # leve frio nas sombras
    a = a * VIG * dim + GRAIN[fi % len(GRAIN)]
    a[:BAR] = 0
    a[H - BAR:] = 0
    return np.clip(a, 0, 255).astype(np.uint8)

# ------------------------------------------------------------------ overlays
def shadow_text(d, xy, txt, f, fill=(255, 255, 255, 255), sh=4, anchor='la', spacing=10, align='left'):
    x, y = xy
    d.multiline_text((x + sh, y + sh), txt, font=f, fill=(0, 0, 0, 170), anchor=anchor, spacing=spacing, align=align)
    d.multiline_text((x, y), txt, font=f, fill=fill, anchor=anchor, spacing=spacing, align=align)

def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

def draw_overlays(img, s, lt, gt):
    """lt = tempo local desde o inicio logico do plano; gt = tempo global."""
    ov = s.get('ov', [])
    if not ov:
        return img
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for o in ov:
        k = o[0]
        if k == 'type':
            txt = o[1]
            n = int(max(0, lt - 0.35) * 22)
            shown = txt[:n]
            cur = '▌' if (int(gt * 2.2) % 2 == 0) else ''
            f = font('type', 54 if '\n' in txt else 96)
            y = 150 if '\n' in txt else 140
            shadow_text(d, (120, y), shown + (cur if n <= len(txt) + 30 else ''), f, fill=(240, 232, 210, 255))
        elif k == 'title':
            a = ease((lt - 0.4) / 1.0)
            f1, f2 = font('bebas', 210), font('oswald', 40, 500)
            col = (245, 240, 230, int(255 * a))
            d.text((W / 2 + 5, H / 2 - 40 + 5), o[1], font=f1, fill=(0, 0, 0, int(160 * a)), anchor='ms')
            d.text((W / 2, H / 2 - 40), o[1], font=f1, fill=col, anchor='ms')
            d.line([(W / 2 - 330 * a, H / 2 - 5), (W / 2 + 330 * a, H / 2 - 5)], fill=(190, 40, 40, int(255 * a)), width=4)
            b = ease((lt - 1.1) / 0.8)
            d.text((W / 2, H / 2 + 55), o[2], font=f2, fill=(220, 215, 205, int(255 * b)), anchor='ms')
        elif k == 'stamp':
            gt0 = o[2]
            if gt >= gt0:
                a = ease((gt - gt0) / 0.25)
                sc = 1.0 + 0.6 * (1 - a)
                st = Image.new('RGBA', (1000, 160), (0, 0, 0, 0))
                sd = ImageDraw.Draw(st)
                sd.rectangle([6, 6, 994, 154], outline=(200, 30, 30, 230), width=8)
                sd.text((500, 82), o[1], font=font('type', 50), fill=(200, 30, 30, 235), anchor='mm')
                st = st.resize((int(1000 * sc * 0.9), int(160 * sc * 0.9)), Image.BICUBIC).rotate(-6, expand=True, resample=Image.BICUBIC)
                al = st.getchannel('A').point(lambda v: int(v * a))
                st.putalpha(al)
                layer.alpha_composite(st, (int(W * 0.55 - st.width / 2), int(H * 0.33 - st.height / 2)))
        elif k in ('label', 'label_at'):
            g0 = o[2] if k == 'label_at' else None
            a = ease((gt - g0) / 0.5) if g0 else ease((lt - 0.3) / 0.6)
            if a <= 0:
                continue
            f = font('oswald', 44, 500)
            tw = d.textlength(o[1], font=f)
            x0, y0 = 120, H - BAR - 210
            d.rectangle([x0, y0, x0 + 10, y0 + 64], fill=(200, 35, 35, int(255 * a)))
            d.rectangle([x0 + 10, y0, x0 + 10 + (tw + 50) * a, y0 + 64], fill=(10, 10, 12, int(200 * a)))
            if a > 0.6:
                d.text((x0 + 35, y0 + 32), o[1], font=f, fill=(240, 236, 228, int(255 * (a - 0.6) / 0.4)), anchor='lm')
        elif k == 'stat':
            g0 = o[3]
            big, small = o[1], o[2]
            a = ease((lt - 0.2) / 0.6)
            if g0 is not None:  # contador
                p = ease((gt - g0) / 1.4) if gt >= g0 else 0
                val = int(round(200000 * p / 1000.0)) * 1000
                big = 'US$ ' + f'{val:,}'.replace(',', '.')
            f1, f2 = font('bebas', 230), font('oswald', 46, 500)
            d.text((W / 2 + 6, H / 2 + 46), big, font=f1, fill=(0, 0, 0, int(150 * a)), anchor='ms')
            d.text((W / 2, H / 2 + 40), big, font=f1, fill=(250, 246, 236, int(255 * a)), anchor='ms')
            d.text((W / 2, H / 2 + 120), small, font=f2, fill=(215, 60, 55, int(255 * a)), anchor='ms')
        elif k == 'note':
            a = ease((lt - 0.4) / 1.2)
            f = font('hand', 120, 700)
            d.multiline_text((W / 2, H / 2 - 20), o[1], font=f, fill=(25, 22, 30, int(235 * a)), anchor='mm', spacing=8, align='center')
            d.text((W / 2, H - BAR - 120), o[2], font=font('inter', 30, 400), fill=(230, 225, 215, int(200 * a)), anchor='ms')
    img = img.convert('RGBA')
    img.alpha_composite(layer)
    return img.convert('RGB')

# ------------------------------------------------------------------ map
def load_geo():
    import shapely.geometry as sg
    land = json.load(open(A('assets/land.geojson')))
    states = json.load(open(A('assets/states.geojson')))
    return land, states

def make_map(name):
    import shapely.geometry as sg
    from shapely.ops import unary_union
    if name == 'map1':
        lat0, lat1 = 44.2, 48.8
        cities = [('PORTLAND', 45.59, -122.60), ('SEATTLE', 47.45, -122.31)]
        route = [(45.59, -122.60), (47.45, -122.31)]
        extra = None
    else:
        lat0, lat1 = 33.0, 50.0
        cities = [('SEATTLE', 47.45, -122.31), ('RENO', 39.50, -119.77)]
        route = [(47.45, -122.31), (39.50, -119.77)]
        extra = [(39.50, -119.77), (33.6, -116.0)]
    latc = (lat0 + lat1) / 2
    k = math.cos(math.radians(latc))
    hdeg = lat1 - lat0
    wdeg = hdeg * (W / H) / k
    lonc = (route[0][1] + route[-1][1]) / 2 + (2.5 if name == 'map2' else 0.8)
    lon0, lon1 = lonc - wdeg / 2, lonc + wdeg / 2
    S = 2
    def P(lat, lon):
        return ((lon - lon0) / (lon1 - lon0) * W * S, (lat1 - lat) / (lat1 - lat0) * H * S)
    box = sg.box(lon0 - 1, lat0 - 1, lon1 + 1, lat1 + 1)
    base = Image.new('RGB', (W * S, H * S), (8, 16, 24))
    d = ImageDraw.Draw(base)
    land, states = load_geo()
    def polys(geom):
        g = sg.shape(geom).intersection(box)
        if g.is_empty:
            return []
        return list(g.geoms) if hasattr(g, 'geoms') else [g]
    for f in land['features']:
        for p in polys(f['geometry']):
            if p.geom_type != 'Polygon':
                continue
            d.polygon([P(y, x) for x, y in p.exterior.coords], fill=(34, 40, 42))
    for f in states['features']:
        for p in polys(f['geometry']):
            if p.geom_type != 'Polygon':
                continue
            d.line([P(y, x) for x, y in p.exterior.coords], fill=(78, 88, 90), width=3)
    # grade de coordenadas
    for la in range(int(lat0), int(lat1) + 1, 2):
        d.line([P(la, lon0), P(la, lon1)], fill=(30, 44, 54), width=1)
    for lo in range(int(lon0), int(lon1) + 1, 2):
        d.line([P(lat0, lo), P(lat1, lo)], fill=(30, 44, 54), width=1)
    base = base.resize((W, H), Image.LANCZOS)
    return dict(base=base, P=lambda la, lo: tuple(v / S for v in P(la, lo)), cities=cities, route=route, extra=extra)

MAPS = {}

def map_frame(name, lt, L):
    m = MAPS.get(name) or MAPS.setdefault(name, make_map(name))
    img = m['base'].copy().convert('RGBA')
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    P = m['P']
    p = ease((lt - 0.5) / max(1.0, L * 0.55))
    (a1, o1), (a2, o2) = m['route']
    x1, y1 = P(a1, o1); x2, y2 = P(a2, o2)
    xe, ye = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
    for wdt, al in ((18, 40), (10, 80), (5, 255)):
        d.line([(x1, y1), (xe, ye)], fill=(220, 50, 45, al), width=wdt)
    if m['extra'] and p >= 1:
        q = ease((lt - 0.5 - L * 0.55) / 1.2)
        (b1, c1), (b2, c2) = m['extra']
        u1, v1 = P(b1, c1); u2, v2 = P(b2, c2)
        n = 14
        for i in range(int(n * q)):
            s0, s1 = i / n, (i + 0.5) / n
            d.line([(u1 + (u2 - u1) * s0, v1 + (v2 - v1) * s0), (u1 + (u2 - u1) * s1, v1 + (v2 - v1) * s1)], fill=(220, 50, 45, 200), width=5)
        if q > 0.6:
            d.text((u2 + 20, v2 + 10), 'MÉXICO ↓', font=font('oswald', 40, 600), fill=(230, 80, 70, int(255 * (q - 0.6) / 0.4)), anchor='lm')
    r = 14 + 4 * math.sin(lt * 5)
    d.ellipse([xe - r, ye - r, xe + r, ye + r], outline=(255, 230, 220, 230), width=4)
    for nm, la, lo in m['cities']:
        cx, cy = P(la, lo)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(245, 240, 230, 255))
        shadow_text(d, (cx + 26, cy - 4), nm, font('oswald', 46, 600), anchor='lm', sh=3)
    img.alpha_composite(layer)
    # leve zoom no mapa
    z = 1.0 + 0.06 * (lt / max(L, 1))
    img = img.convert('RGB').resize((int(W * z), int(H * z)), Image.BICUBIC)
    ox, oy = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((ox, oy, ox + W, oy + H))

# ------------------------------------------------------------------ shot renderers
def kb_frame(src, move, p, focus=(0.5, 0.5), lt=0.0):
    sw, sh = src.size
    base = max(W / sw, H / sh)
    z0, z1 = 1.04, 1.16
    fx, fy = 0.5, 0.5
    if move == 'in':
        z = z0 + (z1 - z0) * p
    elif move == 'out':
        z = z1 - (z1 - z0) * p
    elif move == 'push':
        z = 1.02 + 0.28 * p
        fx, fy = 0.5 + (focus[0] - 0.5) * p, 0.5 + (focus[1] - 0.5) * p
    elif move in ('in_l', 'in_r'):
        z = 1.12 + 0.04 * p
        dx = 0.06 * (p - 0.5)
        fx = 0.5 + (dx if move == 'in_r' else -dx)
    elif move == 'shake':
        z = 1.14
        amp = 0.012 * max(0, 1 - lt / 1.5)
        fx, fy = 0.5 + amp * math.sin(lt * 53), 0.5 + amp * math.cos(lt * 47)
    else:
        z = 1.08
    scale = base * z  # pixels de saida por pixel de origem
    vw, vh = W / scale, H / scale  # janela na origem
    cx = min(max(fx * sw, vw / 2), sw - vw / 2)
    cy = min(max(fy * sh, vh / 2), sh - vh / 2)
    x0, y0 = cx - vw / 2, cy - vh / 2
    return src.transform((W, H), Image.AFFINE, (1 / scale, 0, x0, 0, 1 / scale, y0), resample=Image.BICUBIC)

def card_frame(text, lt):
    img = Image.new('RGB', (W, H), (6, 6, 8))
    d = ImageDraw.Draw(img)
    a = ease(lt / 0.15)
    sc = 1.0 + 0.04 * min(lt, 2)
    f = font('bebas', int(170 * sc))
    d.text((W / 2, H / 2 + 60), text, font=f, fill=(int(240 * a), int(236 * a), int(228 * a)), anchor='ms')
    return img

def end_frame(lt):
    bg = Image.open(A('img', 'img05.png')).convert('RGB')
    img = kb_frame(bg, 'in', min(1, lt / 6))
    img = Image.eval(img, lambda v: int(v * 0.35))
    d = ImageDraw.Draw(img, 'RGBA')
    a = ease((lt - 0.6) / 1.2)
    d.text((W / 2, H / 2 + 10), 'CONTINUA...', font=font('bebas', 150), fill=(245, 240, 230, int(255 * a)), anchor='ms')
    b = ease((lt - 1.6) / 1.0)
    d.text((W / 2, H / 2 + 80), 'AMOSTRA · CASO D.B. COOPER', font=font('oswald', 36, 400), fill=(200, 60, 55, int(255 * b)), anchor='ms')
    return img

def video_frames(name, n):
    """le n quadros 1920x1080 a 30fps, desacelerando se o clipe for curto."""
    src = A('vid', name + '.mp4')
    d0 = dur(src)
    need = n / FPS
    slow = max(1.0, min(need / d0, 1.7))
    vf = f'setpts={slow:.4f}*PTS,fps={FPS},scale={W}:{H}:flags=lanczos,tpad=stop_mode=clone:stop_duration=30'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', vf, '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    for _ in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        yield Image.frombytes('RGB', (W, H), buf)
    p.stdout.close(); p.wait()

def render_shot(i):
    s = SH[i]
    out = A('render', 'shots', f'{i:03d}.mp4')
    n = int(round(s['len'] * FPS))
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    logical0 = s['t'] - s['render_start']  # quanto do clipe vem antes do corte
    src = None
    if s['kind'] == 'img':
        src = Image.open(A('img', s['src'] + '.png')).convert('RGB')
        if s.get('blur'):
            src = src.filter(ImageFilter.GaussianBlur(s['blur']))
    gen = video_frames(s['src'], n) if s['kind'] == 'video' else None
    for fi in range(n):
        lt_r = fi / FPS
        lt = lt_r - logical0
        gt = s['render_start'] + lt_r
        p = lt_r / max(s['len'], 0.01)
        if s['kind'] == 'img':
            fr = kb_frame(src, s.get('move', 'in'), p, s.get('focus', (0.5, 0.5)), lt)
        elif s['kind'] == 'video':
            fr = next(gen, None) or fr
        elif s['kind'] == 'map':
            fr = map_frame(s['src'], max(lt, 0), s['end'] - s['t'])
        elif s['kind'] == 'card':
            fr = card_frame(s['text'], max(lt, 0))
        else:
            fr = end_frame(max(lt, 0))
        if s.get('dim', 1.0) != 1.0:
            dm = s['dim']; fr = fr.point(lambda v: int(v * dm))
        fr = draw_overlays(fr, s, lt, gt)
        a = finish(fr, fi + i * 3)
        if s.get('flash') and 0 <= lt < 0.35:
            a = np.clip(a.astype(np.float32) + 255 * (1 - lt / 0.35) * 0.85, 0, 255).astype(np.uint8)
            a[:BAR] = 0; a[H - BAR:] = 0
        enc.stdin.write(a.tobytes())
    enc.stdin.close(); enc.wait()
    return i

# ------------------------------------------------------------------ subtitles
def ass_time(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h}:{m:02d}:{s:05.2f}'

def write_ass(path):
    lines = []
    for s in SEGS:
        cur = []
        for w in words[s]:
            cur.append(w)
            txt = ' '.join(x['text'] for x in cur)
            brk = re.search(r'[.!?:]$|\.\.\.$', w['text']) or len(txt) > 38 or (w['text'].endswith(',') and len(txt) > 22)
            if brk:
                lines.append((cur[0]['start'], cur[-1]['end'] + 0.25, txt)); cur = []
        if cur:
            lines.append((cur[0]['start'], cur[-1]['end'] + 0.25, ' '.join(x['text'] for x in cur)))
    # evita sobreposicao
    for i in range(len(lines) - 1):
        if lines[i][1] > lines[i + 1][0]:
            lines[i] = (lines[i][0], lines[i + 1][0] - 0.02, lines[i][2])
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter,46,&H00F2F2F2,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,2.6,1.2,2,200,200,{BAR + 34},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(path, 'w') as f:
        f.write(head)
        for a, b, t in lines:
            f.write(f'Dialogue: 0,{ass_time(a)},{ass_time(b)},Sub,,0,0,0,,{t}\n')

# ------------------------------------------------------------------ assemble
def assemble():
    shots = [A('render', 'shots', f'{i:03d}.mp4') for i in range(len(SH))]
    inp = []
    for p in shots:
        inp += ['-i', p]
    fc, prev = [], '[0:v]'
    for i in range(1, len(SH)):
        x = max(SH[i]['x_in'], 0.04)
        off = SH[i]['t'] - x / 2
        lab = f'[x{i}]'
        fc.append(f'{prev}[{i}:v]xfade=transition=fade:duration={x:.3f}:offset={off:.3f}{lab}')
        prev = lab
    ass = A('render', 'legendas.ass')
    fc.append(f"{prev}ass={ass}:fontsdir={A('assets')}[v]")
    # ---- audio
    ai = len(SH)
    aud = []
    na = []
    for k, s in enumerate(SEGS):
        aud += ['-i', A('audio', s + '.mp3')]
        ms = int(seg_start[s] * 1000)
        fc.append(f'[{ai + k}:a]aresample=48000,adelay={ms}|{ms},apad=whole_dur={END:.2f}[n{k}]')
        na.append(f'[n{k}]')
    base = ai + len(SEGS)
    aud += ['-i', A('audio', 'music.mp3'), '-i', A('audio', 'sfx_thunder.mp3'), '-i', A('audio', 'sfx_wind.mp3'), '-i', A('audio', 'sfx_type.mp3')]
    m, th, wi, ty = base, base + 1, base + 2, base + 3
    fc.append(f"{''.join(na)}amix=inputs={len(na)}:normalize=0,volume=1.0,asplit=2[narr][sc]")
    fc.append(f'[{m}:a]aresample=48000,volume=0.42,afade=t=in:d=2,afade=t=out:st={END - 3.5:.2f}:d=3.5,apad=whole_dur={END:.2f}[mus0]')
    fc.append('[mus0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=30:release=600[mus]')
    def sfx(idx, t0, vol, name, extra=''):
        ms = int(t0 * 1000)
        fc.append(f'[{idx}:a]aresample=48000,{extra}volume={vol},adelay={ms}|{ms},apad=whole_dur={END:.2f}[{name}]')
    t_tranco = at('s7', 'tranco')
    fc.append(f'[{th}:a]asplit=3[th1][th2][th3]')
    fc.append(f'[{wi}:a]asplit=2[wi1][wi2]')
    fc.append(f'[{ty}:a]asplit=3[ty1][ty2][ty3]')
    def sfx_l(lbl, t0, vol, name, extra=''):
        ms = int(t0 * 1000)
        fc.append(f'{lbl}aresample=48000,{extra}volume={vol},adelay={ms}|{ms},apad=whole_dur={END:.2f}[{name}]')
    sfx_l('[th1]', 0.15, 1.0, 'e1', 'aecho=0.8:0.85:600|1100:0.45|0.3,')
    sfx_l('[th2]', t_tranco - 0.05, 1.1, 'e2', 'aecho=0.8:0.85:700|1300:0.5|0.3,')
    sfx_l('[th3]', at('s1', 'Mais') + 0.2, 0.55, 'e3', 'lowpass=f=500,aecho=0.8:0.9:900|1600:0.5|0.35,')
    sfx_l('[wi1]', t_tranco + 0.1, 0.8, 'e4', 'afade=t=out:st=2.2:d=0.8,')
    sfx_l('[wi2]', at('s6', 'escada') - 0.2, 0.45, 'e5', 'afade=t=out:st=2.0:d=1,')
    sfx_l('[ty1]', at('s1', 'Vinte') + 0.2, 0.5, 'e6')
    sfx_l('[ty2]', at('s5', 'Às') + 0.2, 0.45, 'e7')
    sfx_l('[ty3]', segin('s7') + 0.3, 0.45, 'e8')
    # ruido de cabine (sintetizado) entre s2 e o salto
    c0, c1 = segin('s2'), t_tranco
    fc.append(f'anoisesrc=color=brown:amplitude=0.5:duration={c1 - c0:.2f}:sample_rate=48000,lowpass=f=220,highpass=f=35,volume=0.12,'
              f'afade=t=in:d=1.5,afade=t=out:st={c1 - c0 - 0.4:.2f}:d=0.4,adelay={int(c0 * 1000)}|{int(c0 * 1000)},apad=whole_dur={END:.2f}[cab]')
    fc.append('[narr][mus][e1][e2][e3][e4][e5][e6][e7][e8][cab]amix=inputs=11:normalize=0,alimiter=limit=0.95,loudnorm=I=-15:TP=-1.5:LRA=11[a]')
    cmd = ['ffmpeg', '-v', 'error', '-y'] + inp + aud + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
           '-t', f'{END:.2f}', '-movflags', '+faststart', A('render', 'DB_Cooper_amostra_PTBR.mp4')]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    os.makedirs(A('render', 'shots'), exist_ok=True)
    print(f'{len(SH)} planos, duracao {END:.1f}s')
    for i, s in enumerate(SH):
        print(f"{i:02d} {s['t']:7.2f} {s['len']:5.2f} {s['kind']:5s} {s.get('src') or s.get('text', '')}")
    if 'plan' in sys.argv:
        sys.exit()
    write_ass(A('render', 'legendas.ass'))
    only = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 1 and sys.argv[1] == 'shots' else list(range(len(SH)))
    with Pool(4) as pool:
        for i in pool.imap_unordered(render_shot, only):
            print('ok', i, flush=True)
    if not (len(sys.argv) > 1 and sys.argv[1] == 'shots'):
        assemble()
        print('PRONTO')
