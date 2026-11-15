# HANDOFF — Fábrica de documentários (continuar no PC local)

> Para o Claude Code rodando no PC (RTX 5090) ou no Mac M4: leia este arquivo inteiro antes de qualquer coisa.
> Ele resume a sessão na nuvem de 15/11/2026 em que planejamos a operação e produzimos a primeira amostra.

## 1. Objetivo do dono do projeto
- Operação de **canais faceless de documentário** no YouTube (e depois no Facebook), **em inglês** (RPM maior). Um canal por nicho:
  1. **Crimes e mistérios** (começar por este)
  2. História
  3. Dinheiro e negócios
- Vídeos de **15–30 min**, muito bem produzidos e **autênticos** (cada vídeo diferente; nada de template repetido).
- Meta imediata: **5 vídeos de teste** (15–30 min) no canal de crimes/mistérios, medir o desempenho e só então escalar (objetivo de longo prazo: até 2 vídeos/dia).
- **Custo-alvo: R$5–10 por vídeo** agora; idealmente perto de R$0 rodando tudo localmente na 5090.
- O dono quer **automação máxima** e entregas prontas. Ele pode deixar o PC e o Mac ligados 24h.
- **Cuidado com direitos autorais** é prioridade explícita do dono.

## 2. O que já existe neste repositório
- `dbcooper-amostra/` — amostra de 3min11s em **PT-BR** sobre o caso D.B. Cooper (aprovação de estilo pendente).
  - `roteiro.json` — roteiro em 8 segmentos.
  - `audio/` — narração ElevenLabs (voz "Nassif - Documentary, History & Thriller", modelo eleven_v4), música, SFX.
  - `img/` — 27 stills gerados (GPT-Image via ElevenLabs). `vid/` (ignorado no git) tinha 5 clipes Kling.
  - `words/` — timestamps por palavra (ElevenLabs Scribe) usados para sincronizar cortes e legendas.
  - `scripts/render.py` — **motor de montagem** (Python + PIL + ffmpeg): planos ancorados em palavras da narração,
    Ken Burns subpixel, mapas animados (Natural Earth), overlays (máquina de escrever, título, carimbo, contadores,
    bilhete), letterbox, grão, vinheta, xfade, legendas ASS, mixagem com ducking (sidechain) e loudnorm.
    Rodar: `python3 scripts/render.py` (precisa de `vid/*.mp4` e `assets/land.geojson`, ver abaixo).
  - `assets/` — fontes OFL/Apache (Bebas Neue, Oswald, Special Elite, Caveat, Inter) e `states.geojson`.
    `land.geojson` foi ignorado no git: baixe de
    `https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson`.
- `docs/pesquisa/` — relatórios completos dos agentes de pesquisa (ver seção 5).

### Custos medidos na amostra (ElevenLabs Pro)
| Item | Créditos | US$ |
|---|---|---|
| Narração 3 min (1 take por trecho) | ~2.450 | ~0,40 |
| Imagem (gpt-image-2.5) | ~190 cada | ~0,03 |
| Clipe vídeo Kling 2.5 turbo 5 s | ~2.121 | ~0,35 |
| Música 3 min | ~900 | ~0,15 |
| **Total amostra 3 min** | **~20.000** | **~3,30** |
Projeção vídeo de 30 min 100% ElevenLabs: ~US$12–19. **Por isso a migração para stack local.**
Regra do dono: **sempre gerar só 1 take** (generations_count=1) quando usar ElevenLabs.

## 3. Decisões e regras (não violar)
- Narrativa: investigação e enigma, **sem gore**. Mistura: 1/3 golpes/roubos, 1/3 mistérios sem solução, 1/3 crimes históricos.
- Quem não foi condenado = "suspeito/acusado". Toda afirmação com fonte registrada (planilha de fontes por vídeo).
- **Nunca** gerar imagem realista de vítima ou suspeito real. Pessoas reais só com foto de arquivo de domínio público.
- Marcar **"conteúdo alterado/sintético"** no upload quando houver cena realista gerada por IA.
- Proibido: trechos de filmes, telejornais, documentários ou vídeos de terceiros; música comercial.
- Política do YouTube "inauthentic content" (jul/2025): variar estrutura, visual e ritmo entre vídeos; roteiro com revisão humana.
- Guardar prova de licença/origem de cada asset (URL, ID, data, print da licença).

## 4. Stack local recomendada (verificar licenças no Hugging Face antes de usar — foi impossível acessar HF da nuvem)
| Etapa | Escolha principal | Licença (a confirmar) | Evitar (não comercial) |
|---|---|---|---|
| Voz | **VoxCPM2**, **Qwen3-TTS 1.7B**; IndexTTS-2.5 (só EN) | Apache-2.0 / bilibili | F5-TTS, XTTS-v2, Spark-TTS, Higgs v3, Fish S2-Pro, VibeVoice |
| Imagens | **Z-Image-Turbo** (volume), **Qwen-Image-2512**, **Qwen-Image-Edit-2511**; upscale SeedVR2 | Apache/MIT | FLUX.1/2 dev, Kontext dev, Qwen-Image-2.1, PuLID/InstantID (InsightFace) |
| Vídeo IA | **Wan 2.2** I2V/T2V 14B + LoRA LightX2V 4 passos; LongCat-Video (MIT) | Apache-2.0 | Hunyuan/FramePack/SkyReels V1 (exclui UE/UK), MiniMax H3 |
| Movimento grátis | Parallax 2.5D: Depth-Anything-V2 **Small** (Apache) + OpenCV | Apache | DA-V2 Base/Large (CC-BY-NC) |
| Música | **ACE-Step 1.5**, DiffRhythm, HeartMuLa | MIT/Apache | MusicGen, MAGNeT, JASCO |
| SFX | Stable Audio 3 (< US$1M receita), `wyzowl/sfx-kit` (CC0), síntese ffmpeg | — | MMAudio, AudioLDM2, Tango, BBC SFX |
| Legendas/alinhamento | **stable-ts** `model.align(audio, texto)` / WhisperX | MIT / BSD-2 | aeneas (AGPL) |
| Orquestração | Python + Prefect; ComfyUI só como serviço via API; ComfyUI com PyTorch cu128/cu130 (5090 = sm_120) | — | — |
| B-roll/arquivo | Pexels/Pixabay API (chaves do dono), Internet Archive, NARA, LoC, NASA, FBI Vault | — | British Pathé (pago), FMA CC-BY-NC |
| Música de terceiros | YouTube Audio Library ("attribution not required") | — | Pixabay Music (risco Content ID) |

Throughput estimado (não medido) na 5090: imagens ~1.400+/h (Z-Image-Turbo NVFP4); clipes Wan 720p ~16–24/h;
vídeo de 20 min completo ~45–80 min de GPU → 8–12 vídeos/dia. Limite real: cota da YouTube Data API
(~6 uploads/dia por projeto; pedir auditoria no dia 1 para agendar com `publishAt`) e estratégia de 1–2 vídeos/dia/canal.

## 5. Relatórios em `docs/pesquisa/`
- `local_tts.md`, `local_image.md`, `local_video.md`, `local_audio.md`, `local_farm.md` (arquitetura, pastas, checklist de 26 passos)
- `pesquisa_youtube_canais.md` (40 canais de referência), `pesquisa_canais_ia.md`, `pesquisa_facebook.md`
- `pesquisa_temas.md` (estruturas de retenção + backlog de 50 ideias; D.B. Cooper faz 55 anos em 24/11)
Os relatórios marcam o que foi verificado vs. não verificado. Quase nada pôde ser testado na nuvem (rede bloqueada).

## 6. Próximos passos (em ordem)
1. Preparar o PC: driver NVIDIA recente, WSL2 (recomendado) ou Windows nativo, Python 3.11+, git, ffmpeg, PyTorch cu128+.
2. Instalar ComfyUI e testar **um** modelo de cada etapa (voz, imagem, vídeo, música); confirmar licenças no HF.
3. **Teste cego de voz**: regenerar os 3 min do D.B. Cooper com VoxCPM2, Qwen3-TTS e Chatterbox-PT e comparar com o ElevenLabs.
4. Adaptar `scripts/render.py` para: parallax 2.5D, efeitos (chuva/poeira), música local, alinhamento com stable-ts, render paralelo por cena + concat (o xfade em série levou 17 min no container de 4 CPUs; usar NVENC na 5090).
5. Pedir ao dono o OK do estilo da amostra e produzir os **5 vídeos de teste em inglês** (15–30 min), escolhendo do backlog.
6. Thumbnails (template PIL), títulos/descrições, upload como "não listado" para checar Content ID antes de publicar.
