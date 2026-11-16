#!/usr/bin/env python3
"""Alinhamento local texto<->audio sem modelos: usa as pausas (silencedetect)
para ancorar o fim de cada frase e distribui as palavras de cada frase
proporcionalmente ao numero de caracteres. Gera words/sNN.json no mesmo
formato do ElevenLabs Scribe ({"words":[{"text","type","start","end"}]})."""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def silences(path, noise='-34dB', d=0.22):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', f'silencedetect=noise={noise}:d={d}', '-f', 'null', '-'],
                       capture_output=True, text=True)
    st, out = None, []
    for line in r.stderr.splitlines():
        m = re.search(r'silence_start: ([\d.]+)', line)
        if m:
            st = float(m.group(1))
        m = re.search(r'silence_end: ([\d.]+)', line)
        if m and st is not None:
            out.append((st, float(m.group(1))))
            st = None
    return out


def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))


def align(text, audio):
    text = re.sub(r'\[[^\]]+\]\s*', '', text)
    words = text.split()
    D = dur(audio)
    sil = silences(audio)
    lead = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] > D - 0.05 else D
    gaps = [s for s in sil if s[0] > lead + 0.05 and s[1] < tail - 0.05]
    # fronteiras candidatas = fim de palavra com pontuacao
    cum, tot = [], 0
    for w in words:
        tot += len(w) + 1
        cum.append(tot)
    punct = [i for i, w in enumerate(words) if re.search(r'[.,;:!?…]$|\.\.\.$', w)]
    # mapeia cada pausa para a fronteira de pontuacao mais proxima (em proporcao)
    speech = tail - lead
    anchors = {}  # indice da palavra -> (fim_fala, inicio_proxima)
    used = set()
    for gs, ge in gaps:
        frac_t = (gs - lead) / speech
        best, bd = None, 1e9
        for i in punct:
            if i in used or i == len(words) - 1:
                continue
            d_ = abs(cum[i] / tot - frac_t)
            if d_ < bd:
                best, bd = i, d_
        if best is not None and bd < 0.08:
            anchors[best] = (gs, ge)
            used.add(best)
    # monta blocos entre ancoras
    keys = sorted(anchors)
    blocks, start_w, t0 = [], 0, lead
    for k in keys:
        blocks.append((start_w, k, t0, anchors[k][0]))
        start_w, t0 = k + 1, anchors[k][1]
    blocks.append((start_w, len(words) - 1, t0, tail))
    out = []
    for a, b, ta, tb in blocks:
        if b < a:
            continue
        ws = words[a:b + 1]
        lens = [len(w) + 1.5 for w in ws]
        L = sum(lens)
        t = ta
        for w, l in zip(ws, lens):
            dt = (tb - ta) * l / L
            out.append({'text': w, 'type': 'word', 'start': round(t, 3), 'end': round(t + dt * 0.92, 3)})
            t += dt
    return out


if __name__ == '__main__':
    d = json.load(open(os.path.join(ROOT, 'roteiro.json')))
    os.makedirs(os.path.join(ROOT, 'words'), exist_ok=True)
    for s in d['segments']:
        a = os.path.join(ROOT, 'audio', s['id'] + '.mp3')
        w = align(s['text'], a)
        json.dump({'words': w}, open(os.path.join(ROOT, 'words', s['id'] + '.json'), 'w'))
        print(s['id'], len(w), 'palavras', w[-1]['end'] if w else 0)
