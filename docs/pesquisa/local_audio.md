# Música e SFX locais, grátis e com uso comercial (substituto do ElevenLabs Music/SFX)

Data da pesquisa: 15/11/2026. Hardware alvo: PC com RTX 5090 (32 GB) + Mac M4.

> **Método e limites:** a cota de WebSearch estava esgotada e o huggingface.co está bloqueado neste ambiente. Todas as licenças abaixo foram lidas direto dos arquivos LICENSE/README nos repositórios do GitHub (raw.githubusercontent.com). Model cards do Hugging Face **não** puderam ser abertos. Itens marcados **(verificar)** dependem do model card no HF: confira antes de usar em produção. Isto não é parecer jurídico.

---

## 1. Resumo da recomendação

| Uso | Ferramenta principal | Licença (código / pesos) | Por quê |
|---|---|---|---|
| **Trilhas cinematográficas, noir, tensão, épico** (RTX 5090) | **ACE-Step 1.5 XL (sft/turbo)** | MIT / MIT (repo; pesos no HF **(verificar)**) | Tem modo instrumental, de 10 s a 10 min, BPM/tom/compasso controláveis, repaint/extend, LoRA, suporte nativo no ComfyUI e roda no Mac (MLX) |
| Segunda opção de música | **DiffRhythm / DiffRhythm 2** | Apache 2.0 / Apache 2.0 (escrito no README) | Código e pesos explicitamente Apache; até 4m45s |
| Terceira opção de música | **HeartMuLa-oss-3B** | Apache 2.0 / Apache 2.0 (desde 20/01/2026) | Licença limpa; qualidade alta, mas focado em canções com letra; RTF ≈ 1 (lento) |
| **SFX, foley, ambiências, loops curtos** | **Stable Audio 3 (Small-SFX / Medium)** | MIT / Stability AI Community License | Rapidíssimo, até 120 s (Small) e 380 s (Medium), roda em CPU/Mac. Comercial grátis **enquanto a receita anual ficar abaixo de US$ 1 milhão** |
| Pads e drones de ambiência | Stable Audio 3 Small-Music / Medium | MIT / Stability Community | Ótimo para camadas de textura, risers e drones |
| Foley sincronizado com vídeo | Nenhum modelo 100% livre. A menos restritiva é **HunyuanVideo-Foley**, com ressalva grave (ver §3) | – | MMAudio, ThinkSound, AudioX e Woosh usam pesos não comerciais |

**Stack sugerido:** ComfyUI (no PC) com ACE-Step 1.5 nativo, mais Stable Audio 3 via CLI/Gradio ou nós de ComfyUI. No Mac M4: ACE-Step 1.5 (MLX) e Stable Audio 3 (MLX/CoreML) para rascunhos e SFX rápidos.

---

## 2. Modelos de música, um a um

| Modelo | Código | Pesos | Comercial? | VRAM | Velocidade | Duração máx. | Instrumental cinematográfico | ComfyUI |
|---|---|---|---|---|---|---|---|---|
| **ACE-Step 1.5** (2B turbo/sft, XL 4B desde 02/04/2026) | MIT | MIT no repo (HF **verificar**) | ✅ Sim | 2B: 6–16 GB; XL sem offload: ≥20 GB; com o LM de 4B o ideal é ≥24 GB → a 5090 roda tudo | Muito rápida (o v1 já fazia 1 min de áudio em cerca de 2 s numa A100; o 1.5 turbo é ainda mais rápido) | **600 s (10 min)** | Muito bom (o README o coloca "entre Suno v4.5 e v5"). Instrumental e controle de BPM e tom | ✅ **Nativo no core** + ComfyUI-AceMusic, ACE-Step-ComfyUI (oficial), JK-AceStep-Nodes |
| ACE-Step v1 (3.5B) | Apache 2.0 | Apache 2.0 | ✅ | ~8 GB | RTF 27x (A100), 2,27x (M2 Max) | ~4 min | Bom, mas superado pelo 1.5 | ✅ (billwuhao/ComfyUI_ACE-Step) |
| **DiffRhythm v1.2 / DiffRhythm 2** | Apache 2.0 | **Apache 2.0** ("code and DiT weights") | ✅ | ≥8 GB (`--chunked`) | Rápido (difusão) | **285 s** | Bom para faixas completas. Instrumental é possível, mas o foco é canção | ✅ billwuhao/ComfyUI_DiffRhythm |
| **HeartMuLa-oss-3B** (happy-new-year, RL) | Apache 2.0 | **Apache 2.0** (atualizado em 20/01/2026) | ✅ | ~16–24 GB (3B LM + codec) | RTF ≈ 1 (tempo real) | 240 s (padrão) | Forte em canções com letra, menos em trilha | ✅ benjiyaya/HeartMuLa_ComfyUI |
| **YuE2-3B** (set/2026) | Apache 2.0 | CC BY-NC 4.0 **+ "permissão de criador individual"** | ⚠️ Pessoa física: sim, pode monetizar. **Empresa: precisa de licença** | 24 GB BF16 | Lenta (LM) | Canção completa | Qualidade de ponta (≈ Suno v5/v6), mas o foco é vocal | ✅ nativo + template oficial |
| SongGeneration (Tencent LeVo) | – | Licença própria da Tencent, que não consegui ler (repo inacessível aqui) | ❓ Evitar até verificar | ≥12 GB | Média | ~4 min | Foco em canção | ✅ smthemex/ComfyUI_SongGeneration |
| InspireMusic (Alibaba) | Apache 2.0 | ModelScope/HF **(verificar)** | ❓ | ~8–16 GB | Média | Long: vários minutos | Razoável para instrumental | parcial |
| MiniMax-Music3 (open weights) | – | "MiniMax-Music3 Community" (condicional) | ⚠️ Condicional | ~10–24 GB | Média | 360 s | Bom | via UI de terceiros |
| Stable Audio Open 1.0 / Small (2024–25) | MIT | Stability Community | ⚠️ < US$ 1 mi/ano | ~6–10 GB | Rápida | 47 s / 11 s | Médio (superado pelo SA3) | ✅ nativo |
| **Stable Audio 3** Small-Music / Medium | MIT | Stability Community | ⚠️ < US$ 1 mi/ano | Small 1,7–2,4 GB (roda em CPU); Medium 5–6,5 GB (exige Flash-Attn 2) | Absurda: 120 s em 0,8 s numa H200; 3 s no Mac via CoreML | 120 s / **380 s** | Bom para pads, drones, beds; inpaint/extend | Awesome-Stable-Audio lista nós |
| Foundation-1 (RoyalCities) | – | Stability Community | ⚠️ < US$ 1 mi | ~7 GB | ~20 it/s | 20 s | Samples e loops musicais | ✅ Saganaki22/ComfyUI-Foundation-1 |
| MusicGen / MAGNeT / JASCO (Meta AudioCraft) | MIT | **CC-BY-NC 4.0** | ❌ Não | – | – | – | – | – |

### Observações de qualidade para trilhas "dark cinematic / noir / epic history"
- No ACE-Step 1.5, use tags como `instrumental, cinematic, dark orchestral, low strings, taiko, brass swells, tension, 70 BPM, D minor`, ative o modo instrumental e deixe a letra vazia ou `[instrumental]`. Gere de 4 a 8 seeds e escolha a melhor. Use **repaint** para consertar trechos e **extend** para chegar à duração do vídeo.
- **LoRA de estilo:** com cerca de 8 faixas *suas* (ou sob licença CC0/comprada com direito de treino) e 1 h numa 3090, você ganha uma "assinatura sonora" do canal. Na 5090 sai ainda mais rápido.
- Noir: `jazz noir, muted trumpet, upright bass, brushed drums, smoky, rain`. Ambient: `dark ambient drone, evolving pads, sub bass`. Para isso o Stable Audio 3 Medium costuma ser melhor e mais rápido.

---

## 3. SFX / foley

| Modelo | Código | Pesos | Comercial? | VRAM | Duração | Notas | ComfyUI |
|---|---|---|---|---|---|---|---|
| **Stable Audio 3 Small-SFX / Medium** | MIT | Stability Community | ⚠️ < US$ 1 mi | 1,7–6,5 GB | 120 s / 380 s | Melhor opção prática. Loops sem emenda, inpaint e prompt negativo ("music, melody") | via Awesome-Stable-Audio, MCPs |
| Stable Audio Open 1.0 | MIT | Stability Community | ⚠️ < US$ 1 mi | ~8 GB | 47 s | Bom e consolidado | ✅ nativo |
| **HunyuanVideo-Foley** (XL/XXL, vídeo→áudio) | Tencent Hunyuan Community | idem | ⚠️ Comercial liberado abaixo de 100 mi de MAU, **MAS** a licença **não vale na UE, no Reino Unido e na Coreia do Sul** e proíbe "exibir Output fora do Território". Um vídeo no YouTube aparece na UE, então há **risco contratual**. A Tencent "não reivindica direitos sobre Outputs" | XXL 20 GB (12 GB com offload); XL 16/8 GB | Clipes de vídeo | Melhor foley sincronizado aberto | ✅ if-ai/ComfyUI_HunyuanVideoFoley, phazei/... |
| MMAudio (Sony/UIUC) | MIT | **CC-BY-NC 4.0** | ❌ | ~6 GB | 8 s | Excelente, mas não comercial | ✅ |
| ThinkSound (Alibaba) | Apache 2.0 | Apache, porém o README diz **"Commercial use is NOT permitted"** e o VAE é Stability | ❌ | – | – | – | – |
| AudioX | – | **CC-BY-NC** + marca d'água | ❌ | – | 10 s | – | – |
| Woosh (Sony AI, 2026) | MIT | **CC-BY-NC** | ❌ | – | – | – | ✅ ilisin/ComfyUI-Woosh |
| AudioLDM2 | – | **CC BY-NC-SA 4.0** | ❌ | ~8 GB (Mac ~20 GB RAM) | – | – | – |
| Tango 2 / TangoFlux | – | CC BY-NC-ND / "research-only" + Stability + WavCaps (só acadêmico) | ❌ | – | 30 s | – | ✅ (mas não serve) |

**Conclusão SFX:** use o **Stable Audio 3** para tudo que for gerado por texto. Para foley sincronizado, gere SFX por texto e sincronize na edição (DaVinci/Premiere). Isso é mais seguro que o HunyuanVideo-Foley por causa da cláusula territorial. Complemente com bibliotecas CC0 (Freesound filtrado por CC0, Sonniss GDC bundles, que são royalty-free) para impactos e whooshes clássicos.

### Sobre a Stability AI Community License
- Grátis para uso comercial por pessoa física ou empresa com **receita anual total abaixo de US$ 1 milhão** (contando todas as fontes, não só o YouTube). Acima disso, é preciso uma licença Enterprise.
- Os outputs são seus. É obrigatório exibir "Powered by Stability AI" quando você **distribui o modelo ou um derivado**. Para outputs isso não se aplica, mas confira o texto em stability.ai/license **(verificar)**.
- Se o canal passar de US$ 1 mi/ano, troque o SA3 por ACE-Step/DiffRhythm (música) e bibliotecas CC0 (SFX).

---

## 4. Content ID: risco de falso positivo com música de IA

**Riscos reais:**
1. **Terceiros registrando música de IA parecida ou idêntica.** O maior vetor de reivindicações falsas hoje são pessoas que sobem faixas geradas por IA (ou loops e samples públicos) a distribuidoras (DistroKid, TuneCore etc.) com Content ID ativado. Se o seu bed usar um loop, sample ou progressão muito genérica que coincida, pode haver claim.
2. **Memorização.** Modelos treinados com música protegida podem, raramente, reproduzir trechos reconhecíveis. O risco é maior com prompts que citam artistas ou faixas famosas e com o modo "cover/audio2audio" sobre músicas de terceiros.
3. **Drones e ambiências muito simples** têm pouca "impressão digital", então a chance de match é baixa, mas não nula, quando alguém registra uma textura parecida.
4. **Direito autoral:** obra 100% gerada por IA, sem autoria humana relevante, em geral **não é protegível** (US Copyright Office; a LDA brasileira exige autor pessoa física). Na prática você **não consegue registrar** essas faixas no Content ID de forma legítima, e também não deve.

**Boas práticas:**
- **Nunca** suba suas faixas geradas a distribuidoras ou ao Content ID. Isso gera claims contra você mesmo e contra outros e viola as regras do YouTube para material não exclusivo.
- **Guarde um log de geração** por faixa: modelo + versão + hash SHA-256 dos pesos, prompt, prompt negativo, seed, steps, CFG, data/hora, WAV original sem edição e o projeto de edição. Um CSV/JSON por faixa numa pasta `audio_provenance/` basta. Esse é o seu dossiê para contestar um claim.
- Não cite artistas, músicas ou trilhas famosas no prompt ("estilo Hans Zimmer – Time"). Descreva instrumentação, andamento e clima.
- Não use cover/audio2audio/remix sobre música de terceiros. Para referência, use só material próprio ou CC0.
- **Pós-processe e misture:** corte, EQ, reverb, mixagem com narração e SFX. Isso cria uma obra derivada com contribuição humana e reduz matches exatos.
- Antes de publicar, suba o vídeo como **não listado/privado** e espere a checagem de direitos autorais do YouTube Studio ("Verificações"). Se aparecer claim, conteste com o log.
- Mantenha uma **biblioteca interna** de faixas aprovadas e reutilize as que já passaram em vídeos anteriores sem claim.
- Divulgação de IA: o rótulo "conteúdo alterado ou sintético" do YouTube é exigido para conteúdo **realista** (pessoas, eventos, lugares). Trilha de fundo em geral não exige, mas conte a política vigente.
- Prefira modelos com licença limpa (MIT/Apache) para o catálogo principal. Isso evita disputa de licença de pesos se o canal crescer.

---

## 5. Instalação

### 5.1 PC RTX 5090 (Windows ou Linux)
A 5090 (Blackwell, sm_120) exige **PyTorch com CUDA 12.8+** (cu128 ou mais novo). Builds antigas não reconhecem a GPU.

**ComfyUI + ACE-Step 1.5 nativo**
```bash
git clone https://github.com/comfyanonymous/ComfyUI && cd ComfyUI
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
python main.py
# Em Workflow > Templates > Audio: "ACE-Step 1.5" (baixa os .safetensors para models/)
# Opcional: ComfyUI-Manager e instale "ComfyUI-AceMusic" (repaint/extend/LoRA)
```
Tutorial oficial: docs.comfy.org (ACE-Step 1.5 Guide). Alternativa portátil: `timoncool/ACE-Step-Studio`.

**ACE-Step 1.5 standalone (Gradio/API)**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/ace-step/ACE-Step-1.5 && cd ACE-Step-1.5
uv sync            # Python 3.11–3.12
# start_gradio_ui.sh (ou .bat). Na 5090: DiT XL sft + LM acestep-5Hz-lm-4B, backend vllm
```

**Stable Audio 3 (SFX/ambiência)**
```bash
git clone https://github.com/Stability-AI/stable-audio-3 && cd stable-audio-3
uv sync             # Medium exige flash-attention 2 (wheel compatível com cu128/sm_120 ou compilar)
huggingface-cli login   # pesos "gated": aceite a licença no HF
uv run python run_gradio.py --model medium
# CLI: stable-audio --model small-sfx -p "heavy wooden door creak, old mansion, reverb" --duration 6 -o door.wav
```

**DiffRhythm (opcional)**
```bash
git clone https://github.com/ASLP-lab/DiffRhythm && cd DiffRhythm
pip install -r requirements.txt   # + espeak-ng
# ou no ComfyUI: billwuhao/ComfyUI_DiffRhythm
```

### 5.2 Mac M4
```bash
# ACE-Step 1.5 (MLX)
git clone https://github.com/ace-step/ACE-Step-1.5 && cd ACE-Step-1.5
chmod +x start_gradio_ui_macos.sh && ./start_gradio_ui_macos.sh
# (ou o pacote portátil para macOS citado no README)

# Stable Audio 3 em Metal/MLX
curl -LsSf https://raw.githubusercontent.com/Stability-AI/stable-audio-3/main/optimized/mlx/bootstrap.sh | bash
```
Recomendação: 16 GB+ de RAM unificada. No Mac, use 2B turbo para o ACE-Step e Small para o SA3. Deixe o XL e o Medium para a 5090.

### 5.3 Opcionais úteis
- **Soundbox** (`HamSanders/soundbox`, MIT): app local com SA3 SFX/Music, ACE-Step 1.5 e HeartMuLa. Mostra a licença de cada modelo antes de baixar.
- **audio-studio-mcp** (MIT): MCP para o Claude Code gerar BGM/SFX com SA3 no Mac/Windows, com loops sem emenda e normalização LUFS.
- Pós-produção: normalize beds de fundo para cerca de −24 a −20 LUFS sob a narração (YouTube normaliza o master em ~−14 LUFS). Use ducking por sidechain.

---

## 6. Checklist rápido de licença por ferramenta
- ✅ Livre para comercial: **ACE-Step 1.5 (MIT)**, **ACE-Step v1 (Apache)**, **DiffRhythm 1/2 (Apache, inclusive pesos)**, **HeartMuLa (Apache, inclusive pesos)**.
- ⚠️ Comercial com condição: **Stable Audio 3 / Open / Foundation-1** (receita < US$ 1 mi), **YuE2** (só pessoa física), **MiniMax-Music3** (condicional), **HunyuanVideo-Foley** (território exclui UE/Reino Unido/Coreia, o que é problemático para o YouTube).
- ❌ Não comercial: MusicGen/MAGNeT/JASCO, MMAudio (pesos), ThinkSound, AudioX, Woosh, AudioLDM2, Tango/TangoFlux.
- ❓ Verificar: SongGeneration/LeVo, InspireMusic (pesos), model card do ACE-Step 1.5 no HF.
