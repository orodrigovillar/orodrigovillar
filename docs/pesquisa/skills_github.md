# Projetos open-source e skills do Claude Code para acelerar o pipeline documental (EN/PT-BR/ES)

**Data da pesquisa:** 16/11/2026
**Método:** busca na API do GitHub (`search/repositories`). READMEs e LICENSEs lidos via raw.githubusercontent.com. Estrelas e "última atualização" (último push) vêm da API no dia da pesquisa. Nada foi instalado.
**Limites:** o huggingface.co está bloqueado neste ambiente. Quando uma licença de pesos só existe no model card do HF, ela aparece como **[confirmar no HF]**.

**Legenda de licença**
- ✅ uso comercial liberado (MIT, BSD, Apache, CC0)
- 🟡 comercial permitido com condição (AGPL, CC-BY com atribuição, licença por faturamento, Remotion)
- ⛔ **NÃO comercial** (CC-BY-NC, NC-SA): não use num canal monetizado
- ❓ sem licença ou licença ambígua. Juridicamente, repositório sem licença = "todos os direitos reservados"

**Contexto do nosso pipeline**, levado em conta nas recomendações:
- `koepcke/scripts/alinhar.py` alinha texto e áudio **por heurística** (silencedetect + proporção de caracteres) e grava JSON no formato do ElevenLabs Scribe.
- `dbcooper-amostra/scripts/render.py` já gera legendas `.ass` e mixa SFX no ffmpeg.
- O conteúdo é faceless: imagens de IA, clipes Kling e narração. **Não há rosto para rastrear.**

---

## 1. Top 20 (ranking geral por impacto no nosso pipeline)

| # | Repo | ⭐ | Últ. push | Licença | O que faz por nós | Como encaixar |
|---|---|---|---|---|---|---|
| 1 | [jianfch/stable-ts](https://github.com/jianfch/stable-ts) | 2.282 | 30/05/2026 | ✅ MIT (pesos Whisper: MIT) | **Alinhamento forçado com o texto conhecido** (`model.align(audio, texto, language)`). Dá timestamps por palavra estáveis em CPU, para EN/PT/ES. | Substituir a heurística do `alinhar.py`: entra o `sNN.mp3` mais o roteiro, sai o mesmo JSON `{"words":[...]}`. Ganho direto de sincronia nas legendas e nos cortes. |
| 2 | [m-bain/whisperX](https://github.com/m-bain/whisperX) | 25.353 | 12/11/2026 | ✅ BSD-2 (código). ⚠️ Modelos de alinhamento variam por idioma (ver §6) | ASR com palavra por palavra via wav2vec2. Roda em CPU com `--compute_type int8`. | Plano B ao stable-ts e para transcrever material que não tem roteiro. **Em ES, troque o modelo padrão** (ver §6). |
| 3 | [BrokenSource/DepthFlow](https://github.com/BrokenSource/DepthFlow) | 1.590 | 13/11/2026 | 🟡 AGPL-3.0. O README diz "Commercial use is encouraged" | Imagem → vídeo com **parallax 3D real** (shader GLSL de ray marching), loops sem emenda, até 8K. Script em lote. | Para cada imagem do ElevenLabs: gerar um clipe parallax de 5–8 s e usar no lugar do zoompan. Dá para fazer em massa na 5090. Os vídeos renderizados não ficam sob AGPL. A AGPL só pesa se vocês modificarem o código e o oferecerem como serviço. |
| 4 | [DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | 9.158 | 24/03/2026 | ✅ Apache só no **Small**. ⛔ **Base/Large/Giant são CC-BY-NC-4.0** | Mapa de profundidade monocular. É a base de qualquer 2.5D. | Use **apenas o V2-Small** (ou DA3-Small/Base/Mono-Large, ver §5) para gerar o depth, e depois o DepthFlow ou nosso próprio parallax em numpy. |
| 5 | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | 6.046 | 16/11/2026 | ✅ MIT | Skill + servidor MCP com 42 ferramentas FFmpeg com contrato JSON: probe, cut, caption, export com presets `shorts`/`reels`/`youtube`, normalização de loudness, verificação. Sem nuvem e sem dependências Python. | Instalar como skill do Claude Code. Ela vira a camada "export + QA" depois do nosso render: loudness por plataforma e presets 9:16. |
| 6 | [francozanardi/pycaps](https://github.com/francozanardi/pycaps) | 233 | 30/09/2026 | ✅ MIT | **Legendas animadas por palavra estilizadas em CSS** (`.word-being-narrated`), com templates, tagging de palavras-chave por regex/lista/IA e animações pop/slide/typewriter. | Gerar a versão Shorts com legenda "estilo Hormozi/MrBeast" sem escrever ASS na mão. Ainda está em alpha (instala do GitHub). O renderer CSS usa Playwright; o `PictexSubtitleRenderer` dispensa navegador. |
| 7 | [danielgatis/rembg](https://github.com/danielgatis/rembg) | 25.506 | 06/11/2026 | ✅ MIT. Modelos u2net/isnet/birefnet ok. ⛔ **não use o modelo `bria-rmbg`** (CC-BY-NC) | Recorte de fundo em CPU (onnxruntime), via CLI ou biblioteca. | Thumbnails: recortar o personagem ou objeto da imagem de IA e compor com PIL sobre o fundo e o texto. Use `-m birefnet-general` ou `birefnet-portrait`. |
| 8 | [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) | 6.061 | 16/09/2026 | ✅ MIT | 11 skills: roteiro com 21 fórmulas de gancho e nota para o gancho, **lint de título + thumbnail como par**, leitura do export de retenção ("o segundo em que saíram"), EDL a partir de transcrição, "Shorts escondidos no vídeo longo", outliers do nicho. Sem API key. | `cp -r skills/yt-* ~/.claude/skills/`. Usar no pré-publicação (título/thumb) e no pós (retenção). |
| 9 | [sanskarprajapati/parallax-doc](https://github.com/sanskarprajapati/parallax-doc) | 8 | 2026 | ✅ MIT. O renderizador **HyperFrames (HeyGen) tem licença não verificada** ❓ | Plugin do Claude Code para **documentário histórico em plano-sequência**: 3–5 camadas com parallax, texto datilografado com uma palavra vermelha, look de filme gasto. Aceita narração ElevenLabs. | Poucas estrelas, mas é exatamente o nosso nicho. Vale como **referência de estilo e de receitas** (camadas, grain, transições sem corte), para portar para o nosso renderer PIL/ffmpeg. |
| 10 | [AgriciDaniel/claude-shorts](https://github.com/AgriciDaniel/claude-shorts) | 401 | 11/07/2026 | ✅ MIT. 🟡 depende do **Remotion** (ver nota) | Skill de long → short: faster-whisper com palavra por palavra, classificação de conteúdo, legendas animadas renderizadas em Remotion, NVENC. | Referência de fluxo de corte para Shorts orientado pelo Claude. Para nós, o melhor é **re-renderizar em 9:16 a partir dos assets** (ver §2). |
| 11 | [hassancs91/claude-faceless-shorts-creator](https://github.com/hassancs91/claude-faceless-shorts-creator) | 366 | 18/08/2026 | ✅ MIT. 🟡 Remotion | Fábrica de Shorts faceless no Claude Code: voz ElevenLabs com **legendas sincronizadas palavra a palavra**, QA quadro a quadro em escala de celular, biblioteca de SFX/música que cresce sozinha, loops com frame 0 = último frame, trilha "vox collage". | É o stack mais parecido com o nosso. Copiar ideias: o QA em escala de celular, a cue sheet de SFX por beat e a "gramática de 6 beats". |
| 12 | [wyzowl/sfx-kit](https://github.com/wyzowl/sfx-kit) | 41 | 20/10/2026 | ✅ CC0 | 320 SFX originais (whooshes, risers, impacts, UI…) com metadados de **ponto de sincronia, duração e nível**, feitos para agentes. | Baixar uma vez para `assets/sfx/`. O `render.py` usa o sync point para posicionar o som no corte. |
| 13 | [Anil-matcha/AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) | 6.116 | 12/11/2026 | ✅ MIT | Alternativa ao Opus Clip: o LLM detecta destaques, Whisper transcreve, recorte 9:16 e legendas. O modo `api` usa MuAPI (pago). O **modo `--mode local`** usa yt-dlp + faster-whisper + ffmpeg/OpenCV e só o LLM é remoto. | Para cortar material de **terceiros/entrevistas** ou vídeos já publicados. Use o modo local com Claude/OpenAI-compatível. |
| 14 | [MontrealCorpusTools/Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) | 1.917 | 15/11/2026 | ✅ MIT (código). 🟡 modelos [mfa-models](https://github.com/MontrealCorpusTools/mfa-models) **CC-BY-4.0** (comercial com atribuição) | Alinhador Kaldi clássico, muito preciso, em CPU, com modelos para EN/PT/ES. Alinha até fonemas. | Opção "padrão ouro" se o stable-ts errar em nomes próprios. Instalação via conda é mais pesada. |
| 15 | [localai-org/depth-anything.cpp](https://github.com/localai-org/depth-anything.cpp) | 1.137 | 07/09/2026 | ✅ MIT (código). Pesos herdam a licença original (use Small/Base) | Port C++/ggml do Depth Anything 2/3. **Mais rápido que PyTorch em CPU**, sem dependências. | Gerar depth no **Mac M4 ou em CPU** sem instalar torch. |
| 16 | [OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage) | 80.771 | 09/11/2026 | 🟡 AGPL-3.0 | "Sistema agentic de produção de vídeo": 12 pipelines, mais de 100 ferramentas, mais de 700 skills. Funciona sem API keys no modo básico. | Grande demais para adotar inteiro. Use como **biblioteca de receitas e skills** para garimpar e ler. Usar como ferramenta é ok; distribuir uma versão modificada como serviço aciona a AGPL. |
| 17 | [adityaarsharma/youtube-marketing-skills](https://github.com/adityaarsharma/youtube-marketing-skills) | 85 | 10/10/2026 | ✅ MIT | 21 comandos + **MCP ligado ao canal real**: lê analytics privados e **escreve SEO de volta no YouTube** (título, descrição, tags). | SEO multilíngue (EN/PT/ES) por vídeo. Exige projeto no Google Cloud (OAuth). Avaliar se não conflita com o Postiz. |
| 18 | [ace-step/ACE-Step-1.5](https://github.com/ace-step/ACE-Step-1.5) | 14.833 | 08/11/2026 | ✅ MIT (repo). Pesos [confirmar no HF] | Música local com qualidade "entre Suno v4.5 e v5", instrumental e de longa duração. Já analisado em `local_audio.md`. | Trilhas sob medida na 5090, como substituto do ElevenLabs Music. |
| 19 | [skyzhao1223/free-for-creators](https://github.com/skyzhao1223/free-for-creators) | 84 | 11/11/2026 | ✅ CC0 (a lista) | Diretório de 220 recursos (música, SFX, footage, fontes, LUTs) com colunas **Licença / Atribuição / Monetização** verificadas e checagem semanal de links. | Fonte de consulta para escolher bibliotecas "seguras para conteúdo monetizado". |
| 20 | [ZhengPeng7/BiRefNet](https://github.com/ZhengPeng7/BiRefNet) | 4.410 | 25/10/2026 | ✅ MIT (código e pesos oficiais) | Segmentação de alta resolução, o melhor recorte livre. Tem ONNX. | O rembg já empacota o BiRefNet. Use direto só se precisar de matting em 4K para thumbnails. ⛔ O fork treinado pela Bria (RMBG-2.0) é NC. |

> **Nota sobre o Remotion** (afeta claude-shorts, faceless-shorts-creator, remotion-superpowers, template-tiktok e claude-remotion-skill): o Remotion tem licença própria. É grátis para pessoa física e empresas pequenas, mas **exige company license** acima do limite de funcionários definido em `remotion.dev/license` (não confirmei o número exato porque o LICENSE.md não foi lido por inteiro). Como nosso renderer é PIL + ffmpeg, prefira portar as ideias em vez de adotar o Remotion.

---

## 2. Cortes automáticos para Shorts/Reels (destaques, reenquadramento 9:16, legendas)

**Recomendação de arquitetura:** os vídeos são nossos e temos todos os assets (imagens, clipes Kling, narração por cena e timestamps por palavra). Por isso, o melhor Short **não é recortar o 16:9**:
1. O Claude lê o roteiro e os timestamps e escolhe de 2 a 4 trechos de 30–55 s com gancho forte. A detecção de destaque vira um prompt, não um modelo.
2. O nosso `render.py` **re-renderiza** o trecho em 1080×1920, com as imagens recompostas em vertical (ou parallax vertical via DepthFlow) e a legenda grande.
3. As ferramentas abaixo servem para material de terceiros ou para quando não houver tempo de re-renderizar.

| Repo | ⭐ | Últ. push | Licença | Comentário |
|---|---|---|---|---|
| [Anil-matcha/AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) | 6.116 | 12/11/2026 | ✅ MIT | O mais maduro. Use `--mode local` (o padrão usa MuAPI, que é pago). |
| [modelscope/FunClip](https://github.com/modelscope/FunClip) | 6.562 | 01/11/2026 | ✅ MIT | Corte guiado por LLM sobre a transcrição (FunASR/Paraformer). Forte em chinês, fraco para PT/ES. |
| [JayWebtech/autoshorts](https://github.com/JayWebtech/autoshorts) | 1.545 | 13/11/2026 | ❓ **sem licença** | App desktop local-first. Sem licença = não usar comercialmente. |
| [jipraks/yt-short-clipper](https://github.com/jipraks/yt-short-clipper) | 1.085 | 20/09/2026 | ✅ MIT | App Windows com detecção de destaque, MediaPipe e LLM OpenAI-compatível. |
| [ClipsAI/clipsai](https://github.com/ClipsAI/clipsai) | 572 | 17/01/2024 | ✅ MIT | Biblioteca Python (TextTiling + WhisperX). O resize usa pyannote, que precisa de token HF. **Parada desde 2024.** |
| [kamilstanuch/Autocrop-vertical](https://github.com/kamilstanuch/Autocrop-vertical) | 463 | 15/02/2026 | ❓ **sem licença**. ⚠️ YOLOv8 (Ultralytics) é **AGPL-3.0** | Crop por cena com YOLO, letterbox quando não há pessoa. Serve só como referência. |
| [mutonby/shortcast](https://github.com/mutonby/shortcast) | 401 | 04/06/2026 | ✅ Apache-2.0. 🟡 pesos Gemma (Gemma Terms of Use) | App **nativo macOS** (WhisperKit + LLM local). Roda no Mac M4. |
| [artbyjazi/autoclip](https://github.com/artbyjazi/autoclip) | 335 | 01/08/2026 | ✅ MIT | Local (Whisper + Ollama) ou com sua chave (Anthropic/OpenAI/Gemini). Queima legenda via libass. |
| [NaufalRizqullah/opensource-clipping](https://github.com/NaufalRizqullah/opensource-clipping) | 286 | 13/11/2026 | ✅ MIT | faster-whisper large-v3 + Gemini + MediaPipe com pan suave e deadzone. Notebook Colab/Kaggle. |
| [AhmedHisham1/pyautoflip](https://github.com/AhmedHisham1/pyautoflip) | 24 | 15/11/2026 | ✅ MIT | **Crop por saliência** (porta Python do AutoFlip do Google). Para conteúdo sem rosto, é melhor que face tracking. |
| [KazKozDev/auto-vertical-reframe](https://github.com/KazKozDev/auto-vertical-reframe) | 25 | 04/10/2026 | ✅ MIT código. ⚠️ YOLO/Ultralytics AGPL | CLI simples de reframe. |
| [xixihhhh/hotclip](https://github.com/xixihhhh/hotclip) · [ColinGPT9/clips-studio](https://github.com/ColinGPT9/clips-studio) | 467 · 268 | 10–11/2026 | 🟡 AGPL-3.0 | Funcionam, mas são AGPL e focados em livestream/Twitch. |

---

## 3. Legendas animadas palavra por palavra (estilo Shorts)

**Caminho mais barato:** já geramos `.ass`. O formato aceita karaokê nativo (`{\k}` / `{\kf}`) e transformações por palavra (`{\t(...)}` para escala e cor). Com os timestamps do §6 dá para gerar **um evento por palavra**, com destaque na palavra falada e "pop" de escala, sem nenhuma dependência nova. As ferramentas abaixo encurtam o trabalho.

| Repo | ⭐ | Últ. push | Licença | Comentário |
|---|---|---|---|---|
| [francozanardi/pycaps](https://github.com/francozanardi/pycaps) | 233 | 30/09/2026 | ✅ MIT | **Melhor opção Python**: estilo em CSS, templates, tagging de palavras-chave e animações. Alpha. |
| [nicolaigaina/ai-video-captions](https://github.com/nicolaigaina/ai-video-captions) | 71 | 27/03/2026 | ✅ MIT | 6 estilos prontos (Hormozi etc.) com faster-whisper + pysubs2 + FFmpeg. Bom para **copiar os presets ASS**. |
| [unconv/captacity](https://github.com/unconv/captacity) | 141 | 07/06/2024 | ✅ MIT | Simples, MoviePy + Whisper. Parado. |
| [muneebkhan08/Capite](https://github.com/muneebkhan08/Capite) | 14 | 21/09/2026 | ✅ MIT | faster-whisper + FFmpeg, legendas cronometradas por palavra. |
| [remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok) | 308 | 09/11/2026 | 🟡 Licença Remotion | Template oficial de legendas TikTok com whisper.cpp. |
| [neutral-Stage/remotion-captioneer](https://github.com/neutral-Stage/remotion-captioneer) · [ahgsql/remotion-subtitles](https://github.com/ahgsql/remotion-subtitles) | 19 · 104 | 2025–26 | ✅ MIT. 🟡 depende do Remotion | Componentes de legenda para Remotion. |
| [nomadkaraoke/python-lyrics-transcriber](https://github.com/nomadkaraoke/python-lyrics-transcriber) | 93 | 19/01/2026 | ✅ MIT | Gera **ASS com timestamps por palavra**. Útil como referência de código para karaokê ASS. |

---

## 4. Thumbnails e fluxo de teste A/B

**Situação real:** não existe projeto open-source maduro de A/B de thumbnail. Os repositórios encontrados têm 0 estrelas ou foram gerados automaticamente. O caminho é o recurso nativo do **YouTube Studio "Testar e comparar"** (até 3 thumbnails por vídeo, vence quem tiver maior participação no tempo de exibição). Ao que sei, ele **não tem API**, então é um passo manual no upload. O Postiz não faz A/B.

**Fluxo proposto:**
1. O Claude gera 3 conceitos (emoção, objeto e texto curto) usando `youtube-agent-skill` (lint título+thumb) ou `ez-thumb`, que compara com o corpus dos concorrentes.
2. A imagem base sai do ElevenLabs. O **rembg/BiRefNet** recorta o sujeito, e o PIL compõe fundo, contorno/glow e texto de 2–4 palavras **por idioma** (EN/PT/ES).
3. QA com o mosaico redimensionado para 168×94 (o tamanho real na home do YouTube).
4. No upload, ativar "Testar e comparar" com as 3 variantes e registrar o vencedor numa planilha (ângulo, emoção, cor). Depois de cerca de 20 vídeos, isso vira regra do canal.

| Repo | ⭐ | Últ. push | Licença | Comentário |
|---|---|---|---|---|
| [danielgatis/rembg](https://github.com/danielgatis/rembg) | 25.506 | 06/11/2026 | ✅ MIT. ⛔ modelo `bria-rmbg` é NC | Recorte em CPU. Use os modelos `birefnet-*` ou `isnet-general-use`. |
| [ZhengPeng7/BiRefNet](https://github.com/ZhengPeng7/BiRefNet) | 4.410 | 25/10/2026 | ✅ MIT | Matting de alta resolução. |
| [Bria-AI/RMBG-2.0](https://github.com/Bria-AI/RMBG-2.0) | 351 | 03/11/2026 | ⛔ **CC-BY-NC-4.0** (comercial só com contrato pago) | **Não usar.** |
| [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) | 6.061 | 16/09/2026 | ✅ MIT | Lint do par título+thumb. |
| [charlesdove977/ez-thumb](https://github.com/charlesdove977/ez-thumb) | 7 | 23/10/2026 | ✅ MIT | Skill de "packaging" de título e thumbnail: onboarding com concorrentes reais, corpus persistente. O README tem muito marketing do autor. |
| [AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube) | 778 | 10/04/2026 | ✅ MIT | `/youtube thumbnail` gera imagem via **Gemini API** (custo à parte) + auditoria de canal e SEO. |
| [ajayyy/DeArrow](https://github.com/ajayyy/DeArrow) | 2.359 | 17/10/2026 | 🟡 GPL-3.0 | Extensão de títulos e thumbs crowdsourced. **Não serve para nós.** Citado só para descartar. |

> Já existem localmente as skills `social-media-skills:thumbnail-design` e `social-media-skills:youtube-publishing-and-metadata`. Use-as junto com as acima antes de instalar algo novo.

---

## 5. Ken Burns, parallax 2.5D e câmera guiada por profundidade

**Recomendação:** **Depth Anything V2-Small** ou **DA3-Small/Base/Mono-Large** (todos Apache) geram o depth, e o **DepthFlow** renderiza (AGPL, uso comercial dos vídeos ok). Alternativa sem dependência: implementar no nosso numpy o deslocamento por camadas (3 a 5 faixas de profundidade, com inpainting simples de borda), à maneira do pixflow e do parallax-doc.

| Repo | ⭐ | Últ. push | Licença | Comentário |
|---|---|---|---|---|
| [BrokenSource/DepthFlow](https://github.com/BrokenSource/DepthFlow) | 1.590 | 13/11/2026 | 🟡 AGPL-3.0 ("commercial use encouraged") | O melhor gerador de parallax. Em lote, via Python/CLI (`pip install depthflow`). |
| [akatz-ai/ComfyUI-Depthflow-Nodes](https://github.com/akatz-ai/ComfyUI-Depthflow-Nodes) | 369 | 15/02/2026 | 🟡 AGPL-3.0 | DepthFlow dentro do ComfyUI, que já está na nossa stack da 5090. |
| [DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | 9.158 | 24/03/2026 | ✅ código Apache. ✅ **Small** Apache. ⛔ **Base/Large/Giant CC-BY-NC-4.0** | Use apenas o Small. |
| [ByteDance-Seed/Depth-Anything-3](https://github.com/ByteDance-Seed/Depth-Anything-3) | 6.693 | 27/07/2026 | ✅ código Apache. ✅ pesos **DA3-Small, DA3-Base, DA3Metric-Large, DA3Mono-Large** Apache. ⛔ **DA3-Large, DA3-Giant e Nested são CC-BY-NC-4.0** | O **DA3Mono-Large** é a melhor opção comercial para depth de imagem única. |
| [localai-org/depth-anything.cpp](https://github.com/localai-org/depth-anything.cpp) | 1.137 | 07/09/2026 | ✅ MIT (pesos herdam a licença) | Depth em CPU ou Mac sem torch. |
| [sanskarprajapati/parallax-doc](https://github.com/sanskarprajapati/parallax-doc) | 8 | 2026 | ✅ MIT. ❓ HyperFrames não verificado | Estilo documental histórico em plano-sequência. Ótimo como referência. |
| [inematds/pixflow](https://github.com/inematds/pixflow) | 8 | 10/2026 | ❓ **sem licença** | Em PT-BR: movie spec YAML → DA-V2-small (transformers.js) → GLSL → Remotion. Tem looks noir e épico, câmeras `push_in/dolly/orbit/handheld`. **Só como referência**: sem licença e com Remotion. |
| [provos/parallax-maker](https://github.com/provos/parallax-maker) | 109 | 27/09/2026 | 🟡 AGPL-3.0 | Separa a imagem em camadas para animação 2.5D, com inpainting. |
| [Trekky12/kburns-slideshow](https://github.com/Trekky12/kburns-slideshow) | 77 | 09/11/2025 | ✅ MIT | Ken Burns clássico em ffmpeg, com sincronia de batida (aubio). Útil para copiar curvas de easing. |
| [vt-vl-lab/3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting) | 7.102 | 30/08/2024 | ✅ MIT | Fotografia 3D com inpainting de camadas (CVPR 2020). Qualidade boa, mas é lento e a stack é antiga (PyTorch 1.4). |
| [sniklaus/3d-ken-burns](https://github.com/sniklaus/3d-ken-burns) | 1.580 | 16/11/2026 | ⛔ **CC-BY-NC-SA-4.0 (Adobe Research)** | **Não usar comercialmente**, apesar de ser o mais famoso. |

---

## 6. Alinhamento forçado (timestamps por palavra) em CPU

**Primeiro, o atalho:** o endpoint de TTS **"with timestamps"** do ElevenLabs devolve alinhamento por caractere junto com o áudio, sem custo extra. Se a narração vier de lá, agrupar caracteres em palavras resolve sem modelo nenhum. Para áudio já gerado sem timestamps, ou para conferir, use a tabela abaixo.

| Repo | ⭐ | Últ. push | Licença | CPU? | Comentário |
|---|---|---|---|---|---|
| [jianfch/stable-ts](https://github.com/jianfch/stable-ts) | 2.282 | 30/05/2026 | ✅ MIT (pesos Whisper MIT) | Sim | **Recomendado.** `align()` com o texto do roteiro, multilíngue e robusto. Também tem modo sem Whisper e com faster-whisper. |
| [m-bain/whisperX](https://github.com/m-bain/whisperX) | 25.353 | 12/11/2026 | ✅ BSD-2 (código) | Sim (`int8`) | Padrões de alinhamento do `alignment.py`: EN = `WAV2VEC2_ASR_BASE_960H` (fairseq, MIT), PT = `jonatasgrosman/wav2vec2-large-xlsr-53-portuguese` [confirmar no HF], **ES = `VOXPOPULI_ASR_BASE_10K_ES`**. ⚠️ A documentação do torchaudio indica que os modelos VoxPopuli são **CC-BY-NC-4.0**. Em ES, passe `--align_model jonatasgrosman/wav2vec2-large-xlsr-53-spanish` [confirmar no HF]. A diarização (pyannote) é opcional e não é necessária. |
| [MahmoudAshraf97/ctc-forced-aligner](https://github.com/MahmoudAshraf97/ctc-forced-aligner) | 576 | 07/09/2026 | ✅ BSD-2 código. ⛔ **o modelo padrão (MMS-300m) é CC-BY-NC-4.0**, como o próprio README avisa | Sim | Leve e rápido com texto conhecido. **Obrigatório trocar `--alignment_model`** por um wav2vec2 PT/ES/EN de licença livre. |
| [MontrealCorpusTools/Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) | 1.917 | 15/11/2026 | ✅ MIT. 🟡 modelos CC-BY-4.0 | Sim | O mais preciso (Kaldi). Instala via conda. Precisa de dicionário de pronúncia, e nomes raros exigem G2P. |
| [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 26.783 | 12/11/2026 | ✅ MIT | Sim (int8) | `word_timestamps=True`. É ASR, não alinhamento com o texto: palavras podem divergir do roteiro. |
| [readbeyond/aeneas](https://github.com/readbeyond/aeneas) | 2.876 | 25/07/2026 | 🟡 AGPL-3.0 | Sim | DTW contra TTS. Bom por frase, fraco por palavra. |
| [strob/gentle](https://github.com/strob/gentle) | 1.713 | 24/07/2026 | ✅ MIT | Sim | **Só inglês.** |
| [echogarden-project/echogarden](https://github.com/echogarden-project/echogarden) | 454 | 08/09/2026 | ❓ o GitHub não identifica a licença (verificar o arquivo) | Sim | Toolkit Node com alinhamento por DTW/Whisper. |
| [linto-ai/whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) | 2.861 | 28/09/2026 | 🟡 AGPL-3.0 | Sim | Funciona, mas a licença é pior que a do stable-ts. |
| [nyrahealth/CrisperWhisper](https://github.com/nyrahealth/CrisperWhisper) | 1.492 | 11/11/2026 | ❓ NOASSERTION. Pesos [confirmar no HF], provavelmente NC | – | Evitar até confirmar a licença. |

---

## 7. Bibliotecas de SFX e música com licença comercial

Para música **gerada localmente** (ACE-Step, DiffRhythm, Stable Audio 3), ver `docs/pesquisa/local_audio.md`. Aqui ficam só bibliotecas prontas e ferramentas de busca.

| Repo | ⭐ | Últ. push | Licença | Comentário |
|---|---|---|---|---|
| [wyzowl/sfx-kit](https://github.com/wyzowl/sfx-kit) | 41 | 20/10/2026 | ✅ CC0 | 320 SFX com sync point e nível. **Baixar já.** |
| [maximilianfeix/plinkfx](https://github.com/maximilianfeix/plinkfx) | 28 | 15/11/2026 | ✅ sons CC0, código MIT | 180 SFX + MCP local. Puxado para game e UI, mas tem impactos e transições úteis. |
| [sfxmint/sfxmint-mcp](https://github.com/sfxmint/sfxmint-mcp) | 8 | 13/11/2026 | ✅ áudio CC0 | MCP de busca por descrição. **Limite grátis:** 5 downloads por dia por rede (20 com chave grátis). Grava o manifesto de licença. |
| [btahir/open-lofi](https://github.com/btahir/open-lofi) | 60 | 15/03/2026 | ✅ CC0 | Mais de 150 faixas lo-fi. Pouco documental, mas serve para fundo de Shorts. |
| [SoundSafari/CC0-1.0-Music](https://github.com/SoundSafari/CC0-1.0-Music) | 82 | 05/12/2023 | ✅ CC0 (declarado) | Cerca de 7.000 músicas (~40 GB) agregadas de vários sites. ⚠️ É uma agregação de terceiros com processo de takedown, então há risco de faixa mal classificada e de **Content ID**. Use com triagem. |
| [skyzhao1223/free-for-creators](https://github.com/skyzhao1223/free-for-creators) | 84 | 11/11/2026 | ✅ CC0 (a lista) | Diretório com colunas de monetização e atribuição verificadas. Ponto de partida para Pixabay, Mixkit, Sonniss GDC etc. |
| [MTG/freesound-python](https://github.com/MTG/freesound-python) | 159 | 22/10/2026 | ✅ MIT (cliente) | API do Freesound. ⚠️ **Cada som tem a própria licença** (CC0, CC-BY ou **CC-BY-NC**): filtre `license:"Creative Commons 0"`. |
| [vibe-motion/sound](https://github.com/vibe-motion/sound) | 629 | 29/10/2026 | ❓ **código sem licença** | Skill do Claude Code que busca no Freesound com filtro `--license cc0`. Serve como ideia; reescrever é trivial. |
| [Losera/soundfetch](https://github.com/Losera/soundfetch) | 4 | 23/10/2026 | ✅ MIT | CLI/MCP de busca com manifesto de licença (Internet Archive, Openverse, Freesound). |
| [kanaworksai-hue/audio-studio-mcp](https://github.com/kanaworksai-hue/audio-studio-mcp) | 673 | 16/11/2026 | ✅ MIT código. 🟡 **pesos Stable Audio 3: Stability Community License** (grátis abaixo de US$ 1 mi de receita/ano) | MCP local de BGM e SFX para o Claude Code. |
| [facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft) (MusicGen/AudioGen) | 23.881 | 03/03/2026 | ✅ código MIT. ⛔ **pesos CC-BY-NC-4.0** | **Não usar** os modelos num canal monetizado. |

---

## 8. Skills e plugins do Claude Code para produção de vídeo e SEO no YouTube

| Repo | ⭐ | Últ. push | Licença | Comentário |
|---|---|---|---|---|
| [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | 6.046 | 16/11/2026 | ✅ MIT | Camada FFmpeg confiável com contrato JSON, presets de plataforma e loudness. **Top 1 das skills.** |
| [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) | 6.061 | 16/09/2026 | ✅ MIT | Ganchos, par título+thumb, retenção, Shorts dentro do vídeo longo e outliers. |
| [sanskarprajapati/parallax-doc](https://github.com/sanskarprajapati/parallax-doc) | 8 | 2026 | ✅ MIT. ❓ HyperFrames | Documentário histórico parallax. |
| [hassancs91/claude-faceless-shorts-creator](https://github.com/hassancs91/claude-faceless-shorts-creator) | 366 | 18/08/2026 | ✅ MIT. 🟡 Remotion | Shorts faceless com ElevenLabs e legendas por palavra. |
| [AgriciDaniel/claude-shorts](https://github.com/AgriciDaniel/claude-shorts) | 401 | 11/07/2026 | ✅ MIT. 🟡 Remotion | Long → short com legendas animadas. |
| [adityaarsharma/youtube-marketing-skills](https://github.com/adityaarsharma/youtube-marketing-skills) | 85 | 10/10/2026 | ✅ MIT | MCP com analytics reais + escrita de SEO no canal. |
| [AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube) | 778 | 10/04/2026 | ✅ MIT | Auditoria de canal, SEO, roteiros de retenção. A thumbnail usa Gemini (pago). |
| [sergebulaev/youtube-skills](https://github.com/sergebulaev/youtube-skills) | 99 | 11/11/2026 | ✅ MIT | Títulos de alto CTR, descrições SEO, Shorts. A publicação usa Publora (não precisamos: temos Postiz). |
| [TubeLabHQ/youtube-research-skills](https://github.com/TubeLabHQ/youtube-research-skills) | 98 | 15/11/2026 | ✅ MIT | Outliers, validação de nicho, mineração de comentários. ⚠️ O MCP depende da API da TubeLab (plano Pro, pago). |
| [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | 2.867 | 14/10/2026 | ✅ MIT (arquivo LICENSE; a API do GitHub mostra NOASSERTION) | 15 skills de edição de reels e Shorts (Node 22, Chrome). Mais voltado a talking-head. |
| [OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage) | 80.771 | 09/11/2026 | 🟡 AGPL-3.0 | Mega-coleção de pipelines e skills. Bom para garimpar receitas. |
| [zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) | 2.170 | 15/11/2026 | ✅ CC0 (lista) | Índice de 180 repos de skills de vídeo, com teste comparativo de 16 skills. Bom para descobrir mais. |
| [DojoCodingLabs/remotion-superpowers](https://github.com/DojoCodingLabs/remotion-superpowers) | 168 | 29/10/2026 | ✅ MIT. 🟡 Remotion | Estúdio Remotion com ElevenLabs, Pexels e Whisper. Só vale se migrarmos para Remotion. |
| [jianshuo/claude-skills](https://github.com/jianshuo/claude-skills) | 142 | 15/11/2026 | ✅ MIT | 13 skills: transcrever, traduzir, dublar, legendas, reframe, multicam. A legendagem em PT/ES usa Whisper word-level da OpenAI (API). |

---

## 9. Instalar primeiro

1. **stable-ts (MIT)**: substitui a heurística do `koepcke/scripts/alinhar.py` por alinhamento forçado real com o roteiro, em CPU, nos três idiomas. É a base de tudo: legenda por palavra, cortes no beat e Shorts. Antes de instalar, teste se o endpoint "with timestamps" do ElevenLabs já resolve.
2. **kajisho5/ffmpeg-skill (MIT)**: dá ao Claude Code uma camada FFmpeg verificável (export 9:16, loudness por plataforma, QA) por cima do nosso `render.py`.
3. **Depth Anything V2-Small ou DA3Mono-Large (Apache) + DepthFlow (AGPL, uso como ferramenta)**: troca o zoompan por parallax 2.5D nas imagens do ElevenLabs. É o maior salto de qualidade visual por hora investida. Rodar na 5090 em lote.
4. **wyzowl/sfx-kit (CC0)**: biblioteca de SFX com sync point, pronta para a mixagem do `render.py`.
5. **Jakeschincariol/youtube-agent-skill (MIT)**: lint do par título+thumb e análise de retenção, sem API key. Combine com **rembg (modelos birefnet)** e o "Testar e comparar" do YouTube Studio para o fluxo de thumbnails.
6. Depois: **pycaps** para legendas animadas dos Shorts. Ou, mais barato, estender o nosso gerador ASS para um evento por palavra com `\t` e `\k`.

**Nunca usar comercialmente:** sniklaus/3d-ken-burns (CC-BY-NC-SA), pesos Depth Anything V2 Base/Large/Giant e DA3 Large/Giant/Nested (CC-BY-NC), Bria RMBG-2.0 e o modelo `bria-rmbg` do rembg (CC-BY-NC), MusicGen/AudioGen (CC-BY-NC), o modelo MMS padrão do ctc-forced-aligner (CC-BY-NC), o modelo ES padrão do WhisperX (VoxPopuli, provavelmente NC) e qualquer repositório sem licença (autoshorts, Autocrop-vertical, pixflow, vibe-motion/sound).
