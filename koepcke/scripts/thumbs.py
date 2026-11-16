#!/usr/bin/env python3
"""3 capas 1280x720 para teste A/B (ver lancamento.md, secao 2)."""
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, *p)
W, H = 1280, 720
BEBAS = A('assets', 'BebasNeue.ttf')
OUT = A('render', 'thumbs')
os.makedirs(OUT, exist_ok=True)

def crop_zoom(im, z, cx, cy):
    sw, sh = im.size
    w, h = sw / z, sh / z
    x0 = min(max(cx * sw - w / 2, 0), sw - w)
    y0 = min(max(cy * sh - h / 2, 0), sh - h)
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)

def vignette(im, k=0.55):
    m = Image.radial_gradient('L').resize((W, H)).point(lambda v: int(255 - v * k))
    return Image.composite(im, Image.new('RGB', (W, H)), m)

def grade(im, sat=1.0, bright=1.0, contrast=1.15):
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    return ImageEnhance.Contrast(im).enhance(contrast)

def text(d, xy, lines, size, anchor='la', glow=True, spacing=-4):
    f = ImageFont.truetype(BEBAS, size)
    x, y = xy
    for parts in lines:  # cada linha: [(texto, cor), ...]
        tw = sum(d.textlength(t, font=f) for t, _ in parts)
        cx = x - tw if anchor == 'ra' else x
        for t, col in parts:
            d.text((cx, y), t, font=f, fill=col, stroke_width=6, stroke_fill=(0, 0, 0))
            cx += d.textlength(t, font=f)
        y += size + spacing

def shadow(im, box, alpha=150, blur=40):
    sh = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sh).rectangle(box, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new('RGB', (W, H)), im, sh)

WHITE, ORANGE, YELLOW, RED = (250, 248, 242), (255, 122, 26), (255, 212, 0), (224, 36, 36)

# A - a queda
im = Image.open(A('img', 'k27.png')).convert('RGB')
im = crop_zoom(im, 2.0, 0.37, 0.43).filter(ImageFilter.UnsharpMask(2, 80, 2))
im = grade(im, sat=0.55, bright=0.95, contrast=1.25)
im = vignette(im, 0.7)
im = shadow(im, (40, 150, 560, 600))
d = ImageDraw.Draw(im)
text(d, (60, 170), [[('STILL IN', WHITE)], [('HER ', WHITE), ('SEAT', ORANGE)]], 180)
im.save(os.path.join(OUT, 'A_still_in_her_seat.jpg'), quality=94)

# B - a sobrevivente
im = Image.open(A('img', 'k40.png')).convert('RGB')
im = crop_zoom(im, 1.25, 0.36, 0.5).filter(ImageFilter.UnsharpMask(2, 60, 2))
im = grade(im, sat=0.75, bright=0.85, contrast=1.2)
im = vignette(im, 0.6)
im = shadow(im, (700, 120, 1260, 620))
d = ImageDraw.Draw(im)
text(d, (1230, 150), [[('11 DAYS.', YELLOW)], [('ALONE.', WHITE)]], 175, anchor='ra')
im.save(os.path.join(OUT, 'B_11_days_alone.jpg'), quality=94)

# C - 1 de 92
im = Image.open(A('img', 'k38.png')).convert('RGB')
im = crop_zoom(im, 1.3, 0.66, 0.55)
im = grade(im, sat=0.6, bright=0.85, contrast=1.25)
im = vignette(im, 0.65)
im = shadow(im, (40, 140, 640, 640))
d = ImageDraw.Draw(im)
text(d, (70, 140), [[('1 ', RED), ('OF 92', WHITE)]], 260)
text(d, (80, 410), [[('SURVIVED', WHITE)]], 110)
im.save(os.path.join(OUT, 'C_1_of_92.jpg'), quality=94)

# folha de comparacao (inclui teste de leitura em tamanho pequeno)
sheet = Image.new('RGB', (1280 * 3 // 2 + 40, 720 // 2 + 200), (18, 18, 18))
for i, n in enumerate(['A_still_in_her_seat', 'B_11_days_alone', 'C_1_of_92']):
    t = Image.open(os.path.join(OUT, n + '.jpg'))
    sheet.paste(t.resize((640, 360)), (i * 650 if i < 2 else 0, 0) if False else (0, 0))
sheet = Image.new('RGB', (1960, 560), (18, 18, 18))
for i, n in enumerate(['A_still_in_her_seat', 'B_11_days_alone', 'C_1_of_92']):
    t = Image.open(os.path.join(OUT, n + '.jpg'))
    sheet.paste(t.resize((640, 360)), (i * 660, 0))
    sheet.paste(t.resize((168, 94)), (i * 660, 400))
sheet.save(os.path.join(OUT, 'comparacao.jpg'), quality=90)
print('ok')
