#!/usr/bin/env python3
"""
stickvid — vídeo de boneco-palito (faceless) a custo zero, em 1 comando.

  roteiro.txt  ->  voz grátis  ->  tempos por palavra  ->  cenas desenhadas em código  ->  MP4

Uso:
  python stickvid.py roteiro.txt                       # voz Edge grátis (precisa internet)
  python stickvid.py roteiro.txt --voz piper --modelo pt_BR-faber-medium.onnx   # voz offline
  python stickvid.py roteiro.txt --audio minha_voz.mp3 # usa sua própria gravação
  python stickvid.py roteiro.txt --vertical            # Shorts/Reels/TikTok 9:16
  python stickvid.py roteiro.txt --sem-voz             # só testa a animação (vídeo mudo)

Formato do roteiro: uma cena por linha. Tags opcionais no começo da linha:
  [pose] texto narrado          pose: fala, aponta, pensa, comemora, triste, choque, anda, ombros
  [pose|objeto] texto           objeto: dinheiro, casa, pergunta, ideia, grafico_sobe, grafico_desce,
                                        relogio, celular, alerta, coracao
  [numero:R$ 10.000] texto      mostra um número/frase gigante na tela
  [dois:pose] texto             dois personagens conversando
Linhas vazias e linhas começando com # são ignoradas.

Dependências (todas grátis): Python 3.9+, ffmpeg, Pillow, edge-tts ou piper-tts, faster-whisper.
"""
import argparse, asyncio, json, math, multiprocessing as mp, os, re, shutil, subprocess, sys, tempfile, wave

from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------------- roteiro

POSES = {"fala", "aponta", "pensa", "comemora", "triste", "choque", "anda", "ombros"}
OBJETOS = {"dinheiro", "casa", "pergunta", "ideia", "grafico_sobe", "grafico_desce",
           "relogio", "celular", "alerta", "coracao"}

PALAVRAS_POSE = [  # se a linha não tiver tag, escolhe a pose pelo sentido
    (r"\b(dinheiro|r\$|\$|reais|dólar|lucro|ganh|renda|pag)", "aponta", "dinheiro"),
    (r"\b(casa|imóvel|aluguel|apartamento)", "aponta", "casa"),
    (r"\?", "pensa", "pergunta"),
    (r"\b(ideia|segredo|truque|descobr)", "comemora", "ideia"),
    (r"\b(cai|perd|queda|crise|dívida|prejuízo)", "triste", "grafico_desce"),
    (r"\b(cresc|sub|aument|dobr|multiplic)", "comemora", "grafico_sobe"),
    (r"\b(tempo|hora|minuto|dias|anos)", "pensa", "relogio"),
    (r"\b(celular|app|instagram|tiktok|youtube)", "aponta", "celular"),
    (r"\b(cuidado|nunca|erro|perigo|pare)", "choque", "alerta"),
    (r"\b(amor|família|filho|mãe|pai)", "fala", "coracao"),
]


def ler_roteiro(caminho):
    cenas = []
    for linha in open(caminho, encoding="utf-8"):
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        cena = {"pose": None, "objeto": None, "numero": None, "dois": False}
        m = re.match(r"^\[([^\]]+)\]\s*(.*)$", linha)
        if m:
            tag, linha = m.group(1).strip().lower(), m.group(2).strip()
            if tag.startswith("numero:"):
                cena["numero"] = m.group(1).split(":", 1)[1].strip()
                cena["pose"] = "aponta"
            else:
                if tag.startswith("dois:"):
                    cena["dois"] = True
                    tag = tag[5:]
                for parte in tag.split("|"):
                    parte = parte.strip()
                    if parte in POSES:
                        cena["pose"] = parte
                    elif parte in OBJETOS:
                        cena["objeto"] = parte
        if not cena["pose"] and not cena["numero"]:
            for rx, pose, obj in PALAVRAS_POSE:
                if re.search(rx, linha.lower()):
                    cena["pose"], cena["objeto"] = pose, cena["objeto"] or obj
                    break
        cena["pose"] = cena["pose"] or "fala"
        cena["texto"] = linha
        cenas.append(cena)
    if not cenas:
        sys.exit("Roteiro vazio.")
    return cenas


# ----------------------------------------------------------------------------- voz (grátis)

def gerar_voz(texto, saida, args):
    if args.voz == "edge":
        try:
            import edge_tts
        except ImportError:
            sys.exit("Instale: pip install edge-tts   (ou use --voz piper / --audio)")
        async def run():
            await edge_tts.Communicate(texto, args.voz_nome, rate=args.velocidade).save(saida)
        asyncio.run(run())
    elif args.voz == "piper":
        if not args.modelo:
            sys.exit("--voz piper precisa de --modelo caminho/voz.onnx (baixe grátis em huggingface.co/rhasspy/piper-voices)")
        wav = saida.rsplit(".", 1)[0] + ".wav"
        subprocess.run([sys.executable, "-m", "piper", "-m", args.modelo, "-f", wav],
                       input=texto.encode("utf-8"), check=True)
        return wav
    return saida


def duracao_audio(caminho):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", caminho], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


# ----------------------------------------------------------------------------- tempos por palavra

def tempos_whisper(audio, idioma, modelo):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    print("• transcrevendo para pegar o tempo de cada palavra (faster-whisper, grátis)…")
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language=idioma, word_timestamps=True)
    palavras = []
    for s in segs:
        for w in s.words or []:
            palavras.append({"w": w.word.strip(), "a": w.start, "b": w.end})
    return palavras or None


def norm(p):
    return re.sub(r"[^\w]", "", p.lower())


def distribuir(cenas, palavras, total):
    """Associa cada palavra do roteiro a um tempo. Usa o whisper quando há, senão estima."""
    roteiro = [(i, w) for i, c in enumerate(cenas) for w in c["texto"].split()]
    if palavras:
        # alinhamento guloso roteiro <-> transcrição (tolera pequenas diferenças)
        j, tempos = 0, []
        for _, w in roteiro:
            alvo, achou = norm(w), None
            for k in range(j, min(j + 6, len(palavras))):
                if norm(palavras[k]["w"]) == alvo:
                    achou = k
                    break
            if achou is None:
                achou = min(j, len(palavras) - 1)
            tempos.append((palavras[achou]["a"], palavras[achou]["b"]))
            j = achou + 1
        # garante tempos crescentes
        for k in range(1, len(tempos)):
            if tempos[k][0] < tempos[k - 1][0]:
                tempos[k] = (tempos[k - 1][1], max(tempos[k - 1][1] + 0.05, tempos[k][1]))
    else:
        pesos = [len(w) + 3 for _, w in roteiro]
        escala, t, tempos = total / sum(pesos), 0.0, []
        for p in pesos:
            tempos.append((t, t + p * escala * 0.85))
            t += p * escala
    for c in cenas:
        c["palavras"] = []
    for (i, w), (a, b) in zip(roteiro, tempos):
        cenas[i]["palavras"].append({"w": w, "a": a, "b": b})
    for i, c in enumerate(cenas):
        c["ini"] = 0.0 if i == 0 else c["palavras"][0]["a"]
    for i, c in enumerate(cenas):
        c["fim"] = cenas[i + 1]["ini"] if i + 1 < len(cenas) else total
    return cenas


# ----------------------------------------------------------------------------- desenho

TEMAS = {
    "claro":  {"fundo": (250, 247, 240), "linha": (25, 25, 30), "destaque": (255, 196, 0),
               "texto": (20, 20, 25), "contorno": (255, 255, 255), "chao": (225, 220, 210)},
    "escuro": {"fundo": (18, 18, 22), "linha": (245, 245, 245), "destaque": (255, 196, 0),
               "texto": (255, 255, 255), "contorno": (0, 0, 0), "chao": (40, 40, 48)},
}

# ângulos em graus (0 = para baixo). braço: ombro, cotovelo; perna: quadril, joelho
POSE_ANG = {
    "fala":     dict(be=(25, 20), bd=(-25, -20), pe=(12, 0), pd=(-12, 0), cab=0, tronco=0),
    "aponta":   dict(be=(95, 5), bd=(-25, -20), pe=(12, 0), pd=(-12, 0), cab=-5, tronco=-3),
    "pensa":    dict(be=(20, 30), bd=(-30, -140), pe=(10, 0), pd=(-10, 0), cab=8, tronco=2),
    "comemora": dict(be=(160, 10), bd=(-160, -10), pe=(18, -5), pd=(-18, 5), cab=-8, tronco=0),
    "triste":   dict(be=(8, 5), bd=(-8, -5), pe=(6, 0), pd=(-6, 0), cab=22, tronco=8),
    "choque":   dict(be=(120, 60), bd=(-120, -60), pe=(20, 0), pd=(-20, 0), cab=-10, tronco=-6),
    "anda":     dict(be=(30, 10), bd=(-30, -10), pe=(25, -10), pd=(-25, 10), cab=0, tronco=0),
    "ombros":   dict(be=(70, 100), bd=(-70, -100), pe=(12, 0), pd=(-12, 0), cab=10, tronco=0),
}


def carregar_fonte(tam):
    for f in ["C:/Windows/Fonts/arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ponto(o, ang, comp):
    r = math.radians(ang)
    return (o[0] + math.sin(r) * comp, o[1] + math.cos(r) * comp)


def boneco(d, x, y, h, pose, t, falando, cor, espessura, olhar=1, ant=None, k=1.0, fundo=None):
    """Desenha um boneco com pé em (x, y) e altura h. Interpola da pose anterior (ant) com peso k."""
    P = dict(POSE_ANG[pose])
    if ant and k < 1:
        A = POSE_ANG[ant]
        for chave in P:
            if isinstance(P[chave], tuple):
                P[chave] = tuple(a + (b - a) * k for a, b in zip(A[chave], P[chave]))
            else:
                P[chave] = A[chave] + (P[chave] - A[chave]) * k
    resp = math.sin(t * 2.2) * 0.012 * h            # respiração
    gest = math.sin(t * 5.0) * 6 if falando else 0  # gesticula ao falar
    if pose == "anda":
        passo = math.sin(t * 7) * 28
        P["pe"], P["pd"] = (passo, -abs(passo) / 2), (-passo, -abs(passo) / 2)
        P["be"], P["bd"] = (-passo * .8, 10), (passo * .8, -10)
    if pose == "comemora":
        y -= abs(math.sin(t * 6)) * h * 0.05
    perna, coxa = h * 0.22, h * 0.22
    torso, braco = h * 0.30, h * 0.18
    raio = h * 0.11
    quadril = (x, y - perna - coxa + resp)
    pesc = ponto(quadril, 180 + P["tronco"] * olhar, torso)
    for lado in ("pe", "pd"):
        a1, a2 = P[lado]
        j = ponto(quadril, a1 * olhar, coxa)
        p = ponto(j, (a1 + a2) * olhar, perna)
        d.line([quadril, j, p], fill=cor, width=espessura, joint="curve")
    ombro = ponto(quadril, 180 + P["tronco"] * olhar, torso * 0.88)
    for lado in ("be", "bd"):
        a1, a2 = P[lado]
        if lado == "be":
            a1 += gest
        c = ponto(ombro, a1 * olhar, braco)
        m = ponto(c, (a1 + a2) * olhar, braco)
        d.line([ombro, c, m], fill=cor, width=espessura, joint="curve")
    d.line([quadril, pesc], fill=cor, width=espessura)
    cab = ponto(pesc, 180 + (P["tronco"] + P["cab"]) * olhar, raio * 1.05)
    d.ellipse([cab[0] - raio, cab[1] - raio, cab[0] + raio, cab[1] + raio],
              fill=fundo, outline=cor, width=espessura)
    # olhos (piscam a cada ~3,5 s)
    piscando = (t % 3.5) < 0.12
    for dx in (-0.35, 0.35):
        ox, oy = cab[0] + (dx + 0.15 * olhar) * raio, cab[1] - 0.1 * raio
        if piscando:
            d.line([(ox - raio * .1, oy), (ox + raio * .1, oy)], fill=cor, width=max(2, espessura // 2))
        else:
            d.ellipse([ox - raio * .1, oy - raio * .12, ox + raio * .1, oy + raio * .12], fill=cor)
    # boca
    bx, by = cab[0] + 0.15 * olhar * raio, cab[1] + 0.42 * raio
    if pose == "triste":
        d.arc([bx - raio * .3, by, bx + raio * .3, by + raio * .35], 200, 340, fill=cor, width=espessura // 2)
    elif pose == "choque" or falando:
        ab = raio * (0.22 if pose == "choque" else 0.08 + 0.12 * abs(math.sin(t * 18)))
        d.ellipse([bx - raio * .18, by - ab / 2, bx + raio * .18, by + ab / 2], fill=cor)
    else:
        d.arc([bx - raio * .3, by - raio * .3, bx + raio * .3, by + raio * .05], 20, 160, fill=cor, width=espessura // 2)


def objeto(d, nome, cx, cy, s, cor, dest, t, fonte):
    """Ícones simples desenhados em código (sem imagens, sem direitos autorais)."""
    s *= 1 + 0.04 * math.sin(t * 3)
    w = max(3, int(s * 0.06))
    if nome == "dinheiro":
        for i in range(3):
            o = i * s * 0.12
            d.rounded_rectangle([cx - s * .6 + o, cy - s * .3 - o, cx + s * .6 + o, cy + s * .3 - o],
                                radius=s * .06, fill=(120, 200, 120), outline=cor, width=w)
        d.text((cx + s * .24, cy - s * .24), "$", font=fonte, fill=cor, anchor="mm")
    elif nome == "casa":
        d.polygon([(cx - s * .6, cy), (cx, cy - s * .55), (cx + s * .6, cy)], fill=dest, outline=cor)
        d.rectangle([cx - s * .45, cy, cx + s * .45, cy + s * .5], outline=cor, width=w)
        d.rectangle([cx - s * .1, cy + s * .2, cx + s * .1, cy + s * .5], fill=cor)
    elif nome == "pergunta":
        d.text((cx, cy), "?", font=fonte, fill=dest, anchor="mm", stroke_width=w, stroke_fill=cor)
    elif nome == "alerta":
        d.polygon([(cx, cy - s * .55), (cx + s * .6, cy + s * .45), (cx - s * .6, cy + s * .45)],
                  fill=(240, 70, 60), outline=cor)
        d.text((cx, cy + s * .08), "!", font=fonte, fill=(255, 255, 255), anchor="mm")
    elif nome == "ideia":
        brilho = 0.5 + 0.5 * math.sin(t * 6)
        for i in range(8):
            a = i * math.pi / 4
            r1, r2 = s * .55, s * (.7 + .1 * brilho)
            d.line([(cx + math.cos(a) * r1, cy - s * .1 + math.sin(a) * r1),
                    (cx + math.cos(a) * r2, cy - s * .1 + math.sin(a) * r2)], fill=dest, width=w)
        d.ellipse([cx - s * .4, cy - s * .5, cx + s * .4, cy + s * .3], fill=dest, outline=cor, width=w)
        d.rectangle([cx - s * .18, cy + s * .3, cx + s * .18, cy + s * .48], fill=cor)
    elif nome in ("grafico_sobe", "grafico_desce"):
        sobe = nome == "grafico_sobe"
        d.line([(cx - s * .6, cy - s * .5), (cx - s * .6, cy + s * .5), (cx + s * .6, cy + s * .5)], fill=cor, width=w)
        pts = [(-.5, .3), (-.2, .05), (.05, .2), (.45, -.4)] if sobe else [(-.5, -.4), (-.2, -.1), (.05, -.2), (.45, .35)]
        prog = ease(t / 1.5) * (len(pts) - 1)
        i = min(int(prog), len(pts) - 2)
        f = prog - i
        cam = [(cx + px * s, cy + py * s) for px, py in pts[:i + 1]]
        a, b = pts[i], pts[i + 1]
        cam.append((cx + (a[0] + (b[0] - a[0]) * f) * s, cy + (a[1] + (b[1] - a[1]) * f) * s))
        d.line(cam, fill=(60, 180, 90) if sobe else (230, 70, 60), width=w * 2, joint="curve")
    elif nome == "relogio":
        d.ellipse([cx - s * .5, cy - s * .5, cx + s * .5, cy + s * .5], fill=(255, 255, 255), outline=cor, width=w)
        a = t * 2
        d.line([(cx, cy), (cx + math.sin(a) * s * .38, cy - math.cos(a) * s * .38)], fill=cor, width=w)
        d.line([(cx, cy), (cx + math.sin(a / 12) * s * .25, cy - math.cos(a / 12) * s * .25)], fill=cor, width=w)
    elif nome == "celular":
        d.rounded_rectangle([cx - s * .3, cy - s * .55, cx + s * .3, cy + s * .55], radius=s * .08,
                            fill=(40, 40, 50), outline=cor, width=w)
        d.rectangle([cx - s * .24, cy - s * .45, cx + s * .24, cy + s * .42], fill=dest)
    elif nome == "coracao":
        b = 1 + 0.1 * abs(math.sin(t * 4))
        r = s * .28 * b
        d.ellipse([cx - 2 * r, cy - r * 1.2, cx, cy + r * .6], fill=(230, 60, 80))
        d.ellipse([cx, cy - r * 1.2, cx + 2 * r, cy + r * .6], fill=(230, 60, 80))
        d.polygon([(cx - 1.9 * r, cy), (cx + 1.9 * r, cy), (cx, cy + r * 2)], fill=(230, 60, 80))


def legenda(d, palavras, t, W, H, y, fonte, tema, max_pal=3):
    """Legenda estilo Shorts: 3 palavras por vez, a palavra falada em destaque."""
    if not palavras:
        return
    atual = 0
    for i, p in enumerate(palavras):
        if t >= p["a"]:
            atual = i
    g = atual // max_pal * max_pal
    grupo = palavras[g:g + max_pal]
    texto = [p["w"].upper() for p in grupo]
    esp = fonte.getlength(" ")
    larg = sum(fonte.getlength(w) for w in texto) + esp * (len(texto) - 1)
    x = (W - larg) / 2
    for i, w in enumerate(texto):
        cor = tema["destaque"] if g + i == atual else tema["texto"]
        d.text((x, y), w, font=fonte, fill=cor, anchor="lm", stroke_width=max(4, fonte.size // 10),
               stroke_fill=tema["contorno"])
        x += fonte.getlength(w) + esp


def quadro(cena, ant, t, W, H, SS, tema, fontes):
    img = Image.new("RGB", (W * SS, H * SS), tema["fundo"])
    d = ImageDraw.Draw(img)
    w, h = W * SS, H * SS
    vertical = H > W
    lt = t - cena["ini"]
    k = ease(lt / 0.35)  # transição de pose
    chao = h * (0.66 if vertical else 0.80)
    d.rectangle([0, chao, w, h], fill=tema["chao"])
    falando = any(p["a"] <= t <= p["b"] for p in cena["palavras"])
    alt = h * (0.34 if vertical else 0.58)
    esp = max(4, int(alt * 0.035))
    pose_ant = ant["pose"] if ant else None
    if cena["dois"]:
        boneco(d, w * .32, chao, alt, cena["pose"], t, falando, tema["linha"], esp, 1, pose_ant, k, tema["fundo"])
        boneco(d, w * .68, chao, alt * .95, "fala" if not falando else "pensa", t + 1.3, False,
               tema["linha"], esp, -1, fundo=tema["fundo"])
    else:
        bx = w * (0.5 if vertical else 0.33)
        if cena["pose"] == "anda":
            bx += (lt - 1) * w * 0.03
        boneco(d, bx, chao, alt, cena["pose"], t, falando, tema["linha"], esp, 1, pose_ant, k, tema["fundo"])
    pop = ease(lt / 0.25)  # objeto "pula" para dentro
    if cena["numero"]:
        f = fontes["numero"]
        txt = cena["numero"]
        while f.getlength(txt) > w * (0.9 if vertical else 0.55) and f.size > 20:
            f = carregar_fonte(int(f.size * 0.9))
        cx, cy = (w * .5, h * .28) if vertical else (w * .70, h * .42)
        d.text((cx, cy + (1 - pop) * 60 * SS), txt, font=f, fill=tema["destaque"], anchor="mm",
               stroke_width=max(6, f.size // 12), stroke_fill=tema["linha"])
    elif cena["objeto"] and not cena["dois"]:
        cx, cy = (w * .5, h * .22) if vertical else (w * .68, h * .42)
        objeto(d, cena["objeto"], cx, cy, h * (0.20 if vertical else 0.30) * (0.4 + 0.6 * pop),
               tema["linha"], tema["destaque"], lt, fontes["obj"])
    ly = h * (0.80 if vertical else 0.91)
    legenda(d, cena["palavras"], t, w, h, ly, fontes["leg"], tema)
    # zoom lento (sensação de câmera)
    z = 1 + 0.04 * ease(lt / max(0.5, cena["fim"] - cena["ini"]))
    if z > 1.001:
        cw, ch = w / z, h / z
        img = img.crop(((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2))
    img = img.resize((w, h), Image.BILINEAR) if z > 1.001 else img
    return img.reduce(SS) if SS > 1 else img


# ----------------------------------------------------------------------------- render

_CTX = None


def fontes_tam(W, SS, vertical):
    return (int(W * SS * (0.075 if vertical else 0.042)), int(W * SS * (0.16 if vertical else 0.10)),
            int(W * SS * (0.10 if vertical else 0.10)))


def _init(ctx):
    global _CTX, _FONTES
    _CTX = ctx
    leg, num, obj = ctx[6]
    _FONTES = {"leg": carregar_fonte(leg), "numero": carregar_fonte(num), "obj": carregar_fonte(obj)}


def _desenha(f):
    if "_FONTES" not in globals():
        _init(_CTX)
    cenas, fps, W, H, SS, tema, _ = _CTX
    t = f / fps
    ci = 0
    while ci + 1 < len(cenas) and t >= cenas[ci + 1]["ini"]:
        ci += 1
    return quadro(cenas[ci], cenas[ci - 1] if ci else None, t, W, H, SS, TEMAS[tema], _FONTES).tobytes()


def renderizar(cenas, audio, total, saida, args):
    W, H = (1080, 1920) if args.vertical else (1920, 1080)
    if args.rapido:
        W, H = W // 2, H // 2
    SS = 1 if args.rapido else 2
    fps = args.fps
    n = int(math.ceil(total * fps))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if audio:
        cmd += ["-i", audio]
    if args.musica:
        cmd += ["-stream_loop", "-1", "-i", args.musica]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p"]
    if audio and args.musica:
        cmd += ["-filter_complex", "[2:a]volume=0.12[m];[1:a][m]amix=inputs=2:duration=first[a]",
                "-map", "0:v", "-map", "[a]"]
    elif args.musica:
        cmd += ["-map", "0:v", "-map", "1:a"]
    if audio or args.musica:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-movflags", "+faststart", saida]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    global _CTX
    _CTX = (cenas, fps, W, H, SS, args.tema, fontes_tam(W, SS, args.vertical))
    procs = args.nucleos or max(1, (os.cpu_count() or 2) - 1)
    pool = mp.Pool(procs, initializer=_init, initargs=(_CTX,)) if procs > 1 else None
    it = pool.imap(_desenha, range(n), chunksize=8) if pool else map(_desenha, range(n))
    for f, dados in enumerate(it):
        ff.stdin.write(dados)
        if f % (fps * 5) == 0:
            print(f"\r• desenhando quadros {100 * f // n:3d}%  ({procs} núcleos)", end="", flush=True)
    if pool:
        pool.close()
    ff.stdin.close()
    ff.wait()
    print("\r• desenhando quadros 100%")
    if ff.returncode:
        sys.exit("ffmpeg falhou")


def thumbnail(cenas, total, saida, args):
    """Gera thumbnail a partir da cena com número/objeto mais forte."""
    W, H = 1280, 720
    alvo = next((c for c in cenas if c["numero"]), None) or next((c for c in cenas if c["objeto"]), cenas[0])
    tema = TEMAS[args.tema]
    fontes = {"leg": carregar_fonte(int(W * 2 * 0.06)), "numero": carregar_fonte(int(W * 2 * 0.12)),
              "obj": carregar_fonte(int(H * 2 * 0.18))}
    img = quadro(alvo, None, alvo["ini"] + 1.0, W, H, 2, tema, fontes)
    img.save(saida, quality=92)


def main():
    ap = argparse.ArgumentParser(description="Vídeo de boneco-palito a custo zero.")
    ap.add_argument("roteiro")
    ap.add_argument("-o", "--saida", default=None)
    ap.add_argument("--voz", choices=["edge", "piper"], default="edge")
    ap.add_argument("--voz-nome", default="pt-BR-AntonioNeural",
                    help="voz Edge (ex.: pt-BR-FranciscaNeural, en-US-GuyNeural, es-MX-JorgeNeural)")
    ap.add_argument("--velocidade", default="+8%", help="velocidade da voz Edge, ex.: +10%%")
    ap.add_argument("--modelo", help="arquivo .onnx da voz Piper")
    ap.add_argument("--audio", help="usar uma narração pronta (mp3/wav)")
    ap.add_argument("--sem-voz", action="store_true", help="vídeo mudo, só para testar")
    ap.add_argument("--musica", help="trilha de fundo (use músicas da Biblioteca de Áudio do YouTube)")
    ap.add_argument("--idioma", default="pt")
    ap.add_argument("--whisper", default="base", help="tiny/base/small (maior = mais preciso, mais lento)")
    ap.add_argument("--vertical", action="store_true", help="9:16 para Shorts/Reels/TikTok")
    ap.add_argument("--tema", choices=list(TEMAS), default="claro")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--nucleos", type=int, default=0, help="processos em paralelo (padrão: todos menos 1)")
    ap.add_argument("--rapido", action="store_true", help="prévia em meia resolução, bem mais rápida")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("Instale o ffmpeg (grátis): https://ffmpeg.org")
    cenas = ler_roteiro(args.roteiro)
    base = os.path.splitext(args.saida or args.roteiro)[0]
    saida = base + ".mp4"
    tmp = tempfile.mkdtemp(prefix="stickvid_")
    texto = " ".join(c["texto"] for c in cenas)

    audio, palavras = None, None
    if args.audio:
        audio = args.audio
    elif not args.sem_voz:
        print(f"• gerando narração grátis ({args.voz})…")
        audio = gerar_voz(texto, os.path.join(tmp, "voz.mp3"), args)
    if audio:
        total = duracao_audio(audio) + 0.4
        palavras = tempos_whisper(audio, args.idioma, args.whisper)
    else:
        total = sum(len(c["texto"].split()) for c in cenas) / 2.7 + 0.5
    cenas = distribuir(cenas, palavras, total)
    json.dump(cenas, open(base + ".cenas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"• {len(cenas)} cenas, {total:.1f}s")
    renderizar(cenas, audio, total, saida, args)
    thumbnail(cenas, total, base + ".thumb.jpg", args)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"✔ pronto: {saida}\n✔ thumbnail: {base}.thumb.jpg")


if __name__ == "__main__":
    main()
