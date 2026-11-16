#!/usr/bin/env python3
"""Documentario Juliane Koepcke (EN) - renderizador em blocos paralelos.

Cada quadro e composto em Python (planos com Ken Burns / clipes / mapas /
cards, dissolves, overlays, HUD de dias, legendas), renderizado em blocos
paralelos e concatenado sem recodificar. Audio mixado a parte e multiplexado.

uso: render.py plan | render.py still T [T...] | render.py [video] [--from A --to B]
"""
import json, math, os, re, subprocess, sys
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, *p)
W, H, FPS = 1920, 1080, 30
BAR = 78
OUT = A('render')

@lru_cache(None)
def font(name, size, weight=None):
    path = {'bebas': 'BebasNeue', 'oswald': 'Oswald', 'type': 'SpecialElite', 'hand': 'Caveat', 'inter': 'Inter'}[name]
    f = ImageFont.truetype(A('assets', path + '.ttf'), size)
    if weight:
        try:
            f.set_variation_by_axes([weight] if name != 'inter' else [14, weight])
        except Exception:
            pass
    return f

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))

def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

# ------------------------------------------------------------------ timeline
SEGS = [f's{i:02d}' for i in range(1, 19)]
GAP = {'s01': 1.0, 's02': 1.3, 's03': 0.9, 's04': 0.9, 's05': 0.5, 's06': 2.2, 's07': 1.2, 's08': 1.4,
       's09': 1.0, 's10': 1.1, 's11': 1.1, 's12': 1.5, 's13': 1.1, 's14': 1.2, 's15': 1.8, 's16': 1.3, 's17': 1.2}
T0 = 1.6
seg_start, words = {}, {}
t = T0
for s in SEGS:
    seg_start[s] = t
    wf = A('words_scribe', s + '.json') if os.path.exists(A('words_scribe', s + '.json')) else A('words', s + '.json')
    ws = [w for w in json.load(open(wf))['words'] if w.get('type', 'word') == 'word' and not w['text'].startswith(('(', '['))]
    words[s] = [dict(w, start=w['start'] + t, end=w['end'] + t) for w in ws]
    t += dur(A('audio', s + '.mp3')) + GAP.get(s, 0)
NARR_END = t
END = NARR_END + 6.0
NFRAMES = int(round(END * FPS))

def norm(x):
    return re.sub(r"[^\w'-]", '', x)

def at(seg, key, nth=1, after=None):
    c = 0
    for w in words[seg]:
        if after is not None and w['start'] < after:
            continue
        if norm(w['text']) == norm(key):
            c += 1
            if c == nth:
                return w['start']
    raise KeyError((seg, key, nth))

def segin(seg):
    i = SEGS.index(seg)
    return seg_start[seg] - (GAP[SEGS[i - 1]] * 0.55 if i else 0)

# ------------------------------------------------------------------ shots
SH = []
def shot(t, kind, src=None, x=0.5, **o):
    SH.append(dict(t=t, kind=kind, src=src, x=x, **o))

ERRS = []
def S(seg, key=None, nth=1, d=-0.12):
    try:
        return segin(seg) if key is None else at(seg, key, nth) + d
    except KeyError as e:
        ERRS.append(e.args[0]); return (SH[-1]['t'] + 2.0) if SH else 0

CH = lambda n, title: ('chapter', n, title)

# --- cold open
shot(0.0, 'video', 'v1', x=0, zoom=(1.0, 1.08), flash=0.0)
shot(S('s01', 'Somewhere'), 'img', 'k01', move='in', ov=[('type', 'DECEMBER 24, 1971\nABOVE THE PERUVIAN AMAZON')])
shot(S('s01', 'Not'), 'video', 'v1', off=2.5, x=0.15, zoom=(1.1, 1.2))
shot(S('s01', 'There'), 'img', 'k26', move='shake', x=0.08, hit=True)
shot(S('s01', 'She', 1), 'img', 'k27', move='fall', x=0.25, wind=True)
shot(S('s01', 'almost'), 'img', 'k33', move='push', focus=(0.5, 0.35), x=0.3)
shot(S('s01', 'Below'), 'img', 'k02', move='dive', x=0.3)
shot(S('s01', 'Ninety-two'), 'img', 'k03', dim=0.45, x=0.2, ov=[('stat', '92', 'PEOPLE ON BOARD', (0, 92, 1.0))])
shot(S('s01', 'Ninety-one'), 'img', 'k03', dim=0.4, move='out', x=0.15, ov=[('stat', '91', 'NEVER CAME HOME', None)], hit=True)
shot(S('s01', 'Her'), 'img', 'k04', move='in', dim=0.55, x=0.8, ov=[('title', 'THE GIRL WHO FELL FROM THE SKY', 'THE TRUE STORY OF JULIANE KOEPCKE')], hit=True)
shot(S('s01', 'extraordinary'), 'img', 'k40', move='in_r')
# --- promise
shot(segin('s02'), 'img', 'k31', move='push', focus=(0.35, 0.5), x=0.7)
shot(S('s02', 'How'), 'img', 'k45', move='in')
shot(S('s02', 'one', 2), 'img', 'k05', move='push', focus=(0.45, 0.55))
shot(S('s02', 'And'), 'img', 'k43', move='in_l')
shot(S('s02', 'became'), 'img', 'k06', move='in', dim=0.85)
# --- PART I
shot(segin('s03'), 'img', 'k14', move='out', x=0.9, ov=[CH('PART I', 'THE FOREST GIRL')], whoosh=True)
shot(S('s03', 'She'), 'img', 'k08', move='in_r', ov=[('type', 'LIMA, PERU · 1954')])
shot(S('s03', 'Her'), 'img', 'k09', move='in', ov=[('label', 'MARIA KOEPCKE · ORNITHOLOGIST')])
shot(S('s03', 'woman'), 'img', 'k51', move='in_r')
shot(S('s03', 'Her', 2), 'img', 'k10', move='push', focus=(0.55, 0.45), ov=[('label', 'HANS-WILHELM KOEPCKE · BIOLOGIST')])
shot(S('s03', 'In'), 'map', 'panguana', x=0.6, whoosh=True)
shot(S('s03', 'They'), 'img', 'k11', move='in', ov=[('type', 'PANGUANA · 1968')])
shot(S('s03', 'While'), 'img', 'k12', move='in_l')
shot(S('s03', 'Which', 1), 'img', 'k13', move='push', focus=(0.3, 0.6), x=0.3)
shot(S('s03', 'How', 1), 'img', 'k14', move='in', x=0.4)
shot(S('s03', 'To', 2), 'img', 'k07', move='in_r')
shot(S('s03', 'And', 2), 'img', 'k43', move='in', warm=True)
# --- the flight decision
shot(segin('s04'), 'img', 'k15', move='in', x=0.8, ov=[('type', 'DECEMBER 1971')])
shot(S('s04', 'Her'), 'img', 'k11', move='in_r')
shot(S('s04', 'It'), 'img', 'k16', move='in_l')
shot(S('s04', 'The', 1), 'img', 'k17', move='in_r', ov=[('label', 'LANSA · LOCKHEED L-188 ELECTRA')])
shot(S('s04', 'Her', 2), 'img', 'k18', move='push', focus=(0.6, 0.6), dim=0.5,
     ov=[('quote', '"ANY OTHER AIRLINE...\nBUT NOT LANSA."', 'HER FATHER, AS LATER REPORTED')])
shot(S('s04', 'Her', 3), 'img', 'k18', move='in', dim=0.85, x=0.3)
shot(S('s04', 'But'), 'img', 'k15', move='push', focus=(0.62, 0.5), dim=0.85)
shot(S('s04', 'And'), 'img', 'k19', move='in', ov=[('label', 'LANSA FLIGHT 508 · LIMA → PUCALLPA')])
# --- PART II
shot(segin('s05'), 'img', 'k17', move='in_l', x=0.8, ov=[CH('PART II', 'FLIGHT 508')], whoosh=True)
shot(S('s05', 'Eighty-six'), 'img', 'k20', move='in', ov=[('stat', '86 + 6', 'PASSENGERS + CREW', None)], dimov=0.55)
shot(S('s05', 'The', 2), 'map', 'route', x=0.5, whoosh=True)
shot(S('s05', 'Juliane'), 'img', 'k21', move='push', focus=(0.62, 0.42))
shot(S('s05', 'For'), 'img', 'k20', move='in_r', x=0.4)
shot(S('s05', 'And'), 'img', 'k33', move='push', focus=(0.55, 0.4), x=0.8)
# --- the storm
shot(segin('s06'), 'video', 'v1', off=1.0, x=0.2, zoom=(1.05, 1.15))
shot(S('s06', 'Within'), 'video', 'v3', x=0.12, zoom=(1.0, 1.06))
shot(S('s06', 'Gifts'), 'img', 'k20', move='shake', x=0.08)
shot(S('s06', 'People'), 'video', 'v3', off=2.2, x=0.08, zoom=(1.08, 1.18))
shot(S('s06', 'Through'), 'img', 'k24', move='shake', x=0.08, flash=True, thunder=True)
shot(S('s06', 'Fire'), 'img', 'k24', move='push', focus=(0.62, 0.35), x=0.05, hit=True)
shot(S('s06', 'Her'), 'img', 'k21', move='push', focus=(0.4, 0.45), dim=0.7, x=0.2)
shot(S('s06', 'This', d=-0.4), 'card', None, text='', x=0.3)
shot(S('s06', 'A', 2, d=-0.05), 'img', 'k26', move='shake', x=0.04, flash=True, thunder=True)
# --- the fall
shot(segin('s07'), 'card', None, text='', x=0.6)
shot(S('s07', 'She', 1), 'img', 'k27', move='fall', x=0.8, wind=True)
shot(S('s07', 'She', 2), 'img', 'k02', move='spin', x=0.4)
shot(S('s07', 'Then', 1, d=0.1), 'card', None, text='', x=0.08)
shot(S('s07', 'Investigators'), 'img', 'k24', move='in', dim=0.4, x=0.6,
     ov=[('list', 'WHAT INVESTIGATORS CONCLUDED', ['LIGHTNING STRIKES THE AIRCRAFT', 'A FUEL TANK IGNITES', 'THE WING FAILS', 'FLIGHT 508 BREAKS UP IN THE AIR'])])
shot(S('s07', 'Juliane'), 'img', 'k30x', x=0.3, hit=True,
     ov=[('stat', '3,000 M', '≈ 10,000 FEET · NO PARACHUTE', (0, 3000, 2.2))])
shot(S('s07', 'except'), 'img', 'k31', move='push', focus=(0.3, 0.45))
shot(S('s07', 'trees'), 'img', 'k14', move='in', x=0.5)
# --- how did she survive
shot(segin('s08'), 'img', 'k31', move='in', dim=0.45, x=0.8, ov=[('quote', 'HOW DID SHE SURVIVE?', '')], hit=True)
shot(S('s08', 'One'), 'img', 'k27', move='spin', ov=[('label', 'THEORY 1 · THE SEAT ROW SPUN LIKE A ROTOR')])
shot(S('s08', 'Another'), 'img', 'k33', move='push', focus=(0.55, 0.4), ov=[('label', 'THEORY 2 · STORM UPDRAFTS')])
shot(S('s08', 'And', 1), 'img', 'k02', move='dive', ov=[('label', 'THEORY 3 · THE RAINFOREST CANOPY')])
shot(S('s08', 'Most'), 'img', 'k14', move='push', focus=(0.5, 0.35))
shot(S('s08', 'But'), 'img', 'k31', move='out', dim=0.8)
shot(S('s08', 'Just'), 'card', None, x=0.4, text='VESNA VULOVIĆ', sub='JANUARY 1972 · CZECHOSLOVAKIA · ≈ 10,000 M')
shot(S('s08', 'But', 2), 'img', 'k40', move='in', x=0.5)
shot(S('s08', 'When'), 'img', 'k37', move='in', x=1.0, ov=[('type', 'DECEMBER 25, 1971')])
# --- PART III alone
shot(segin('s09'), 'img', 'k38', move='push', focus=(0.55, 0.6), x=0.8, ov=[CH('PART III', 'ALONE')], whoosh=True)
shot(S('s09', 'The'), 'img', 'k38', move='in_r', dim=0.8)
shot(S('s09', 'Her'), 'img', 'k57', move='in', dim=0.45,
     ov=[('list', 'HER INJURIES', ['BROKEN COLLARBONE', 'DEEP CUT ON HER ARM', 'WOUND ON HER LEG', 'ONE EYE SWOLLEN SHUT', 'GLASSES LOST'])])
shot(S('s09', 'She', 3), 'img', 'k05', move='push', focus=(0.45, 0.55))
shot(S('s09', 'She', 5), 'img', 'k40', move='in')
shot(S('s09', 'Searching'), 'img', 'k41', move='push', focus=(0.4, 0.5))
# --- father's rule
shot(segin('s10'), 'img', 'k04', move='in', x=0.8)
shot(S('s10', 'And'), 'img', 'k40', move='out', dim=0.8)
shot(S('s10', 'Then'), 'img', 'k43', move='in', x=0.9, warm=True)
shot(S('s10', 'Find'), 'img', 'k06', move='push', focus=(0.55, 0.6), dim=0.5,
     ov=[('rule', ['FIND WATER.', 'FOLLOW IT DOWNSTREAM.', 'STREAMS LEAD TO RIVERS.', 'RIVERS LEAD TO PEOPLE.'],
          [at('s10', 'Find'), at('s10', 'Follow'), at('s10', 'A'), at('s10', 'rivers...')])])
shot(S('s10', 'Nearby'), 'video', 'v4', x=0.6)
shot(S('s10', 'And', 3), 'img', 'k45', move='in', x=0.5, ov=[('type', 'SHE STARTED WALKING.')])
# --- the stream
shot(segin('s11'), 'img', 'k45', move='push', focus=(0.5, 0.8), x=0.7)
shot(S('s11', 'Stingrays'), 'img', 'k47', move='push', focus=(0.5, 0.55))
shot(S('s11', 'She', 2), 'img', 'k58', move='in')
shot(S('s11', 'Overhead'), 'img', 'k48', move='in_r', ov=[('label', 'ONE OF THE LARGEST AIR SEARCHES IN PERU’S HISTORY')])
shot(S('s11', 'But', 2), 'img', 'k02', move='out', dim=0.8)
shot(S('s11', 'Soon'), 'img', 'k40', move='out', dim=0.75)
# --- vultures
shot(segin('s12'), 'img', 'k51', move='push', focus=(0.55, 0.45), x=0.8)
shot(S('s12', 'Something'), 'img', 'k55', move='in', dim=0.7)
shot(S('s12', 'Soon'), 'img', 'k31', move='push', focus=(0.4, 0.55), dim=0.7)
shot(S('s12', 'With'), 'img', 'k04', move='in', dim=0.8)
shot(S('s12', 'It', 2), 'img', 'k03', move='out', dim=0.7)
shot(S('s12', 'The'), 'card', None, x=0.6, text='NO ONE WAS COMING.')
# --- days blur
shot(segin('s13'), 'img', 'k55', move='in', x=0.8, rain=True)
shot(S('s13', 'Mosquitoes'), 'img', 'k12', move='push', focus=(0.6, 0.5), dim=0.8)
shot(S('s13', 'And'), 'img', 'k57', move='push', focus=(0.4, 0.6))
shot(S('s13', 'Juliane'), 'img', 'k57', move='in', dim=0.6)
shot(S('s13', 'Still'), 'img', 'k58', move='push', focus=(0.5, 0.45))
shot(S('s13', 'The', 3), 'video', 'v4', off=2.0, x=0.6)
shot(S('s13', 'But', 1), 'img', 'k03', move='out', dim=0.7)
# --- the boat
shot(segin('s14'), 'img', 'k60', move='in', x=0.8)
shot(S('s14', 'A'), 'img', 'k60', move='push', focus=(0.35, 0.6), x=0.3)
shot(S('s14', 'And'), 'img', 'k60', move='push', focus=(0.75, 0.4), x=0.4)
shot(S('s14', 'There'), 'img', 'k60', move='push', focus=(0.3, 0.7), dim=0.9)
shot(S('s14', 'Juliane'), 'img', 'k10', move='in', warm=True, dim=0.85)
shot(S('s14', 'So'), 'img', 'k57', move='push', focus=(0.5, 0.55), dim=0.85)
shot(S('s14', 'pain'), 'img', 'k57', move='shake', dim=0.6, x=0.1, hit=True)
shot(S('s14', 'One'), 'img', 'k06', move='push', focus=(0.5, 0.6))
shot(S('s14', 'She'), 'img', 'k60', move='out')
shot(S('s14', 'So', 2), 'img', 'k60', move='in', dim=0.55, x=0.8)
# --- rescue
shot(segin('s15'), 'img', 'k64', move='in', x=0.6)
shot(S('s15', 'When'), 'img', 'k64', move='push', focus=(0.5, 0.4), dim=0.85)
shot(S('s15', 'Juliane'), 'img', 'k58', move='in', dim=0.85)
shot(S('s15', 'She'), 'img', 'k45', move='push', focus=(0.5, 0.4))
shot(S('s15', 'The', 2), 'img', 'k67', move='in_r')
shot(S('s15', 'From'), 'img', 'k48', move='in')
shot(S('s15', 'After'), 'img', 'k83', move='in', dim=0.45, ov=[('stat', '11 DAYS', 'ALONE IN THE AMAZON', (0, 11, 1.4))], hit=True)
# --- PART IV after
shot(segin('s16'), 'img', 'k69', move='push', focus=(0.45, 0.5), x=0.9, ov=[CH('PART IV', 'WHAT THE JUNGLE KEPT')], whoosh=True)
shot(S('s16', 'Maria'), 'img', 'k09', move='in', dim=0.6, gray=True)
shot(S('s16', 'Using'), 'img', 'k64', move='in_l', dim=0.8)
shot(S('s16', 'Among'), 'img', 'k37', move='in', dim=0.65)
shot(S('s16', 'Investigators'), 'img', 'k38', move='out', dim=0.6)
shot(S('s16', 'Of'), 'img', 'k01', move='in', dim=0.4, ov=[('stat', '1 OF 92', 'THE ONLY SURVIVOR', None)], hit=True)
shot(S('s16', 'LANSA'), 'img', 'k17', move='out', dim=0.6, gray=True)
# --- after story
shot(segin('s17'), 'img', 'k04', move='in', dim=0.5, x=0.8, ov=[('quote', '"THE GIRL WHO FELL\nFROM THE SKY"', 'HOW THE WORLD CAME TO KNOW HER')])
shot(S('s17', 'But'), 'img', 'k75x', move='in', dim=0.85)
shot(S('s17', 'Why'), 'card', None, x=0.3, text='WHY ME?')
shot(S('s17', 'She', 1), 'img', 'k07', move='in_r')
shot(S('s17', 'She', 2), 'img', 'k77', move='push', focus=(0.4, 0.4), ov=[('label', 'DR. JULIANE DILLER (NÉE KOEPCKE) · MAMMALOGIST')])
shot(S('s17', 'In'), 'img', 'k31', move='in', ov=[('label', 'WERNER HERZOG · "WINGS OF HOPE" (2000)')])
shot(S('s17', 'Years'), 'img', 'k18', move='push', focus=(0.65, 0.6), dim=0.8, ov=[('label', '"WHEN I FELL FROM THE SKY" · HER MEMOIR')])
# --- finale
shot(segin('s18'), 'img', 'k11', move='in', x=0.8, ov=[('type', 'PANGUANA · TODAY')])
shot(S('s18', 'She'), 'img', 'k11', move='push', focus=(0.4, 0.5))
shot(S('s18', 'The', 1), 'img', 'k14', move='out')
shot(S('s18', 'So'), 'img', 'k27', move='in', dim=0.8)
shot(S('s18', 'The', 2), 'card', None, x=0.06, text='THE SEATS.', hit=True)
shot(S('s18', 'The', 3), 'card', None, x=0.06, text='THE STORM.', hit=True)
shot(S('s18', 'The', 4), 'card', None, x=0.06, text='THE TREES.', hit=True)
shot(S('s18', 'Luck'), 'img', 'k33', move='out', x=0.3)
shot(S('s18', 'Knowledge'), 'img', 'k43', move='in', warm=True)
shot(S('s18', 'Half'), 'img', 'k81', move='in_r', x=0.8, ov=[('label', 'COLOMBIAN AMAZON · 2023')])
shot(S('s18', 'Four'), 'img', 'k81', move='push', focus=(0.45, 0.5))
shot(S('s18', 'Their'), 'img', 'k03', move='in', dim=0.6)
shot(S('s18', 'The', 6), 'img', 'k55', move='in', dim=0.75)
shot(S('s18', 'For'), 'img', 'k81', move='push', focus=(0.5, 0.5), dim=0.45, ov=[('stat', '40 DAYS', 'FOUR CHILDREN ALONE IN THE JUNGLE', (0, 40, 1.6))], hit=True)
shot(S('s18', 'Just'), 'img', 'k45', move='in')
shot(S('s18', 'Ninety-one'), 'img', 'k03', move='in', dim=0.7)
shot(S('s18', 'One'), 'img', 'k04', move='in')
shot(S('s18', 'And'), 'img', 'k83', move='in', x=0.9)
shot(S('s18', 'If'), 'end', None, x=1.0)
SH = [s for s in SH if s is not None]

for i, s in enumerate(SH):
    s['end'] = SH[i + 1]['t'] if i + 1 < len(SH) else END
    s['w0'] = s['t'] - s['x'] / 2
    s['w1'] = s['end'] + (SH[i + 1]['x'] / 2 if i + 1 < len(SH) else 0)
SH[0]['w0'] = 0.0

def check():
    ok = True
    for i in range(1, len(SH)):
        if SH[i]['t'] <= SH[i - 1]['t'] + 0.3:
            print('ERRO ordem/curto', i, SH[i - 1]['src'], SH[i]['src'], round(SH[i - 1]['t'], 2), round(SH[i]['t'], 2)); ok = False
    return ok

# ------------------------------------------------------------------ look
rng = np.random.default_rng(11)
GRAIN = [np.asarray(Image.fromarray(rng.normal(0, 8, (H // 2, W // 2)).astype(np.float32)).resize((W, H), Image.BILINEAR))[..., None] for _ in range(8)]
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.42 * np.clip(((xx - W / 2) / (W / 2)) ** 2 * 0.6 + ((yy - H / 2) / (H / 2)) ** 2 * 0.9, 0, 1) ** 1.3)[..., None].astype(np.float32)
del yy, xx

def finish(a, fi):
    a = a.astype(np.float32)
    a = (a - 128) * 1.07 + 125
    a = a * VIG + GRAIN[fi % len(GRAIN)]
    a[:BAR] = 0
    a[H - BAR:] = 0
    return np.clip(a, 0, 255).astype(np.uint8)

# ------------------------------------------------------------------ sources
@lru_cache(8)
def load_img(name):
    if name == 'k30x':  # altura: nuvens em cima, floresta embaixo (composicao vertical)
        a = Image.open(A('img', 'k33.png')).convert('RGB')
        b = Image.open(A('img', 'k02.png')).convert('RGB')
        ov = 200
        im = Image.new('RGB', (1280, 1440 - ov))
        im.paste(a, (0, 0))
        im.paste(b.crop((0, ov, 1280, 720)), (0, 720))
        m = Image.linear_gradient('L').resize((1280, ov))
        im.paste(b.crop((0, 0, 1280, ov)), (0, 720 - ov), m)
        return im
    if name == 'k75x':
        return Image.open(A('img', 'k69.png')).convert('RGB').filter(ImageFilter.GaussianBlur(2))
    return Image.open(A('img', name + '.png')).convert('RGB')

def kb(src, move, p, lt, focus=(0.5, 0.5)):
    sw, sh = src.size
    base = max(W / sw, H / sh)
    fx, fy, rot = 0.5, 0.5, 0.0
    if move == 'in':
        z = 1.04 + 0.13 * p
    elif move == 'out':
        z = 1.17 - 0.13 * p
    elif move == 'push':
        z = 1.03 + 0.30 * ease(p) ; fx = 0.5 + (focus[0] - 0.5) * p; fy = 0.5 + (focus[1] - 0.5) * p
    elif move in ('in_l', 'in_r'):
        z = 1.12 + 0.04 * p
        dx = 0.07 * (p - 0.5)
        fx = 0.5 + (dx if move == 'in_r' else -dx)
    elif move == 'shake':
        z = 1.16
        amp = 0.010 * max(0.25, 1 - lt / 1.2)
        fx, fy = 0.5 + amp * math.sin(lt * 53), 0.5 + amp * math.cos(lt * 47)
    elif move == 'fall':  # queda: zoom lento + tremor + leve rotacao
        z = 1.12 + 0.25 * p
        rot = 2.5 * math.sin(lt * 0.9)
        fx = 0.5 + 0.004 * math.sin(lt * 31); fy = 0.5 + 0.004 * math.cos(lt * 27)
    elif move == 'spin':
        z = 1.32
        rot = 9 * p - 4.5
    elif move == 'dive':  # mergulho em direcao a copa
        z = 1.0 + 0.45 * ease(p)
    else:
        z = 1.08
    if src.size[1] > src.size[0]:  # composicao vertical: desce de cima para baixo
        base = W / sw
        z = 1.0
        fy = 0.0 + ease(p)
    scale = base * z
    vw, vh = W / scale, H / scale
    cx = min(max(fx * sw, vw / 2), sw - vw / 2)
    cy = min(max(fy * sh, vh / 2), sh - vh / 2)
    th = math.radians(rot)
    c, s_ = math.cos(th) / scale, math.sin(th) / scale
    # mapeia saida -> origem: src = C + R/scale * (out - O)
    a, b, d, e = c, -s_, s_, c
    x0 = cx - (a * W / 2 + b * H / 2)
    y0 = cy - (d * W / 2 + e * H / 2)
    return src.transform((W, H), Image.AFFINE, (a, b, x0, d, e, y0), resample=Image.BICUBIC)

class VidReader:
    def __init__(self, name, off, slow):
        self.src, self.off, self.slow = A('vid', name + '.mp4'), off, slow
        self.p, self.next = None, None

    def get(self, idx):
        if self.p is None or idx != self.next:
            if self.p:
                self.p.kill()
            ss = self.off + idx / FPS / self.slow
            vf = f'setpts={self.slow:.4f}*PTS,fps={FPS},scale={W}:{H}:flags=lanczos,tpad=stop_mode=clone:stop_duration=60'
            self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-i', self.src, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                      stdout=subprocess.PIPE)
            self.next = idx
        buf = self.p.stdout.read(W * H * 3)
        self.next = idx + 1
        if len(buf) < W * H * 3:
            return getattr(self, 'last', Image.new('RGB', (W, H)))
        self.last = Image.frombytes('RGB', (W, H), buf)
        return self.last

READERS = {}
def vid_frame(i, s, gt):
    if i not in READERS:
        L = s['w1'] - s['w0']
        d0 = dur(A('vid', s['src'] + '.mp4')) - s.get('off', 0)
        READERS[i] = VidReader(s['src'], s.get('off', 0), max(1.0, min(L / d0, 2.0)))
    fr = READERS[i].get(int(round((gt - s['w0']) * FPS)))
    z0, z1 = s.get('zoom', (1.0, 1.06))
    p = (gt - s['w0']) / max(0.01, s['w1'] - s['w0'])
    z = z0 + (z1 - z0) * p
    if z > 1.001:
        vw, vh = W / z, H / z
        fr = fr.transform((W, H), Image.AFFINE, (1 / z, 0, (W - vw) / 2, 0, 1 / z, (H - vh) / 2), resample=Image.BILINEAR)
    return fr

# ------------------------------------------------------------------ maps
@lru_cache(None)
def geo():
    import shapely.geometry as sg
    cs = json.load(open(A('assets', 'countries.geojson')))
    rv = json.load(open(A('assets', 'rivers.geojson')))
    return cs, rv

MAPDEF = {
    'panguana': dict(lat=(-15.5, -3.0), lonc=-75.2, pts=[('LIMA', -12.05, -77.04, 'city'), ('PANGUANA', -9.61, -74.94, 'star')], route=None),
    'route': dict(lat=(-14.0, -6.5), lonc=-75.6, pts=[('LIMA', -12.02, -77.11, 'city'), ('PUCALLPA', -8.38, -74.57, 'city')],
                  route=[(-12.02, -77.11), (-8.38, -74.57)]),
}

@lru_cache(None)
def map_base(name):
    import shapely.geometry as sg
    m = MAPDEF[name]
    lat0, lat1 = m['lat']
    k = math.cos(math.radians((lat0 + lat1) / 2))
    wdeg = (lat1 - lat0) * (W / H) / k
    lon0, lon1 = m['lonc'] - wdeg / 2, m['lonc'] + wdeg / 2
    S = 2
    P = lambda la, lo: ((lo - lon0) / (lon1 - lon0) * W * S, (lat1 - la) / (lat1 - lat0) * H * S)
    box = sg.box(lon0 - 2, lat0 - 2, lon1 + 2, lat1 + 2)
    img = Image.new('RGB', (W * S, H * S), (12, 26, 34))
    d = ImageDraw.Draw(img)
    cs, rv = geo()
    def polys(g):
        g = sg.shape(g).intersection(box)
        if g.is_empty:
            return []
        return [x for x in (g.geoms if hasattr(g, 'geoms') else [g]) if x.geom_type == 'Polygon']
    for f in cs['features']:
        peru = f['properties']['NAME'] == 'Peru'
        for p in polys(f['geometry']):
            d.polygon([P(y, x) for x, y in p.exterior.coords], fill=(44, 58, 44) if peru else (30, 38, 34))
            d.line([P(y, x) for x, y in p.exterior.coords], fill=(120, 132, 110) if peru else (70, 80, 72), width=4 if peru else 2)
    for f in rv['features']:
        g = sg.shape(f['geometry']).intersection(box)
        if g.is_empty:
            continue
        for l in (g.geoms if hasattr(g, 'geoms') else [g]):
            if l.geom_type == 'LineString':
                d.line([P(y, x) for x, y in l.coords], fill=(70, 120, 150), width=3)
    for la in range(-20, 0, 2):
        d.line([P(la, lon0), P(la, lon1)], fill=(20, 40, 50), width=1)
    img = img.resize((W, H), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    for nm, la, lo in (('PACIFIC OCEAN', -12.8, -79.6), ('BRAZIL', -8.0, -71.0) if name == 'panguana' else ('BRAZIL', -8.5, -72.2)):
        x, y = P(la, lo)
        if 0 < x / S < W and 0 < y / S < H:
            d.text((x / S, y / S), nm, font=font('oswald', 30, 400), fill=(110, 130, 130), anchor='mm')
    return img, (lambda la, lo: tuple(v / S for v in P(la, lo)))

def map_frame(name, lt, L):
    base, P = map_base(name)
    m = MAPDEF[name]
    img = base.copy()
    d = ImageDraw.Draw(img, 'RGBA')
    if m['route']:
        p = ease((lt - 0.4) / max(1.5, L * 0.6))
        (a1, o1), (a2, o2) = m['route']
        x1, y1 = P(a1, o1); x2, y2 = P(a2, o2)
        xe, ye = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
        for wd, al in ((20, 40), (11, 90), (5, 255)):
            d.line([(x1, y1), (xe, ye)], fill=(225, 55, 45, al), width=wd)
        ang = math.atan2(y2 - y1, x2 - x1)
        pts = [(18, 0), (-12, -9), (-6, 0), (-12, 9)]
        d.polygon([(xe + px * math.cos(ang) - py * math.sin(ang), ye + px * math.sin(ang) + py * math.cos(ang)) for px, py in pts], fill=(255, 240, 230, 255))
        if p > 0.95:
            q = ease((lt - 0.4 - L * 0.6) / 0.8)
            shadow_text(d, (W / 2, H - BAR - 120), 'UNDER ONE HOUR · OVER THE ANDES', font('oswald', 44, 600), fill=(240, 220, 210, int(255 * q)), anchor='mm')
    for nm, la, lo, kind in m['pts']:
        cx, cy = P(la, lo)
        a = ease((lt - (0.3 if kind == 'city' else 1.0)) / 0.5)
        if kind == 'star':
            r = 16 + 6 * math.sin(lt * 4)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(240, 200, 80, int(230 * a)), width=4)
            d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(240, 200, 80, int(255 * a)))
        else:
            d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(245, 240, 230, int(255 * a)))
        shadow_text(d, (cx + 28, cy), nm, font('oswald', 50, 600), anchor='lm', sh=3, fill=(245, 240, 230, int(255 * a)))
    z = 1.0 + 0.07 * (lt / max(L, 1))
    img = img.resize((int(W * z), int(H * z)), Image.BICUBIC)
    ox, oy = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((ox, oy, ox + W, oy + H))

# ------------------------------------------------------------------ overlays
def shadow_text(d, xy, txt, f, fill=(255, 255, 255, 255), sh=4, anchor='la', spacing=10, align='left'):
    x, y = xy
    al = fill[3] if len(fill) == 4 else 255
    d.multiline_text((x + sh, y + sh), txt, font=f, fill=(0, 0, 0, int(170 * al / 255)), anchor=anchor, spacing=spacing, align=align)
    d.multiline_text((x, y), txt, font=f, fill=fill, anchor=anchor, spacing=spacing, align=align)

def draw_overlays(img, s, lt, gt):
    ov = s.get('ov', [])
    if not ov:
        return img
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for o in ov:
        k = o[0]
        if k == 'type':
            txt = o[1]
            n = int(max(0, lt - 0.3) * 24)
            cur = '▌' if int(gt * 2.2) % 2 == 0 else ''
            f = font('type', 56 if '\n' in txt else 80)
            shadow_text(d, (120, 150), txt[:n] + cur, f, fill=(240, 232, 210, 255))
        elif k == 'title':
            a = ease((lt - 0.3) / 0.35)
            sc = 1.0 + 0.25 * (1 - a)
            f1, f2 = font('bebas', int(150 * sc)), font('oswald', 42, 500)
            col = (245, 240, 230, int(255 * a))
            d.text((W / 2 + 5, H / 2 - 20 + 5), o[1], font=f1, fill=(0, 0, 0, int(160 * a)), anchor='ms')
            d.text((W / 2, H / 2 - 20), o[1], font=f1, fill=col, anchor='ms')
            d.line([(W / 2 - 420 * a, H / 2 + 12), (W / 2 + 420 * a, H / 2 + 12)], fill=(200, 40, 40, int(255 * a)), width=4)
            b = ease((lt - 1.0) / 0.8)
            d.text((W / 2, H / 2 + 80), o[2], font=f2, fill=(220, 215, 205, int(255 * b)), anchor='ms')
        elif k == 'chapter':
            a = ease((lt - 0.2) / 0.6) * (1 - ease((lt - 4.2) / 0.8))
            if a <= 0:
                continue
            d.text((W / 2, H / 2 - 105), o[1], font=font('oswald', 50, 500), fill=(225, 65, 58, int(255 * a)), anchor='ms')
            sp = 1 + 0.03 * lt
            shadow_text(d, (W / 2, H / 2 + 60), o[2], font('bebas', int(160 * sp)), fill=(248, 244, 236, int(255 * a)), anchor='ms', sh=5)
        elif k == 'label':
            a = ease((lt - 0.3) / 0.6)
            if a <= 0:
                continue
            f = font('oswald', 42, 500)
            tw = d.textlength(o[1], font=f)
            x0, y0 = 110, H - BAR - 230
            d.rectangle([x0, y0, x0 + 10, y0 + 62], fill=(200, 35, 35, int(255 * a)))
            d.rectangle([x0 + 10, y0, x0 + 10 + (tw + 50) * a, y0 + 62], fill=(10, 10, 12, int(205 * a)))
            if a > 0.6:
                d.text((x0 + 35, y0 + 31), o[1], font=f, fill=(240, 236, 228, int(255 * (a - 0.6) / 0.4)), anchor='lm')
        elif k == 'stat':
            big, small, cnt = o[1], o[2], o[3]
            a = ease((lt - 0.1) / 0.3)
            sc = 1.0 + 0.35 * (1 - ease((lt - 0.1) / 0.25))
            if cnt:
                v0, v1, dd = cnt
                v = int(round(v0 + (v1 - v0) * ease((lt - 0.1) / dd)))
                big = re.sub(r'[\d,]+', f'{v:,}', big, count=1)
            f1, f2 = font('bebas', int(240 * sc)), font('oswald', 46, 500)
            d.text((W / 2 + 6, H / 2 + 66), big, font=f1, fill=(0, 0, 0, int(150 * a)), anchor='ms')
            d.text((W / 2, H / 2 + 60), big, font=f1, fill=(250, 246, 236, int(255 * a)), anchor='ms')
            b = ease((lt - 0.5) / 0.5)
            d.text((W / 2, H / 2 + 140), small, font=f2, fill=(220, 65, 58, int(255 * b)), anchor='ms')
        elif k == 'quote':
            a = ease((lt - 0.3) / 0.8)
            shadow_text(d, (W / 2, H / 2 - 10), o[1], font('bebas', 130), fill=(248, 244, 236, int(255 * a)), anchor='mm', align='center', spacing=6, sh=5)
            if o[2]:
                b = ease((lt - 1.2) / 0.7)
                d.text((W / 2, H / 2 + 150), o[2], font=font('oswald', 38, 400), fill=(215, 70, 60, int(255 * b)), anchor='ms')
        elif k in ('list', 'rule'):
            if k == 'list':
                head, items = o[1], o[2]
                times = [0.9 + 0.75 * j for j in range(len(items))]
            else:
                head, items = None, o[1]
                times = [max(0.2, tt - s['t']) for tt in o[2]]
            y = H / 2 - (len(items) * 80) / 2 - (40 if head else 0)
            if head:
                a = ease((lt - 0.2) / 0.5)
                d.text((180, y), head, font=font('oswald', 40, 500), fill=(215, 65, 58, int(255 * a)), anchor='ls')
                y += 40
            for j, it in enumerate(items):
                a = ease((lt - times[j]) / 0.35)
                if a <= 0:
                    continue
                x = 180 - 40 * (1 - a)
                f = font('bebas', 86 if k == 'rule' else 72)
                d.rectangle([x - 40, y + 28, x - 22, y + 46], fill=(205, 45, 40, int(255 * a)))
                shadow_text(d, (x, y + 64), it, f, fill=(246, 242, 234, int(255 * a)), anchor='ls')
                y += 96 if k == 'rule' else 82
    img = img.convert('RGBA')
    img.alpha_composite(layer)
    return img.convert('RGB')

def card_frame(s, lt):
    img = Image.new('RGB', (W, H), (5, 5, 7))
    if not s.get('text'):
        return img
    d = ImageDraw.Draw(img)
    a = ease(lt / 0.12)
    sc = 1.0 + 0.035 * min(lt, 3)
    d.text((W / 2, H / 2 + 60), s['text'], font=font('bebas', int(180 * sc)), fill=(int(242 * a), int(238 * a), int(230 * a)), anchor='ms')
    if s.get('sub'):
        b = ease((lt - 0.6) / 0.6)
        d.text((W / 2, H / 2 + 140), s['sub'], font=font('oswald', 42, 500), fill=(int(215 * b), int(65 * b), int(58 * b)), anchor='ms')
    return img

def end_frame(lt):
    img = kb(load_img('k83'), 'in', min(1, lt / 8), lt)
    img = Image.eval(img, lambda v: int(v * 0.32))
    d = ImageDraw.Draw(img, 'RGBA')
    a = ease((lt - 0.5) / 1.0)
    shadow_text(d, (W / 2, H / 2 - 10), 'MORE TRUE STORIES', font('bebas', 150), fill=(245, 240, 230, int(255 * a)), anchor='ms')
    b = ease((lt - 1.3) / 0.8)
    d.text((W / 2, H / 2 + 70), 'SOME OF THEM ARE EVEN STRANGER', font=font('oswald', 40, 400), fill=(215, 70, 60, int(255 * b)), anchor='ms')
    return img

# ------------------------------------------------------------------ HUD (dias)
def day_at(gt):
    if segin('s09') <= gt < segin('s10'):
        return 'DAY 1'
    if segin('s12') <= gt < segin('s13'):
        return 'DAY 4'
    if segin('s13') <= gt < segin('s14'):
        p = (gt - segin('s13')) / (segin('s14') - segin('s13'))
        return f'DAY {5 + min(4, int(p * 5))}'
    if segin('s14') <= gt < segin('s15'):
        return 'DAY 10'
    if segin('s15') <= gt < at('s15', 'After') - 0.3:
        return 'DAY 11'
    return None

def hud(img, gt):
    lab = day_at(gt)
    if not lab:
        return img
    prev = day_at(gt - 0.4)
    pulse = 1.0 if prev == lab else 1.25
    d = ImageDraw.Draw(img, 'RGBA')
    x, y = W - 110, BAR + 50
    d.text((x, y + 4), 'SURVIVAL', font=font('oswald', 26, 500), fill=(215, 65, 58, 230), anchor='ra')
    shadow_text(d, (x, y + 34), lab, font('bebas', int(76 * pulse)), fill=(246, 242, 234, 240), anchor='ra', sh=3)
    return img

# ------------------------------------------------------------------ subtitles (queimadas)
def sub_lines():
    lines = []
    for s in SEGS:
        cur = []
        for w in words[s]:
            if w['text'].startswith('['):
                continue
            cur.append(w)
            txt = ' '.join(x['text'] for x in cur)
            if re.search(r'[.!?:]$|\.\.\.$', w['text']) or len(txt) > 40 or (w['text'].endswith(',') and len(txt) > 24):
                lines.append([cur[0]['start'], cur[-1]['end'] + 0.25, txt]); cur = []
        if cur:
            lines.append([cur[0]['start'], cur[-1]['end'] + 0.25, ' '.join(x['text'] for x in cur)])
    for i in range(len(lines) - 1):
        lines[i][1] = min(lines[i][1], lines[i + 1][0] - 0.02)
    return lines

SUBS = sub_lines()
SUB_STARTS = [l[0] for l in SUBS]

@lru_cache(64)
def sub_img(i):
    txt = SUBS[i][2]
    f = font('inter', 44, 600)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw = int(tmp.textlength(txt, font=f)) + 40
    im = Image.new('RGBA', (tw, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((tw / 2, 40), txt, font=f, fill=(244, 244, 240, 255), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0, 230))
    return im

def subs(img, gt):
    import bisect
    i = bisect.bisect_right(SUB_STARTS, gt) - 1
    if i < 0 or gt > SUBS[i][1]:
        return img
    im = sub_img(i)
    img.paste(im, (int(W / 2 - im.width / 2), H - BAR - 96), im)
    return img

# ------------------------------------------------------------------ frame
def shot_frame(i, gt):
    s = SH[i]
    lt = gt - s['t']
    L = s['w1'] - s['w0']
    p = (gt - s['w0']) / max(L, 0.01)
    k = s['kind']
    if k == 'img':
        fr = kb(load_img(s['src']), s.get('move', 'in'), p, lt, s.get('focus', (0.5, 0.5)))
    elif k == 'video':
        fr = vid_frame(i, s, gt)
    elif k == 'map':
        fr = map_frame(s['src'], max(lt, 0), s['end'] - s['t'])
    elif k == 'card':
        fr = card_frame(s, max(lt, 0))
    else:
        fr = end_frame(max(lt, 0))
    if s.get('gray'):
        fr = Image.blend(fr, fr.convert('L').convert('RGB'), 0.75)
    if s.get('warm'):
        r, g, b = fr.split()
        fr = Image.merge('RGB', (r.point(lambda v: min(255, int(v * 1.08 + 6))), g, b.point(lambda v: int(v * 0.88))))
    dm = s.get('dim', 1.0)
    if s.get('ov') and s.get('dimov'):
        dm = s['dimov'] if lt > 0 else dm
    if dm != 1.0:
        fr = fr.point(lambda v, dm=dm: int(v * dm))
    if s.get('rain'):
        fr = rain(fr, gt)
    fr = draw_overlays(fr, s, lt, gt)
    if s.get('flash') and 0 <= lt < 0.3:
        fr = Image.blend(fr, Image.new('RGB', (W, H), (255, 255, 255)), 0.85 * (1 - lt / 0.3))
    return fr

RAIN = None
def rain(fr, gt):
    global RAIN
    if RAIN is None:
        r = np.random.default_rng(3)
        im = Image.new('L', (W, H * 2), 0)
        d = ImageDraw.Draw(im)
        for _ in range(900):
            x, y, l = r.integers(0, W), r.integers(0, H * 2), r.integers(20, 60)
            d.line([(x, y), (x - l * 0.15, y + l)], fill=int(r.integers(40, 110)), width=1)
        RAIN = im
    off = int(gt * 1400) % H
    m = RAIN.crop((0, off, W, off + H))
    return Image.composite(Image.new('RGB', (W, H), (200, 205, 210)), fr, m)

def frame(fi):
    gt = fi / FPS
    act = [i for i, s in enumerate(SH) if s['w0'] <= gt < s['w1']]
    if not act:
        act = [len(SH) - 1]
    if len(act) == 1:
        fr = shot_frame(act[0], gt)
    else:
        i, j = act[-2], act[-1]
        s = SH[j]
        a = ease((gt - s['w0']) / max(s['x'], 0.01))
        fr = Image.blend(shot_frame(i, gt), shot_frame(j, gt), a)
    fr = hud(fr, gt)
    fr = subs(fr, gt)
    a = finish(np.asarray(fr), fi)
    fo = min(1.0, (END - gt) / 2.5)
    if fo < 1:
        a = (a * max(fo, 0)).astype(np.uint8)
    if gt < 0.6:
        a = (a * (gt / 0.6)).astype(np.uint8)
    return a

def render_chunk(args):
    ci, f0, f1 = args
    out = os.path.join(OUT, 'chunks', f'c{ci:03d}.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-threads', '1', '-g', '60', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        enc.stdin.write(frame(fi).tobytes())
    enc.stdin.close(); enc.wait()
    for r in READERS.values():
        if r.p:
            r.p.kill()
    READERS.clear()
    return ci

# ------------------------------------------------------------------ audio
def build_audio(path):
    fc, inp, labs = [], [], []
    def add(p):
        inp.extend(['-i', p]); return len(inp) // 2 - 1
    for k, s in enumerate(SEGS):
        i = add(A('audio', s + '.mp3'))
        ms = int(seg_start[s] * 1000)
        fc.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},apad=whole_dur={END:.2f}[n{k}]')
    fc.append(f"{''.join(f'[n{k}]' for k in range(len(SEGS)))}amix=inputs={len(SEGS)}:normalize=0,asplit=2[narr][sc]")
    # trilha em blocos: (arquivo, inicio_no_video, fim_no_video, offset_no_arquivo, volume)
    t_break = at('s06', 'A', 2)
    t_after = at('s15', 'After') - 1.0
    blocks = [
        ('music.mp3', 0.0, segin('s03') + 1.5, 0.0, 0.50),
        ('m_backstory.mp3', segin('s03') - 0.5, segin('s06') + 1.0, 0.0, 0.45),
        ('music.mp3', segin('s06') - 0.5, t_break + 0.3, 70.0, 0.55),
        ('m_survival.mp3', segin('s07') + 3.0, t_after + 1.5, 0.0, 0.42),
        ('m_finale.mp3', t_after - 0.5, END, 0.0, 0.46),
    ]
    ml = []
    for k, (f, a, b, off, vol) in enumerate(blocks):
        L = b - a
        src = A('audio', f)
        i = add(src)
        D = dur(src) - off
        loop = '' if L <= D else f'aloop=loop={int(L // D) + 1}:size={int(D * 48000)},'
        ms = int(a * 1000)
        fc.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=start={off},asetpts=PTS-STARTPTS,{loop}atrim=0:{L:.2f},'
                  f'afade=t=in:d=1.2,afade=t=out:st={L - 1.6:.2f}:d=1.6,volume={vol},adelay={ms}|{ms},apad=whole_dur={END:.2f}[m{k}]')
        ml.append(f'[m{k}]')
    fc.append(f"{''.join(ml)}amix=inputs={len(ml)}:normalize=0[mus0]")
    fc.append('[mus0][sc]sidechaincompress=threshold=0.025:ratio=7:attack=25:release=700[mus]')
    # efeitos
    fx = []
    def sfx(f, t0, vol, extra='', name=None):
        i = add(A('audio', f) if os.path.exists(A('audio', f)) else A('..', 'dbcooper-amostra', 'audio', f))
        lab = f'f{len(fx)}'
        ms = int(max(0, t0) * 1000)
        fc.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{extra}volume={vol},adelay={ms}|{ms},apad=whole_dur={END:.2f}[{lab}]')
        fx.append(f'[{lab}]')
    sfx('sfx_thunder.mp3', 0.05, 1.0, 'aecho=0.8:0.85:600|1100:0.45|0.3,')
    for s in SH:
        if s.get('thunder'):
            sfx('sfx_thunder.mp3', s['t'] - 0.05, 0.9)
        if s.get('hit'):
            sfx('sfx_hit.mp3', s['t'] + (0.1 if s['kind'] != 'card' else 0), 0.7)
        if s.get('whoosh'):
            sfx('sfx_whoosh.mp3', s['t'] - 0.45, 0.45)
        if s.get('wind'):
            sfx('sfx_wind.mp3', s['t'] - 0.3, 0.7, 'afade=t=in:d=0.6,afade=t=out:st=4.5:d=2.5,')
        for o in s.get('ov', []):
            if o[0] == 'type':
                sfx('sfx_type.mp3', s['t'] + 0.3, 0.35)
            if o[0] == 'stat' and not s.get('hit'):
                sfx('sfx_hit.mp3', s['t'] + 0.1, 0.5)
    # cabine (s04 'And' ate a ruptura), selva (s08 'When' ate s16), chuva em s13
    def bed(f, a, b, vol, extra=''):
        i = add(A('audio', f) if os.path.exists(A('audio', f)) else A('..', 'dbcooper-amostra', 'audio', f))
        L = b - a
        D = dur(inp[2 * i + 1])
        lab = f'f{len(fx)}'
        ms = int(a * 1000)
        fc.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,aloop=loop={int(L // D) + 1}:size={int(D * 48000)},atrim=0:{L:.2f},{extra}'
                  f'afade=t=in:d=2,afade=t=out:st={L - 2:.2f}:d=2,volume={vol},adelay={ms}|{ms},apad=whole_dur={END:.2f}[{lab}]')
        fx.append(f'[{lab}]')
    bed('sfx_cabin.mp3', at('s04', 'And'), t_break + 0.1, 0.30)
    bed('sfx_jungle.mp3', at('s08', 'When') - 0.5, segin('s16') + 1.0, 0.30)
    L = segin('s14') - segin('s13')
    fc.append(f'anoisesrc=color=pink:amplitude=0.35:duration={L:.2f}:sample_rate=48000,highpass=f=900,lowpass=f=7000,'
              f'afade=t=in:d=2,afade=t=out:st={L - 2:.2f}:d=2,aformat=channel_layouts=stereo,adelay={int(segin("s13") * 1000)}|{int(segin("s13") * 1000)},apad=whole_dur={END:.2f}[rain]')
    fx.append('[rain]')
    n = 2 + len(fx)
    fc.append(f"[narr][mus]{''.join(fx)}amix=inputs={n}:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    cmd = ['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[a]', '-c:a', 'pcm_s16le', '-ar', '48000', '-t', f'{END:.2f}', path]
    subprocess.run(cmd, check=True)

def write_srt(path):
    def ts(x):
        return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x % 1) * 1000)) % 1000:03d}'
    with open(path, 'w') as f:
        for k, (a, b, t) in enumerate(SUBS, 1):
            f.write(f'{k}\n{ts(a)} --> {ts(b)}\n{t}\n\n')

if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'chunks'), exist_ok=True)
    ok = check()
    for e in ERRS:
        print('ANCORA FALTANDO', e)
    print(f'{len(SH)} planos · {END / 60:.2f} min · {NFRAMES} quadros')
    if 'plan' in sys.argv:
        for i, s in enumerate(SH):
            print(f"{i:03d} {s['t']:7.2f} {s['end'] - s['t']:5.2f} {s['kind']:5s} {s.get('src') or s.get('text', '')}")
        sys.exit(0 if ok else 1)
    if 'still' in sys.argv:
        for x in sys.argv[2:]:
            Image.fromarray(frame(int(float(x) * FPS))).save(os.path.join(OUT, f'still_{x}.jpg'), quality=88)
        sys.exit()
    if 'audio' in sys.argv:
        build_audio(os.path.join(OUT, 'mix.wav')); sys.exit()
    f_from = int(float(sys.argv[sys.argv.index('--from') + 1]) * FPS) if '--from' in sys.argv else 0
    f_to = int(float(sys.argv[sys.argv.index('--to') + 1]) * FPS) if '--to' in sys.argv else NFRAMES
    NCH = int(os.environ.get('CHUNKS', 24))
    edges = np.linspace(f_from, f_to, NCH + 1).astype(int)
    jobs = [(k, edges[k], edges[k + 1]) for k in range(NCH) if edges[k + 1] > edges[k]]
    with Pool(int(os.environ.get('PROCS', os.cpu_count()))) as pool:
        for ci in pool.imap_unordered(render_chunk, jobs):
            print('bloco', ci, 'ok', flush=True)
    with open(os.path.join(OUT, 'chunks.txt'), 'w') as f:
        for k, _, _ in jobs:
            f.write(f"file 'chunks/c{k:03d}.mp4'\n")
    if not os.path.exists(os.path.join(OUT, 'mix.wav')):
        build_audio(os.path.join(OUT, 'mix.wav'))
    write_srt(os.path.join(OUT, 'Juliane_Koepcke_EN.srt'))
    final = os.path.join(OUT, 'Juliane_Koepcke_EN.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(OUT, 'chunks.txt'),
                    '-ss', f'{f_from / FPS:.3f}', '-i', os.path.join(OUT, 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', final], check=True)
    print('PRONTO', final)
