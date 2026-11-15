# Geração local de vídeo com IA para canal documental faceless: RTX 5090 + Mac M4

**Data da pesquisa:** 15/11/2026
**Fontes:** GitHub (API de busca + arquivos README/LICENSE via raw.githubusercontent.com). A cota de WebSearch estava esgotada e o huggingface.co está bloqueado neste ambiente. Por isso não consegui ler as licenças que existem **apenas** nos model cards do Hugging Face. Elas estão marcadas como **[confirmar no HF]**.
**Legenda:** ✅ verificado em arquivo do repositório · 🟡 fonte secundária (benchmark ou índice comunitário no GitHub) · ⚠️ estimativa minha

---

## 0. Resumo executivo

| Pergunta | Resposta curta |
|---|---|
| Melhor modelo local, grátis e **comercial sem pegadinhas** | **Wan 2.2** (T2V/I2V A14B MoE + TI2V 5B). Apache-2.0 no código e nos pesos ✅. |
| Wan 2.5 / 2.6 / 2.7 / 3.0 são open? | **Não.** Só existem por API. No GitHub só aparecem relays de API, e o template oficial do ComfyUI é `api_wan2_6_*`, `api_wan2_7_*`, `api_wan3_0_*` ✅. A linha aberta parou na 2.2 (+ Animate-2) 🟡. |
| Melhor alternativa também permissiva | **LongCat-Video** (Meituan, 13,6B, pesos sob **MIT** ✅, T2V/I2V/continuação, 720p a 30fps) e **Kandinsky 5.0 Video Pro/Lite** (repositório MIT ✅, pesos [confirmar no HF]). |
| Modelos com cláusula que pesa para YouTube global | **HunyuanVideo / I2V / 1.5**, **FramePack** (usa pesos Hunyuan), **SkyReels V1** (base Hunyuan) e **MiniMax H3**: todos têm exclusão territorial (UE/Reino Unido/Coreia, e no H3 também os EUA). O texto da Tencent proíbe inclusive *exibir o Output fora do Território*. Não use como motor principal de um canal com audiência mundial. |
| LTX-2.3 / LTX-2.5 | Código Apache-2.0, mas os **pesos usam a LTX-2 Community License**: grátis apenas se a receita anual da entidade for **< US$ 10 milhões** ✅. Atende vocês hoje, mas é uma condição a monitorar. |
| Stack recomendada | **ComfyUI (PyTorch cu130) + Wan 2.2 I2V A14B fp8/NVFP4 + LoRA LightX2V 4 passos + SageAttention + SeedVR2 3B (upscale) + RIFE/GIMM (interpolação)**. **Wan2GP** como alternativa "fila pronta". |
| Produção estimada (5090 desktop) ⚠️ | **~15–20 clipes/h** de 5 s em 720p nativo, ou **~12–18 clipes/h** de 5 s finalizados em 1080p (gerados em 480p e ampliados). Isso dá **~300–450 clipes/dia** em 24/7. |
| Mac M4 | Viável só para testes ou como apoio: **10–45 min por clipe**. Use como estação de roteiro, edição e controle da fila. |

---

## 1. RTX 5090 (Blackwell, sm_120): compatibilidade

- O sm_120 entrou no PyTorch **2.7 + CUDA 12.8 (cu128)**, que é o mínimo. O README atual do ComfyUI ✅ diz: *"Using a cu130 or above version of pytorch is required on Nvidia 20 series and above"*. Instale **PyTorch estável com cu130**:
  `pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130`
  (o nightly usa cu132).
- Um benchmark real numa 5090 Laptop 🟡 (repositório `lifeidle/comfyui-5090-laptop-24gb-...`) usou ComfyUI 0.43.0, PyTorch 2.14.1+cu130 e driver 617.42. A conclusão dele: **em Blackwell, prefira NVFP4**. Foi 2,6× mais rápido que INT8 e 27% menor, sem perda de qualidade mensurável. Com os kernels cu130, a NVFP4 ficou 3,45× mais rápida que o modo eager.
- **SageAttention** (Apache-2.0 ✅) tem builds para Blackwell. Para modelos MiniMax H3 existe também o **Sol-Attn** da NVIDIA, 1,14–1,44× mais rápido que Sage numa 5090 🟡.
- Com 32 GB de VRAM, a 5090 desktop tem 8 GB a mais que a laptop do benchmark. Os dois especialistas do Wan 2.2 14B em fp8 (14,3 GB cada, carregados alternadamente high-noise/low-noise) cabem com muito menos offload. Recomendo **64 GB+ de RAM** (o ideal é 96–128 GB) e **NVMe de 2 TB** só para modelos.
- Driver: use o Studio/Game Ready mais recente com suporte a CUDA 13.

---

## 2. Modelos de geração: avaliação um a um

### 2.1 Tabela-mestra

| Modelo | Licença do código | Licença dos pesos | Comercial? | Params / VRAM | I2V | Velocidade publicada | Nota de qualidade |
|---|---|---|---|---|---|---|---|
| **Wan 2.2 A14B (T2V / I2V / FLF2V)** | Apache-2.0 ✅ | Apache-2.0 ✅🟡 | **Sim, sem condições** | MoE 2×14B; fp8 = 2×14,3 GB; GGUF Q4–Q8 para menos VRAM | **Sim** (I2V-A14B, FLF2V primeiro/último quadro) | 5090 **Laptop**: 832×480×81 quadros, 4 passos (LightX2V) = **93,8 s** 🟡. Com 20 passos, 7,9× mais lento 🟡 | O melhor equilíbrio aberto. Ótimo em movimento de câmera e física. Saída nativa a 16 fps. |
| **Wan 2.2 TI2V 5B** | Apache-2.0 ✅ | Apache-2.0 | Sim | 5B; fp16 ≈ 10 GB; roda em 24 GB ✅ | Sim (texto e imagem num só modelo) | 5090 Laptop: 1280×704×121 quadros (5 s a 24 fps) = **355 s** sem destilação 🟡. Existe versão Turbo de 4 passos (`quanhaol/Wan2.2-TI2V-5B-Turbo`) | 720p a 24 fps nativo. Segue bem o prompt, mas tem menos detalhe que o 14B. |
| Wan 2.1 14B / 1.3B | Apache-2.0 ✅ | Apache-2.0 | Sim | 14B / 1.3B | Sim (I2V 480p/720p, VACE) | Superado pelo 2.2 | Use só por causa de LoRAs antigas. |
| Wan 2.2 Animate-2 / S2V | Apache-2.0 | Apache-2.0 🟡 | Sim | 14B | Animação de personagem / áudio→vídeo | Move: 105 s em 832×480 (laptop) 🟡 | Pouco útil para faceless. |
| **Wan 2.5 / 2.6 / 2.7 / 3.0** | – | **Fechado (API)** ✅ | – | – | – | – | Não há pesos para rodar localmente. |
| **LongCat-Video** (Meituan) | MIT ✅ | **MIT** ✅ (README: *"model weights are released under the MIT License"*) | **Sim** | 13,6B | Sim (T2V, I2V, continuação de vídeo) | "720p a 30 fps em minutos" (estratégia coarse-to-fine + block sparse attention) ✅ | Forte em vídeos longos e consistência. Bom 2º motor. Tem suporte no Wan2GP e no LightX2V. |
| **Kandinsky 5.0 Video Pro / Lite** | MIT ✅ | MIT? [confirmar no HF] | Provável | Pro 19B / Lite 2B (Lite roda em 12 GB) | Sim (Pro I2V e Lite I2V) | Lite: 4,57 GB, o mais leve 🟡 | O Pro chegou a Top-1 open T2V no LMArena em dez/2025 ✅. Tem LoRAs de câmera. Templates `video_kandinsky5_t2v/i2v`. |
| **HunyuanVideo / HunyuanVideo-I2V / HunyuanVideo 1.5** | Licença Tencent (NOASSERTION) | **Tencent Hunyuan Community License** ✅ | **Condicional**: território exclui **UE, Reino Unido e Coreia do Sul**; >100M MAU exige licença à parte; proíbe usar a saída para treinar outros modelos | 1.5: 8,3B; mínimo de 14 GB com offload ✅ | Sim (720p I2V; 480p I2V step-distilled) | 1.5 480p I2V distilled: **~75 s numa 4090** ✅. No laptop 24 GB, 720p→1080p SR não terminou em 70 min 🟡 | Estética cinematográfica excelente. **Risco jurídico**: a cláusula 5(c) proíbe *"use… display… Output… outside the Territory"*. Um vídeo no YouTube é exibido na UE. |
| **LTX-Video (0.9.x) / LTX-2 / LTX-2.3 / LTX-2.5** | Apache-2.0 ✅ | **LTX-2 Community License** (2.3) / **LTX-2.x Community License** (2.5) ✅ | **Sim se receita anual < US$ 10M** (entidades acima disso pagam) ✅ | 2.3/2.5: 22B (14B vídeo + 5B áudio) + encoder Gemma; o download do 2.5 tem ~66 GiB ✅. GGUF/fp8 disponíveis | Sim (T2V, I2V, FLF2V, IA2V, IC-LoRA) | LTX-Video 2B: 19–23 s 🟡, porém **não seguia o prompt** no teste 🟡. 2.3/2.5 distilled: rápidos, sem número verificado para 5090 | **Gera áudio sincronizado.** O 2.5 tem pipeline DFR "production quality" e vai até 4K. Templates `video_ltx2_5_t2v/i2v/flf2v/dfr_i2v`. |
| **CogVideoX 1.5-5B (T2V / I2V)** | Apache-2.0 ✅ | **CogVideoX License** (só o 2B é Apache) ✅ [termos: confirmar no HF] | Condicional (registro / limites) | 5B | Sim (I2V em qualquer resolução) | 5 s: ~550 s numa H100 / ~1000 s numa A100 ✅ | Ficou para trás (2024). Não recomendo. |
| **Mochi 1 (Genmo)** | Apache-2.0 ✅ | Apache-2.0 ✅ | Sim | 10B; ~60 GB nativo, **< 20 GB no ComfyUI** ✅ | **Não (só T2V)** | Lento | Só 480p ✅. Fraco em animação. Não recomendo. |
| **SkyReels V1** | (Skywork) | Base HunyuanVideo, **herda a licença Tencent** | Condicional | 13B | Sim | – | Foco em humanos. Evitar pela licença. |
| **SkyReels V2 (DF / I2V 14B 720p)** | Skywork | **Skywork Community License**: *"supports commercial use… no need to apply"* ✅ | Sim, com termos próprios (ler o PDF) | 1.3B / 14B (base Wan 2.1) | Sim; Diffusion Forcing para duração "infinita" | – | Bom para planos longos/extensão. Fica atrás do Wan 2.2 em qualidade por clipe. |
| **SkyReels V3** | Skywork (NOASSERTION) | Skywork (provável) [confirmar no HF] | Provável | R2V / V2V 14B 720p, avatar 19B | Referência→vídeo e extensão de 5–30 s ✅ | – | Útil para estender planos. |
| **FramePack / F1** (lllyasviel) | Apache-2.0 ✅ | Usa **HunyuanVideo** (FramePack-I2V-HY), **herda a licença Tencent** | Condicional | 13B; roda com 6 GB | **Só I2V** (ótimo para animar stills) | Gera progressivamente; o custo não cresce com a duração | Bom para "animar fotos", mas com o mesmo risco territorial do Hunyuan. |
| **MAGI-1 / MAGI-1.1** (Sand AI) | Apache-2.0 ✅ | Apache-2.0 ✅ | Sim | 4.5B (1× 4090) / 24B (8× H100 ou 8× 4090) ✅ | Sim (autorregressivo, extensão) | – | O 24B não cabe numa 5090. O 4.5B fica abaixo do Wan 2.2. |
| **Open-Sora 2.0** | Apache-2.0 ✅ | Apache-2.0 ✅ | Sim | 11B; 256px em 1 GPU, **768px exige multi-GPU** ✅ | Sim (T2I2V) | Lento | Ficou para trás. Não recomendo. |
| **Step-Video T2V / TI2V** | MIT ✅ | MIT [confirmar no HF] | Provável | **30B**; projetado para GPUs de 80 GB | TI2V sim | – | Pesado demais para 32 GB sem quantização agressiva. Não recomendo. |
| **MiniMax H3** (2026) | Apache-2.0 (implementações da comunidade) | **MiniMax H3 Community License** 🟡: exclui **EUA/UE/Reino Unido/Coreia**, < US$ 20M de receita, exige atribuição "MiniMax H3" | **Condicional, e arriscado para YouTube global** | DiT 33B (~20 GB pruned int8) + encoder Qwen3-VL-32B (~15 GB nvfp4) | Sim (FL2VA, Ref2VA com até 9 imagens) | 5090 Laptop: 1344×768×124 quadros com áudio = 519 s (8 passos) / 286 s (4 passos) 🟡. 5090: 17 s/it em 1280×736 🟡 | Qualidade topo de linha + **áudio estéreo nativo**, até 2K e 15 s. Pela licença, não recomendo para este canal. |

### 2.2 Sobre licença e uso no YouTube

1. **Tencent (Hunyuan, FramePack-HY, SkyReels V1):** o Brasil está dentro do "Território". O problema é a cláusula 5(c) ✅: *"You must not use, reproduce, modify, distribute, or display the Tencent Hunyuan Works, Output or results… outside the Territory."* Um canal do YouTube é exibido na UE e no Reino Unido. Na leitura literal, isso é uso não licenciado do Output. Para um negócio que depende de monetização, **é risco desnecessário** quando Wan e LongCat estão disponíveis sem essa cláusula.
2. **MiniMax H3:** o raciocínio é o mesmo, com o agravante de que os EUA (sede do YouTube e maior mercado de CPM) também estão excluídos 🟡. Não consegui ler o LICENSE no HF, então confirme antes de usar.
3. **LTX-2.x:** o limite de US$ 10M considera a receita da entidade **somada à do grupo econômico** ✅. Para um canal novo, o uso é livre. Guarde uma cópia da licença na data do download.
4. **Wan 2.2, LongCat, MAGI-1, Mochi, Open-Sora, Step-Video:** licenças permissivas (Apache ou MIT). Você continua responsável pelo conteúdo, pelos direitos das imagens de entrada e pelas regras do YouTube sobre conteúdo sintético (marcar "conteúdo alterado/sintético" quando parecer realista).
5. **Ferramentas:** o **ComfyUI é GPL-3.0**. Isso afeta a redistribuição do software, **não** os vídeos gerados. **WanVideoWrapper** é Apache-2.0 ✅. **SwarmUI** e **Pinokio** são MIT ✅. **Wan2GP** usa a *WanGP Community License 2.0* ✅: o uso é grátis inclusive em empresa e os outputs podem ser vendidos. Só se pede crédito quando o output em si é vendido ou licenciado. O que é proibido é revender o WanGP como SaaS.

---

## 3. Aceleradores

| Técnica | Licença | O que faz | Uso recomendado |
|---|---|---|---|
| **LightX2V** (ModelTC) | Apache-2.0 ✅ (pesos no HF `lightx2v/*`, [confirmar no HF]) | LoRAs e modelos destilados de **4 passos sem CFG** para Wan 2.1/2.2, HunyuanVideo 1.5 e MiniMax H3. Em abr/2026 saiu `wan2.2_i2v_A14b_{high,low}_noise_lightx2v_4step_720p_260412` (treinado em 720p) ✅. Em mai/2026 saiu **Wan2.2-NVFP4-Sparse** para Blackwell: *">50× de speedup end-to-end vs 40 NFE numa RTX 5090"* ✅ | **Essencial.** Use o LoRA 4-step 720p no I2V. Para produção máxima, teste o NVFP4-Sparse (configs `configs/wan22/extreme/*nvfp4_sparse_attn.json`). |
| **Self-Forcing** | Apache-2.0 ✅ | Destilação autorregressiva (Wan 1.3B), quase em tempo real | Prévias rápidas. Qualidade inferior. |
| **CausVid** | Repositório sem SPDX (NOASSERTION) [verificar; possivelmente não comercial] | LoRA de poucos passos | **Evite.** Use LightX2V no lugar. |
| **TeaCache / MagCache** | Apache-2.0 ✅ | Cache entre timesteps, 1,5–2× | Útil com 20+ passos. **Pouco ganho com 4 passos.** |
| **SageAttention 2/3** | Apache-2.0 ✅ | Atenção quantizada, 2–5× no kernel | **Ligue sempre** (`--use-sage-attention`). |
| **GGUF** (city96/ComfyUI-GGUF) | Apache-2.0 ✅ | Q4–Q8 para caber em pouca VRAM | Na 5090, prefira **fp8_scaled ou NVFP4**. GGUF é mais lento que fp8 nativo. |
| **NVFP4** | – | FP4 nativo de Blackwell | **O melhor formato na 5090** 🟡. |
| **torch.compile** | – | +10–30% | Ative depois que o pipeline estiver estável. |
| **Regra de bolso** 🟡 | | *"Velocidade vem de reduzir passos, não de comprimir pesos."* 8→4 passos rende mais que qualquer quantização. A quantização serve para caber na VRAM; o LoRA destilado serve para acelerar. | |

**Problema conhecido:** LoRAs de 4 passos no Wan 2.2 I2V tendem a gerar **câmera lenta**. O nó `princepainter/ComfyUI-PainterI2V` (636★) corrige isso 🟡.
**Pegadinha** 🟡: o Wan 2.2 **14B usa `wan_2.1_vae`** (16 canais) e o **5B usa `wan2.2_vae`** (48 canais). Trocar um pelo outro gera o erro "expected 48 channels, got 16".

---

## 4. Orquestração

| Ferramenta | Licença | Prós | Contras | Papel |
|---|---|---|---|---|
| **ComfyUI** (+ ComfyUI-Manager) | GPL-3.0 | Suporte no dia 0, templates oficiais, **API HTTP/WebSocket** para fila em lote | Curva de aprendizado | **Motor principal.** |
| **ComfyUI-WanVideoWrapper** (kijai) | Apache-2.0 ✅ | Recursos novos primeiro (block swap, LoRAs LightX2V, contexto longo, FlashVSR) | Muda com frequência | Use quando o nó nativo não tiver o recurso. |
| **Wan2GP / WanGP** (deepbeepmeep) | WanGP CL 2.0 ✅ | Interface única com **fila de geração, modo headless, API e MCP**; Wan 2.1/2.2, LTX-2.x, Hunyuan 1.5, LongCat, Kandinsky, H3; upscalers **RIFE, FlashVSR, SeedVR**; NVFP4/GGUF/int8 | Menos flexível que grafos do ComfyUI | **Plano B / farm simples**: dá para enfileirar centenas de prompts sem montar grafos. |
| **SwarmUI** | MIT ✅ | Interface sobre o ComfyUI, multi-GPU/multi-backend | Mais uma camada | Se quiser front-end amigável + ComfyUI no back-end. |
| **Pinokio** | MIT ✅ | Instalador de 1 clique (inclui Wan2GP, FramePack) | Menos controle, ambientes duplicados | Só para testar rápido. Não use na farm. |
| **LightX2V** (CLI/servidor) | Apache-2.0 ✅ | Servidor HTTP (`scripts/wan22/server/start_server_t2v.sh`), NVFP4+sparse | Menos visual | Opção de máximo throughput. |

---

## 5. Upscaling e interpolação (local, grátis)

| Ferramenta | Licença | Uso | Notas |
|---|---|---|---|
| **SeedVR2 3B / 7B** (ByteDance-Seed) | **Apache-2.0** ✅ (código e nó `numz/ComfyUI-SeedVR2_VideoUpscaler` ✅) | Restauração/upscale de vídeo por difusão **em 1 passo**, com consistência temporal | O melhor para 480p→1080p. Templates oficiais `utility_seedvr2_video_upscale`, `utility_seedvr2_3b_int8_upscale_video` ✅. Imagem 768²→3072² em 23,6 s no laptop 🟡. Exige PyTorch 2.9+ (correção de VRAM do Conv3d ✅). |
| **Real-ESRGAN** | **BSD-3-Clause** ✅ | Upscale quadro a quadro com GAN, rápido | Pode cintilar entre quadros. Serve para material simples. Template `utility-gan_upscaler`. |
| **RIFE** (hzwer, Practical-RIFE) | **MIT** ✅ | Interpolação 16→32 fps (depois converter para 24/30) | Rapidíssimo. Nó `Fannovel16/ComfyUI-Frame-Interpolation` (MIT ✅). Alguns outros modelos desse pacote têm licença própria. |
| **GIMM-VFI / FILM** | (ver cada um) | Interpolação de qualidade maior | Templates `utility_gimm_frame_interpolation`, `utility-frame_interpolation-film` ✅. |
| **FlashVSR / RelayVSR** | [confirmar] | VSR rápido | Integrados ao Wan2GP. Templates `utility_relayvsr_video_x2/x4_upscale` ✅. |
| **LTX-2.5 spatial/temporal upscaler** | LTX-2.x CL | Upscale latente dentro do LTX | Só no pipeline LTX. |

Pipeline típico: **Wan 2.2 em 832×480 ou 1280×720 a 16 fps → RIFE ×2 (32 fps) → reamostrar para 24 ou 30 fps no ffmpeg → SeedVR2 3B para 1080p (ou 1440p)**.

---

## 6. Mac M4: dá para usar?

- Dá, mas **é lento demais para farm**. Benchmark primário do Draw Things 🟡 (MiniMax H3, 1024×512, 124 quadros, 20 passos): **M4 Pro 20c / 24 GB = 2761 s (~46 min) por clipe**. Um M4 base com 16–24 GB fica ainda pior.
- Opções que existem: **Draw Things** (Wan 2.1/2.2, LTX), `james-see/ltx-video-mac` (MIT, LTX-2/2.3/2.5 nativo), `rinste/turbo-mlx`, `mflux` (MLX), ComfyUI em MPS, `antirez/h3.c` (Metal). O **Wan 2.2 5B ou o 1.3B com LoRA de 4 passos** em 480p é o único cenário "aceitável": ~5–15 min por clipe ⚠️.
- **Papel sugerido para o Mac:** roteiro, geração dos **stills** (ou receber os stills prontos), revisão e curadoria dos clipes, edição (DaVinci/Final Cut), narração/TTS e **disparo da fila do ComfyUI na 5090 pela rede** (API em `http://IP-DA-5090:8188`).

---

## 7. Stack recomendada (5090 desktop, 24/7)

### 7.1 Motores
1. **Principal (I2V dos seus stills):** **Wan 2.2 I2V A14B**, high+low noise em fp8_scaled (ou NVFP4), + **LoRA LightX2V 4-step 720p (260412)** + SageAttention. Template oficial: **`video_wan2_2_14B_i2v`** ✅. Se precisar de transição controlada entre dois stills: **`video_wan2_2_14B_flf2v`** ✅.
2. **T2V (planos de cobertura, b-roll):** **`video_wan2_2_14B_t2v`** ✅ + LoRA LightX2V T2V 4-step.
3. **Rascunho rápido e 720p a 24 fps nativo:** **`video_wan2_2_5B_ti2v`** ✅ (+ Turbo de 4 passos).
4. **Segundo motor permissivo (MIT), para variedade de estilo e planos longos:** **LongCat-Video**, via Wan2GP ou LightX2V.
5. **Opcional, se quiser áudio ambiente nativo e aceitar a licença (receita < US$ 10M):** **LTX-2.5**, templates `video_ltx2_5_i2v` / `video_ltx2_5_t2v` / `video_ltx2_5_dfr_i2v` ✅.
6. **Câmera (pan/dolly/órbita):** `video_wan2_2_14B_fun_camera` ✅.
7. **Pós-produção:** `utility_seedvr2_3b_int8_upscale_video` ✅ + RIFE (ComfyUI-Frame-Interpolation).

### 7.2 Instalação passo a passo (Windows ou Linux; Linux rende mais para 24/7)

```bash
# 0) Driver NVIDIA recente (CUDA 13), Python 3.11/3.12, git, ffmpeg
# 1) ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI && cd ComfyUI
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
pip install -r requirements.txt
# 2) Custom nodes
cd custom_nodes
git clone https://github.com/Comfy-Org/ComfyUI-Manager
git clone https://github.com/kijai/ComfyUI-WanVideoWrapper
git clone https://github.com/kijai/ComfyUI-KJNodes
git clone https://github.com/city96/ComfyUI-GGUF
git clone https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler
git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
git clone https://github.com/princepainter/ComfyUI-PainterI2V     # corrige a câmera lenta dos LoRAs 4-step
for d in */; do [ -f "$d/requirements.txt" ] && pip install -r "$d/requirements.txt"; done
cd ..
# 3) SageAttention (build para sm_120 / cu130; use uma wheel que case com a versão do torch)
pip install triton  # Windows: triton-windows
pip install sageattention   # ou compile SageAttention 2/3 do repositório thu-ml/SageAttention
# 4) Rodar
python main.py --listen 0.0.0.0 --use-sage-attention
```

**Modelos** (estrutura `ComfyUI/models/...`; o *Manager → Model Manager* ou o próprio template baixa automaticamente):
- `diffusion_models/`: `wan2.2_i2v_high_noise_14B_fp8_scaled`, `wan2.2_i2v_low_noise_14B_fp8_scaled`, os equivalentes `t2v_*`, `wan2.2_ti2v_5B_fp16`
- `text_encoders/`: `umt5_xxl_fp8_e4m3fn_scaled`
- `vae/`: `wan_2.1_vae` (para o 14B) **e** `wan2.2_vae` (para o 5B)
- `clip_vision/`: `clip_vision_h` (se o workflow pedir)
- `loras/`: `wan2.2_i2v_A14b_high_noise_lightx2v_4step_720p_260412` + `..._low_noise_...` (de `lightx2v/Wan2.2-Distill-Models`) e os LoRAs T2V 4-step
- SeedVR2: o nó baixa o 3B (int8/fp8) na primeira execução.
- Espaço total: ~120–180 GB só para a stack Wan. LTX-2.5 acrescenta ~66 GB.

**Configuração inicial do I2V 14B (4 passos):** 1280×720 (ou 832×480 para rascunho), **81 quadros** (5 s a 16 fps), 2+2 passos (high→low), **CFG 1**, sampler `euler`/`lcm`, shift 5–8, LoRA com força 1,0. Para 10 s, gere 2 clipes e **encadeie pelo último quadro** (I2V a partir do último frame, ou FLF2V).

### 7.3 Farm 24/7
- Uma instância do ComfyUI com `--listen`. Um script em Python lê um CSV/JSON (still, prompt, seed, duração), envia o workflow (exportado em **"Save (API format)"**) para `POST /prompt` e acompanha o progresso por `/ws` e `/history`. Depois move o MP4 para `out/AAAA-MM-DD/`.
- Duas filas: (1) **geração** em 480p ou 720p; (2) **pós** com SeedVR2 + RIFE, rodando em lote à noite ou intercalada. Agrupar por modelo evita recarregar pesos.
- Alternativa sem código: **Wan2GP** em modo headless/fila (aceita lote por linha de comando e tem API).
- Cuidados para 24/7: limite de potência de ~450–500 W (`nvidia-smi -pl 480`) perde pouca velocidade e reduz calor. Monitore a temperatura da VRAM (GDDR7) e reinicie o ComfyUI a cada N jobs, porque há fragmentação de memória e vazamento de RAM pinada 🟡. No Windows, use `--disable-pinned-memory` se a RAM for pouca.
- **Custo de energia** ⚠️: ~0,55–0,6 kW × 24 h ≈ 13–14 kWh/dia, ou **~R$ 300–450/mês** em tarifa residencial brasileira. "Grátis" vale para licença, não para energia.

---

## 8. Estimativa de produção (5090 desktop 32 GB) ⚠️

Ponto de partida medido 🟡: numa **5090 Laptop 24 GB** (TGP muito menor que a desktop, com offload), Wan 2.2 14B em 832×480×81 quadros e 4 passos levou **93,8 s**. A 5090 desktop costuma ser **~1,5–1,8×** mais rápida que a versão laptop (estimativa minha, não medida), e com 32 GB precisa de menos offload.

| Cenário (clipe de 5 s) | Tempo/clipe estimado ⚠️ | Clipes/hora | Clipes/dia 24/7 |
|---|---|---|---|
| Wan 2.2 14B I2V, 480p, 4 passos, fp8 + Sage | ~55–70 s | **50–65** | ~1200–1500 |
| Idem + SeedVR2 3B (→1080p) + RIFE | ~150–240 s | **15–24** | ~360–570 |
| Wan 2.2 14B I2V, **720p nativo**, 4 passos | ~150–220 s | **16–24** | ~400–570 |
| Idem com **NVFP4-Sparse (LightX2V)** | ~60–100 s (se o ganho anunciado se confirmar) | 35–60 | ~850–1400 |
| Wan 2.2 5B TI2V, 720p a 24 fps, ~20–30 passos | ~200–250 s | 14–18 | ~350–430 |
| Wan 2.2 14B, 720p, **20 passos sem LoRA** (qualidade máxima) | ~15–25 min | 2–4 | ~50–90 |
| Clipe de 10 s (2 × 5 s encadeados) | 2× o valor da linha | metade | metade |

**Número para planejamento:** **~15–20 clipes finalizados de 5 s por hora em 1080p** (geração em 480p ou 720p + upscale), ou seja **~350–450 por dia**. Isso dá ~30–37 min de material bruto por dia. Na prática, considere **descartar 30–50%** na curadoria. Faça o seu próprio benchmark na primeira semana, porque a variação entre drivers e versões é grande.

---

## 9. O que **não** usar e por quê
- **Wan 2.5+/LTX "API", Hunyuan via API, H3 Max:** pagos ou fechados.
- **HunyuanVideo / FramePack / SkyReels V1 / MiniMax H3** como motor principal: risco territorial ao exibir no YouTube (ver 2.2).
- **CogVideoX 1.5, Mochi 1, Open-Sora 2.0, Step-Video, MAGI-1 24B:** gerações anteriores, resolução baixa ou VRAM incompatível. O Wan 2.2 é superior em tudo.
- **LTX-Video 2B (0.9.x):** rápido, mas **ignorou o prompt** em teste controlado 🟡. Se quiser LTX, use 2.3/2.5.
- **CausVid LoRA:** licença não verificada. O LightX2V cobre o mesmo uso.

## 10. Próximos passos sugeridos
1. Instalar a stack da seção 7.2 e rodar `video_wan2_2_14B_i2v` com o LoRA 4-step 720p em 10 stills reais do canal. Medir s/clipe.
2. Comparar fp8 × NVFP4-Sparse (LightX2V) e 480p+SeedVR2 × 720p nativo, avaliando qualidade e tempo.
3. Testar LongCat-Video (MIT) como 2º estilo.
4. Ler e arquivar (PDF + data) os LICENSEs no HF: Wan2.2, LightX2V LoRAs, LongCat, Kandinsky 5, SeedVR2 e, se for usar, LTX-2.5.
5. Montar o script de fila pela API do ComfyUI e definir o processo de curadoria.

---
### Fontes (GitHub)
- Wan-Video/Wan2.1, Wan-Video/Wan2.2 (Apache-2.0; README)
- Comfy-Org/workflow_templates `templates/index.json` (nomes dos templates)
- comfyanonymous/ComfyUI README (cu130 obrigatório)
- lifeidle/comfyui-5090-laptop-24gb-minimax-h3-qwen-image-wan2.2 (benchmarks medidos numa 5090 Laptop, matriz de licenças)
- Lightricks/LTX-2 (README, LICENSE, LICENSE-2, LICENSE-2_x)
- Tencent-Hunyuan/HunyuanVideo-1.5 (LICENSE, README)
- meituan-longcat/LongCat-Video (README: pesos MIT)
- kandinskylab/kandinsky-5, SandAI-org/MAGI-1, hpcaitech/Open-Sora, zai-org/CogVideo, genmoai/mochi, lllyasviel/FramePack, SkyworkAI/SkyReels-V1/V2/V3, stepfun-ai/Step-Video-*
- ModelTC/LightX2V (README, scripts/wan22/README.md), guandeh17/Self-Forcing, ali-vilab/TeaCache, thu-ml/SageAttention, city96/ComfyUI-GGUF, kijai/ComfyUI-WanVideoWrapper
- deepbeepmeep/Wan2GP (README, LICENSE.txt), mcmonkeyprojects/SwarmUI, pinokiocomputer/pinokio
- MiniMax-AI/MiniMax-H3, MiniMax-AI/awesome-minimax-h3-integration (docs/run-h3-locally.md), FlashML-org/FreeVideo
- xinntao/Real-ESRGAN, hzwer/ECCV2022-RIFE, ByteDance-Seed/SeedVR, numz/ComfyUI-SeedVR2_VideoUpscaler, Fannovel16/ComfyUI-Frame-Interpolation
