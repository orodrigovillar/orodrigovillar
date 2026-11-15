# Vídeos faceless de boneco-palito a custo zero (método Grow With Kaz, mais rápido)

## 1. O que o Grow With Kaz faz

Não consegui assistir aos vídeos: o YouTube está bloqueado na rede deste ambiente.
O que está abaixo vem de fontes secundárias: resumos dos vídeos dele, o repositório
`j0p3s/2d-studio-videos-youtube` (feito para replicar o tutorial dele) e a busca.

- **Canal:** cerca de 112–114 mil inscritos. Ensina YouTube automation, ou seja, canais
  "faceless" (sem mostrar o rosto) para gerar renda passiva.
- **Tese de nicho:** um personagem fixo e reconhecível (boneco-palito 2D) em nicho de RPM
  alto: finanças, investimentos, psicologia, histórias, curiosidades e "histórias do Reddit"
  animadas. Vídeos recentes: *"New VIRAL niche on YouTube 2026 | High RPM"*, *"The Most
  Profitable Niche Nobody's Found"* e *"Make Videos With Claude Code / Free Plugin"*.
- **Fluxo dele (versão Claude Code):**
  1. Um prompt de nicho em PDF ("2D Niche Prompt") gera 10 ideias, o roteiro, o título e a descrição.
  2. Narração: Piper (offline), Edge TTS ou voz paga.
  3. Whisper extrai o tempo de cada palavra.
  4. O Claude Code, com o plugin dele (`GrowKaz_Stickman.plugin`, que é three.js + Playwright),
     escreve uma cena em código para cada trecho do roteiro.
  5. O FFmpeg monta o MP4. Depois vêm a thumbnail e o upload.
- **Onde ele gasta:** a assinatura do Claude Code (ou Codex/Gemini), que é o agente que
  escreve cada cena, e às vezes créditos de IA de imagem/vídeo (OpenArt, Kling, nano-banana).
  Ele também usa ChatGPT, Canva e Dubdub nas versões mais antigas do fluxo.

**O gargalo do método dele:** uma IA escreve código novo a cada cena, cena por cena, com
"rodadas de reparo" quando algo quebra. Isso é lento, gasta assinatura e falha às vezes.

## 2. O jeito mais rápido e mais fácil (o que está nesta pasta)

`stickvid.py` faz a mesma coisa **sem IA pagando por cena**. O boneco, as poses, os
objetos, as legendas e a câmera já estão prontos em código. Você só escreve o roteiro.

| | Grow With Kaz | stickvid |
|---|---|---|
| Comandos | instalar o plugin, abrir o Claude Code, pedir cena por cena | **1 comando** |
| Custo por vídeo | assinatura de IA + créditos opcionais | **R$ 0** |
| Falhas de cena | o agente refaz até 3 vezes | não existem (nada é gerado na hora) |
| Internet | obrigatória para o agente | opcional (Piper é 100% offline) |
| Formatos | 16:9 / Shorts | 16:9, 9:16, tema claro ou escuro |

### Instalação (uma vez só, tudo grátis)

```bash
# 1. Python 3.9+ e ffmpeg  (Windows: winget install Python.Python.3.12 Gyan.FFmpeg)
pip install pillow edge-tts faster-whisper
```

### Uso

```bash
python stickvid.py exemplo-roteiro.txt                  # vídeo 16:9 com voz grátis (Edge)
python stickvid.py exemplo-roteiro.txt --vertical       # Shorts / Reels / TikTok
python stickvid.py exemplo-roteiro.txt --tema escuro    # estilo fundo preto
python stickvid.py exemplo-roteiro.txt --rapido         # prévia rápida, meia resolução
python stickvid.py roteiro.txt --audio minha_voz.mp3    # sua própria narração
python stickvid.py roteiro.txt --musica trilha.mp3      # trilha de fundo baixinha
python stickvid.py roteiro.txt --voz-nome en-US-GuyNeural --idioma en   # canal em inglês (RPM maior)
```

Saída: `roteiro.mp4`, `roteiro.thumb.jpg` (thumbnail) e `roteiro.cenas.json` (tempos de cada cena).

### Formato do roteiro

Uma linha é uma cena. A tag é opcional: sem tag, o script escolhe a pose e o objeto pelo
sentido da frase (por exemplo, "dinheiro" mostra notas e "?" faz o boneco pensar).

```
[fala] Você sabia que existe dinheiro esquecido no seu nome?
[numero:R$ 8 bilhões] É isso que os brasileiros ainda não sacaram.
[triste|grafico_desce] Porque cada real esquecido é lucro parado.
[dois:fala] Eu mostrei para um amigo e ele achou mais de mil reais.
```

- **Poses:** fala, aponta, pensa, comemora, triste, choque, anda, ombros
- **Objetos:** dinheiro, casa, pergunta, ideia, grafico_sobe, grafico_desce, relogio, celular, alerta, coracao
- **Especiais:** `[numero:TEXTO]` mostra um número ou frase gigante; `[dois:pose]` coloca dois personagens

### Voz 100% offline (Piper)

```bash
pip install piper-tts
# baixe pt_BR-faber-medium.onnx + .onnx.json em huggingface.co/rhasspy/piper-voices
python stickvid.py roteiro.txt --voz piper --modelo pt_BR-faber-medium.onnx
```

## 3. Rotina para publicar todo dia (cerca de 15 min por vídeo)

1. **Roteiro (5 min):** cole no ChatGPT ou Claude grátis:
   > Escreva um roteiro de 60–90 s para YouTube sobre [TEMA], nicho [finanças/psicologia/curiosidades].
   > Uma frase curta por linha. Gancho forte na 1ª linha, um número chocante no meio, CTA no fim.
   > No começo de cada linha coloque uma tag entre colchetes com uma destas poses: fala, aponta,
   > pensa, comemora, triste, choque, anda, ombros. Opcionalmente, junte com | um destes objetos:
   > dinheiro, casa, pergunta, ideia, grafico_sobe, grafico_desce, relogio, celular, alerta, coracao.
   > Use [numero:VALOR] para números grandes.
2. **Vídeo (1 comando):** `python stickvid.py roteiro.txt --vertical`, deixe rodando.
3. **Upload grátis:** pelo YouTube Studio (use a thumbnail gerada). Para trilha sonora, use a
   Biblioteca de Áudio do YouTube, que é grátis e não dá direitos autorais.
4. **Escala:** faça 1 Short por dia e 1 vídeo longo por semana. Repita os formatos que passam
   da média de visualizações do canal.

## 4. Cuidados

- **Monetização:** o YouTube desmonetiza "conteúdo repetitivo/produzido em massa". Varie
  roteiros, temas e poses, e sempre traga informação real e checada.
- **Licenças:** este script e as vozes Edge/Piper são livres para uso. A voz grátis do
  ElevenLabs **não** tem licença comercial.
- **Desempenho:** um vídeo de 1 min em 1080p leva cerca de 2 min num PC de 4 núcleos e menos
  com mais núcleos. Use `--rapido` para revisar antes de gerar a versão final.
