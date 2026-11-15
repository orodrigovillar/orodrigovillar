# TTS local, gratuito e com licença comercial para substituir o ElevenLabs

**Caso de uso:** narração de documentários longos no YouTube (20–30 min por vídeo), primeiro em inglês e depois em português do Brasil, com voz masculina grave e cinematográfica.
**Hardware:** PC com RTX 5090 (32 GB, Blackwell sm_120) e Mac M4 (MLX).
**Data da pesquisa:** 15/11/2026.

> **Como verifiquei as informações.** As licenças e os dados técnicos vêm dos README e LICENSE oficiais no GitHub (lidos via raw.githubusercontent) e dos metadados de repositório da API de busca do GitHub. **O huggingface.co estava bloqueado neste ambiente**, então não consegui ler os *model cards*. Em todo lugar marcado com **(verificar no HF)**, a licença dos pesos vem de memória ou do que o README afirma. Antes de monetizar, abra o model card e salve um print ou PDF da licença com data, como prova de diligência.
>
> **O cenário mudou muito em 2026.** O Chatterbox foi aposentado em agosto de 2026, mas continua MIT. O Higgs Audio v3 é não comercial. A Fish Audio trocou de licença em out/2026. Surgiram opções Apache-2.0 fortes com PT-BR: **VoxCPM2**, **Qwen3-TTS**, **OmniVoice** e **MOSS-TTS v1.5**. Elas passam a ser as melhores escolhas.

---

## 1. Resumo executivo / shortlist ranqueada

### Inglês (top 3)
| # | Modelo | Licença do código / dos pesos | Por quê |
|---|---|---|---|
| 1 | **VoxCPM2 (OpenBMB, 2B)** | Apache-2.0 / Apache-2.0 (o README diz que é "free for commercial use") | Áudio de 48 kHz nativo. Tem *Voice Design* (cria a voz a partir de uma descrição, sem pessoa real), clonagem controlável (emoção e ritmo) e fine-tune LoRA. Usa ~8 GB de VRAM, com RTF ~0,30 numa 4090 (~0,13 com Nano-vLLM). Funciona no Mac via MLX e GGUF. |
| 2 | **Qwen3-TTS 1.7B (Alibaba)** | Apache-2.0 / Apache-2.0 (verificar no HF) | Faz *VoiceDesign* e depois *Clone* (fluxo oficial para manter uma voz "de marca" consistente). Aceita instruções em linguagem natural ("grave, lento, tom de documentário"). Tem servidor vLLM, nós de ComfyUI e porta MLX. |
| 3 | **IndexTTS-2.5 (bilibili)** | bilibili Model Use License (código e pesos) | É o mais expressivo e controlável em emoção (vetor de emoção, `emo_text`, `emo_alpha`), com controle de duração e RTF ~0,20 numa 4090. O uso comercial é **permitido sem pedir licença**, desde que você tenha **menos de 100 milhões de MAU e menos de RMB 1 bi de receita/ano**. **Não fala PT.** |

Alternativas em inglês. **Chatterbox-Turbo** (MIT, tags `[laugh]`, leve, mas sem manutenção desde ago/2026). **MOSS-TTS v1.5** (Apache-2.0, feito para narração longa de "dezenas de minutos", modelo de 8B). **Fish Audio Drama 3**, provavelmente o de maior qualidade, mas com licença condicionada (ver a tabela).

### Português do Brasil (top 3)
| # | Modelo | Por quê |
|---|---|---|
| 1 | **VoxCPM2** | Lista "Portuguese" entre as 30 línguas. Áudio de 48 kHz, Voice Design e LoRA para fixar a voz da marca. Apache-2.0. |
| 2 | **Qwen3-TTS 1.7B** | Português entre as 10 línguas principais. Instruções de estilo e o fluxo Design para Clone. Apache-2.0. |
| 3 | **Chatterbox Multilingual V3 + pacote "pt-br"** | Tem um *finetune dedicado de PT-BR* (`ResembleAI/Chatterbox-Multilingual-pt-br`). Licença MIT. Sem manutenção, mas estável e fácil de instalar. Inclui marca d'água PerTh (não tem problema para o YouTube). |

Alternativas em PT-BR. **OmniVoice** (k2-fsa, Apache-2.0, mais de 600 línguas, RTF de 0,025, melhor no modo de clonagem). **MOSS-TTS v1.5** (Apache-2.0, PT, narração longa). **Fish Drama 3** (83 línguas, com a ressalva de licença). **KugelAudio** (MIT, 7B, ~19 GB, foco europeu; o PT tende a soar europeu).

**Recomendação prática:** padronize em **VoxCPM2** nas duas línguas e use o **Qwen3-TTS** como segunda opção para comparação A/B. Crie a voz da marca com *Voice Design* (sem pessoa real) ou com um dublador contratado (ver a seção 4) e fixe-a com um clipe de referência mais um LoRA.

---

## 2. Tabela comparativa (todos os modelos pedidos e os novos relevantes)

Legenda de uso comercial: ✅ permitido · ⚠️ permitido com condições · ❌ não comercial (NC) ou inviável.

| Modelo | Licença do CÓDIGO | Licença dos PESOS | Comercial | PT-BR | Clonagem | Texto longo | Tags/emoção | VRAM | Manutenção (último push no GitHub) |
|---|---|---|---|---|---|---|---|---|---|
| **VoxCPM2** (OpenBMB) | Apache-2.0 | Apache-2.0 | ✅ | ✅ (30 línguas) | ✅ + controle de estilo | Bom com streaming; fatiar por parágrafo | Instrução entre parênteses "(deep, slow...)" | ~8 GB | Ativo (nov/2026), 42k★ |
| **Qwen3-TTS** 0.6B/1.7B | Apache-2.0 | Apache-2.0 (verificar no HF) | ✅ | ✅ (10 línguas) | ✅ em 3 s; VoiceDesign | Fatiar; streaming | `instruct` em linguagem natural | ~4–8 GB (est.) | Último push em mar/2026, 14k★; ecossistema ativo (faster-qwen3-tts, ComfyUI, MLX) |
| **OmniVoice** (k2-fsa) | Apache-2.0 | Apache-2.0 (verificar no HF) | ✅ (verificar dados de treino) | ✅ (600+) | ✅ (modo mais estável) | Fatiar; referência de 3–10 s | `[laughter]`, fonemas | Baixa (roda em GPU de 4 GB) | Ativo (nov/2026), 16k★ |
| **MOSS-TTS v1.5** (OpenMOSS) | Apache-2.0 | Apache-2.0 | ✅ | ✅ (31 línguas) | ✅ | **Projetado para "dezenas de minutos"** | Voice design, duração | 8B (GGUF cabe em 8 GB) | Ativo (set/2026) |
| **Chatterbox** (Resemble) Turbo / Multilingual V3 / pt-br | MIT | MIT (verificar no HF) | ✅ | ✅ (pacote pt-br dedicado) | ✅ | Fatiar (Chatterbox-TTS-Server faz isso) | Turbo: `[laugh]` etc.; `exaggeration`, `cfg_weight` | ~4–7 GB | **Aposentado em ago/2026** (arquivo MIT, sem suporte) |
| **IndexTTS-2 / 2.5** (bilibili) | bilibili Model Use License | idem | ⚠️ (bloqueio só acima de 100M MAU ou RMB 1 bi) | ❌ (zh, en, ja, es, ar) | ✅ | Bom | **Melhor controle de emoção** | ~8–12 GB (est.) | Ativo (set/2026) |
| **Fish Audio Drama 3 / S2-Pro** | Fish Audio Community License (out/2026) | Drama 3: Community. **S2-Pro: Research License (NC)** | ⚠️ Drama 3: só com **receita anual abaixo de US$ 500 mil** (do grupo econômico todo). Proíbe *hosted service*, usar saídas para treinar modelos e remover marca d'água | ✅ (83 línguas) | ✅ | **Excelente** (streaming longo, edição de palavra) | `[whisper]`, `[angry]`, revisão "de diretor" | Drama 3 é MoE 35B (3B ativos): na 5090 só quantizado (~4 bits, ~20 GB est.) | Muito ativo |
| **Higgs Audio v2 / v2.5** (Boson) | Apache-2.0 | "Boson Higgs Audio 2 Community License" (verificar no HF; de memória: comercial até ~100k usuários ativos/ano) | ⚠️ | ❌ oficial (EN, ZH, KO, DE, ES) | ✅ | Bom, prosódia adaptativa | Sim | ≥24 GB recomendados | v2 legado |
| **Higgs Audio v3** | (standalone) | **Research & Non-Commercial** | ❌ | 100+ | ✅ | — | Sim | 4B | Ativo, mas NC |
| **F5-TTS** (SWivid) | MIT | **CC-BY-NC** (dataset Emilia) | ❌ | Finetunes comunitários PT-BR herdam o NC | ✅ | Fatiar | Não | ~3–6 GB | Ativo |
| **XTTS-v2** (Coqui) | MPL-2.0 (fork idiap) | **Coqui Public Model License (NC)** | ❌ (a Coqui fechou e não há como comprar licença) | ✅ | ✅ | Fraco em textos longos | Não | ~4 GB | Só o fork comunitário |
| **Spark-TTS** | Apache-2.0 | **CC-BY-NC-SA 4.0** (verificar no HF) | ❌ | ❌ (zh/en) | ✅ | — | Atributos (tom, velocidade) | ~4 GB | Parado desde abr/2025 |
| **MegaTTS3** (ByteDance) | Apache-2.0 | Apache-2.0, mas o **encoder WaveVAE não foi publicado** (só latentes pré-extraídos) | ⚠️ na prática (não clona voz própria) | ❌ (zh/en) | Limitada | — | — | ~6 GB | Pouco ativo |
| **Orpheus TTS** (Canopy) | Apache-2.0 | Base Llama-3.2 → **Llama 3.2 Community License** (verificar no HF) | ⚠️ (atribuição "Built with Llama"; limite de 700M MAU) | ❌ (multilíngue em research preview, sem PT) | Fine-tune | Médio | `<laugh>`, `<sigh>` | ~8–16 GB (3B) | Parado (dez/2025) |
| **Dia 1.6B** (Nari) | Apache-2.0 | Apache-2.0 | ✅ | ❌ (EN) | ✅ (áudio de prompt) | **Ruim**: mais de ~20 s fica acelerado | `(laughs)` etc. | ~4,4 GB (bf16); RTF x2,1 numa 4090 | Parado (nov/2025) |
| **Sesame CSM-1B** | Apache-2.0 | Apache-2.0 (verificar no HF) | ✅ | ❌ (o próprio README diz que outras línguas "likely won't do well") | ✅ (contexto) | Fraco para narração | Conversacional | ~4–6 GB | Parado (mai/2025) |
| **Zonos v0.1** (Zyphra) | Apache-2.0 | Apache-2.0 | ✅ | ❌ (en, ja, zh, fr, de) | ✅ | Médio | Vetor de emoção | ~6 GB | Parado (mar/2025) |
| **ZONOS3-Mini** (Zyphra, nov/2026) | MIT | MIT (verificar no HF) | ✅ | Multilíngue (lista não verificada) | ✅ + voice design | Alinhamento de texto longo | Sim | ~9 GB de pesos | **Novíssimo** (nov/2026); launcher Pinokio |
| **CosyVoice 2 / Fun-CosyVoice 3** | Apache-2.0 | Apache-2.0 (verificar no HF) | ✅ | ❌ (9 línguas, sem PT) | ✅ | Bom | `instruct`, `[laughter]` | ~6–8 GB | Moderado |
| **VibeVoice** (Microsoft) | MIT | MIT, mas **"research only"** segundo a própria MS; modelo Large **desativado "due to widespread misuse"** | ⚠️ (desaconselhado) | ❌ (EN/ZH; "outras línguas podem dar saída inesperada") | ✅ | Até 90 min de uma vez (1.5B) | Implícito | ~7–18 GB | O TTS foi abandonado; foco atual em ASR |
| **KugelAudio-0-open** (base VibeVoice) | MIT | MIT | ✅ | PT (europeu; qualidade varia) | ✅ | Bom | — | ~19 GB; RTF 1,0 | Ativo (set/2026) |
| **Kyutai TTS 1.6B** (delayed-streams) | MIT/Apache | CC-BY-4.0 (verificar no HF) | ✅ com atribuição | ❌ (en/fr) | Só vozes do catálogo (encoder de voz não liberado) | Streaming | — | ~4–6 GB | Moderado |
| **Kyutai Pocket TTS** | MIT | (verificar no HF; de memória CC-BY-4.0) | ✅ provável | ✅ (inclui português) | ✅ | OK | — | Roda em CPU | Ativo (nov/2026); qualidade abaixo do nível "cinema" |
| **StyleTTS2** | MIT | MIT, mas o README exige **avisar que a fala é sintética**, salvo autorização do falante | ✅ (com aviso) | ❌ (EN) | Limitada | Bom | Não | ~2 GB | Parado (2024) |
| **Piper** (piper1-gpl) | **GPL-3.0** (o rhasspy/piper original era MIT e foi arquivado) | Por voz (cada `.onnx` tem licença própria; algumas pt_BR são CC0/CC-BY, outras NC) | ⚠️ por voz | ✅ (vozes pt_BR) | ❌ | Estável, mas robótico | Não | CPU | Ativo; **inadequado para documentário** |
| **Kokoro-82M** | Apache-2.0 | Apache-2.0 | ✅ | ✅ só 3 vozes pt-br (pf_dora, pm_alex, pm_santa), qualidade mediana | ❌ (vozes fixas) | Muito estável e rápido | Não | ~1 GB; CPU ok | Biblioteca parada (ago/2025); Kokoro-FastAPI ativo |
| **MLX-Audio** (Mac) | MIT (repo migrou para `Neywa-Labs/mlx-audio`) | Depende do modelo | — | — | — | — | — | RAM unificada | **Muito ativo** (nov/2026); roda VoxCPM2, Qwen3-TTS, Chatterbox v3, OmniVoice, Kokoro e outros; API compatível com OpenAI |

**Não use comercialmente:** F5-TTS (pesos), XTTS-v2, Spark-TTS, Higgs v3, Fish S2-Pro. Também não use nenhum *finetune* comunitário construído sobre essas bases, porque a licença NC é herdada.

### RTF publicado (quanto menor, melhor; 0,3 = 1 min de áudio em 18 s)
- VoxCPM2: ~0,30 numa 4090 (PyTorch), ~0,13 com Nano-vLLM ou vLLM-Omni. **~1,76 no M4 Pro** (llama.cpp-omni Q8_0, ou seja, mais lento que tempo real).
- IndexTTS-2.5: 0,20 numa 4090 (bf16, kv_cache).
- OmniVoice: até 0,025 (H100, em lote).
- Fish S2-Pro: 0,195 numa H200.
- Dia: x2,1 de tempo real numa 4090 (bf16 + compile).
- **RTX 5090:** nenhum projeto publica números. Como estimativa, espere ~1,3 a 1,6 vez a velocidade da 4090. Para 30 min de narração com o VoxCPM2, isso dá **cerca de 5 a 8 min de geração**, ou menos de 4 min com o Nano-vLLM.
- **M4:** sem números oficiais para o M4 base. Espere algo entre 1 e 3 vezes o tempo real com modelos de 1,7B a 2B em 8 bits. Para 30 min de áudio, conte **~30 a 90 min** de geração. O Mac serve como segunda máquina; a 5090 é a de produção.

### Interfaces gráficas e APIs
- **Pinokio:** launchers de um clique para ZONOS3-Mini (cocktailpeanut/zonos3-mini), além de launchers comunitários para Chatterbox, IndexTTS, F5 e outros.
- **ComfyUI:** `DarioFT/ComfyUI-Qwen3-TTS`, `wildminder/ComfyUI-VoxCPM`, `HM-RunningHub/ComfyUI_RH_VoxCPM` (multi-locutor, LoRA, ASR), `Saganaki22/ComfyUI-OmniVoice-TTS`, `Saganaki22/ComfyUI-KugelAudio`.
- **WebUIs:** `rsxdalv/TTS-WebUI` (MIT, extensões para VoxCPM, OmniVoice e muitos outros); `qwen-tts-demo` (Gradio oficial); `debpalash/VoiceStudio` (AGPL-3.0, "alternativa local ao ElevenLabs"; o AGPL só pesa se você redistribuir ou hospedar para terceiros).
- **APIs compatíveis com OpenAI** (`/v1/audio/speech`): `mlx_audio.server` (Mac), vLLM-Omni (VoxCPM2, Fish, Qwen3-TTS), Nano-vLLM-VoxCPM (FastAPI), `devnen/Chatterbox-TTS-Server` (MIT, com fatiamento para audiobook), `remsky/Kokoro-FastAPI`.

---

## 3. Instalação

### 3.1 RTX 5090 (Blackwell): pré-requisitos obrigatórios
- Driver NVIDIA **R570 ou superior** e **CUDA 12.8 ou superior**. O PyTorch precisa ser **2.7 ou superior com wheels `cu128`** (ou cu129/cu130), porque versões ≤2.6 não têm kernels para sm_120 e dão o erro "no kernel image is available".
- **Atenção ao Chatterbox:** o `pyproject` fixa `torch==2.6.0` em Python abaixo de 3.14. Na 5090 você precisa sobrescrever o torch depois de instalar (veja abaixo) ou usar Python 3.14 com torch ≥2.9.
- **FlashAttention 2:** a compilação para Blackwell é problemática. Comece sem ela (o SDPA nativo do PyTorch funciona) e só instale se precisar economizar VRAM.
- No Windows, prefira **WSL2 com Ubuntu 24.04**. O vLLM e o SGLang não rodam nativos no Windows.

```bash
# Base comum (Linux/WSL2)
nvidia-smi                      # driver >= 570, "CUDA Version: 12.8+"
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo apt-get install -y ffmpeg sox espeak-ng

# ---------- VoxCPM2 (recomendação nº 1) ----------
uv venv ~/venvs/voxcpm --python 3.11 && source ~/venvs/voxcpm/bin/activate
uv pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
uv pip install voxcpm
python -c "import torch;print(torch.__version__, torch.cuda.get_device_capability())"  # espera (12, 0)
# Criar a voz da marca sem pessoa real (Voice Design):
voxcpm design --text "(deep, resonant middle-aged male documentary narrator, slow, cinematic, warm baritone)In the winter of 1943, the city fell silent." --seed 42 --output brand_ref_en.wav
# Clonar a partir do clipe de referência (próprio ou licenciado):
voxcpm clone --text "Texto do roteiro..." --prompt-audio brand_ref_en.wav --prompt-text "In the winter of 1943, the city fell silent." --output take.wav
# Opcional, mais rápido (RTF ~0,13) e com servidor HTTP:
uv pip install nano-vllm-voxcpm

# ---------- Qwen3-TTS (nº 2) ----------
uv venv ~/venvs/qwen3tts --python 3.12 && source ~/venvs/qwen3tts/bin/activate
uv pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
uv pip install -U qwen-tts
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign --ip 0.0.0.0 --port 8000   # cria a voz
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-Base --ip 0.0.0.0 --port 8001          # clona e reutiliza a voz

# ---------- Chatterbox Multilingual V3 / pt-br (nº 3 em PT-BR) ----------
uv venv ~/venvs/chatterbox --python 3.11 && source ~/venvs/chatterbox/bin/activate
uv pip install chatterbox-tts
uv pip install --reinstall torch torchaudio --index-url https://download.pytorch.org/whl/cu128   # sobrescreve o torch 2.6 fixado
# Em Python: ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3"); generate(texto, language_id="pt", audio_prompt_path="ref.wav")
# Para o checkpoint dedicado de PT-BR (ResembleAI/Chatterbox-Multilingual-pt-br), veja o model card no HF.

# ---------- IndexTTS-2.5 (só EN, máxima emoção) ----------
git clone https://github.com/index-tts/index-tts.git && cd index-tts
uv sync --all-extras          # confira se o torch resolvido é cu128; senão: uv pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
uv run tools/gpu_check.py
uv run webui.py --version 2 --model_dir ./checkpoints_2
```

### 3.2 Mac M4 (MLX)
```bash
brew install python@3.12 ffmpeg espeak-ng
python3.12 -m venv ~/venvs/mlxaudio && source ~/venvs/mlxaudio/bin/activate
pip install -U mlx-audio
# VoxCPM2 (8 bits é o equilíbrio entre qualidade e velocidade; use bf16 com 24 GB ou mais de RAM)
mlx_audio.tts.generate --model mlx-community/VoxCPM2-8bit --text "In the winter of 1943..." --ref_audio ./brand_ref_en.wav --output_path ./out
# Qwen3-TTS VoiceDesign
mlx_audio.tts.generate --model mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16 --text "Narração..." --output_path ./out
# Chatterbox Multilingual V3 (PT)
mlx_audio.tts.generate --model mlx-community/chatterbox-multilingual-v3 --text "No inverno de 1943..." --lang_code pt --ref_audio ./brand_ref_pt.wav --output_path ./out
# Servidor compatível com OpenAI
mlx_audio.server --host 0.0.0.0 --port 8000
# POST http://localhost:8000/v1/audio/speech  {"model": "...", "input": "...", "voice": "..."}
```
Os nomes exatos das flags (`--ref_audio`, `--lang_code`) variam por modelo. Rode `mlx_audio.tts.generate --help`.

---

## 4. Licenciamento da voz de referência e voz "de marca" legal

**Regra de ouro:** a licença do *modelo* não dá direito sobre a *voz* que você clona. Só clone uma voz que é sua, que você contratou ou que é sintética.

### Riscos jurídicos
- **Brasil:** a voz é atributo da personalidade, protegida pelo art. 5º, X e XXVIII "a" da CF e pelos arts. 11 a 21 do Código Civil (o art. 20 trata do uso da imagem e da voz). Também é dado pessoal, e possivelmente biométrico (LGPD, art. 5º, II), então o tratamento exige consentimento específico. Há projetos de lei sobre IA e deepfake de voz em tramitação, e o PL 2338 traz regras de transparência para IA.
- **EUA:** o direito de publicidade varia por estado, e o *ELVIS Act* (Tennessee, 2024) trata especificamente de clonagem de voz. Há ainda o NO FAKES Act federal em discussão. O mesmo vale para a imitação de narradores famosos ("soa como o Morgan Freeman"): **não faça**, nem por descrição.
- **As próprias licenças dos modelos proíbem** imitar uma pessoa identificável sem consentimento. A Fish Community License diz isso expressamente na seção IV(b). O StyleTTS2 exige aviso de fala sintética.

### Datasets "livres" não são livres para clonagem
- **LibriVox:** as gravações estão em domínio público quanto ao *copyright*, mas o narrador continua uma pessoa identificável com direitos de personalidade. Clonar a voz de um leitor específico para narrar em escala comercial é juridicamente arriscado. **Evite.**
- **Mozilla Common Voice (CC0):** o CC0 cobre o dataset, mas os termos proíbem tentar identificar os falantes, e os contribuidores não consentiram em ser "a voz" de um canal. Use só para pesquisa e treino, nunca como voz de referência.
- **Vozes de catálogo dos próprios modelos** (Kokoro, CustomVoice do Qwen3, vozes da Kyutai): cada voz tem sua licença. O Kokoro é Apache-2.0, e as vozes do repositório `kyutai/tts-voices` têm licença por voz, algumas CC0 e outras CC-BY. São utilizáveis, mas **qualquer outro canal pode usar a mesma voz**, então não são "de marca".

### Três caminhos legais para uma voz de marca exclusiva (do mais seguro ao mais barato)
1. **Contratar um dublador ou locutor** e gravar de 30 a 60 min de leitura limpa (48 kHz, sala tratada) em EN e PT-BR, ou um locutor por idioma. O **contrato de cessão e licença de voz para síntese por IA** deve dizer explicitamente:
   - finalidade: narração de vídeos do canal, inclusive geração sintética ilimitada;
   - território mundial, prazo determinado ou perpétuo, e pagamento único ou royalty;
   - idiomas, incluindo geração cross-lingual;
   - direito de criar modelo ou LoRA derivado;
   - exclusividade, se for desejada;
   - consentimento LGPD para dado biométrico;
   - proibições (conteúdo político, publicidade de terceiros etc.);
   - cláusula de revogação e o que acontece com o modelo depois dela.

   O SAG-AFTRA tem modelos de acordo para "digital replica" que servem de referência nos EUA. Em plataformas como Voices.com e Fiverr, exija a cláusula "AI voice cloning license" por escrito.
2. **Usar a sua própria voz** (ou a de um sócio, com termo assinado), gravada no mesmo padrão, e fazer o fine-tune.
3. **Criar uma voz 100% sintética** com *Voice Design* (VoxCPM2, Qwen3-TTS VoiceDesign, ZONOS3, MOSS-VoiceGenerator). Por exemplo: "deep, resonant baritone, 50s, slow measured documentary delivery, slight gravel". Gere de 20 a 50 candidatas com seeds diferentes, escolha uma e **congele**: guarde o clipe de referência de 10 a 20 s, o texto, a seed e os parâmetros. Não há pessoa real envolvida. Só confira se a voz não lembra demais alguém famoso, e documente o processo (datas, prompts, arquivos).

### Consistência ao longo de 30 min e entre vídeos
- Use **sempre o mesmo clipe de referência e a transcrição exata** (modo "ultimate cloning" do VoxCPM2, ou `create_voice_clone_prompt` do Qwen3, que gera um prompt reutilizável). Mantenha seed fixa, mesmo `cfg` e mesmo número de *timesteps*.
- Para fixar a voz de vez, faça o **fine-tune LoRA** no VoxCPM2 (`lora_ft_webui.py`) ou o fine-tune do Qwen3-TTS com 30 a 60 min de áudio licenciado ou sintético. Isso reduz a deriva de timbre.
- **Fatie** o roteiro por parágrafo (~200 a 400 caracteres, sempre terminando em ponto final). Gere cada trecho, valide com ASR (Whisper ou Qwen3-ASR) comparando WER e duração, e **regenere automaticamente** os trechos com WER alto, cortes ou alucinação. Concatene com 250 a 600 ms de silêncio.
- Normalize o texto antes de gerar: números, datas e siglas por extenso, e um glossário de pronúncia para nomes próprios (o IndexTTS aceita fonemas CMU; o VoxCPM e o Qwen respondem bem a grafia fonética).
- **Masterize sempre na mesma cadeia:** high-pass em 70 Hz, de-esser, compressão leve (2:1), EQ com leve realce em 120 a 200 Hz para dar o "grave cinematográfico", e loudness em **-14 LUFS integrado, -1 dBTP** para o YouTube (`ffmpeg -af loudnorm=I=-14:TP=-1:LRA=7`).

### YouTube
- Na divulgação de conteúdo sintético ("altered or synthetic content"), marque a opção quando uma **voz realista imitar uma pessoa real** ou quando o conteúdo puder enganar sobre fatos. Uma narração com voz sintética própria geralmente não exige a marcação, mas marcar não penaliza. Também é bom deixar transparência na descrição.
- Na monetização, a política de "conteúdo inautêntico" (antes chamada de repetitivo ou produzido em massa) atinge canais de narração por IA com pouco valor agregado. A qualidade do roteiro, a pesquisa e a edição importam mais que o TTS.
- As marcas d'água inaudíveis (PerTh no Chatterbox, sinais na Fish) não atrapalham o YouTube. **Não tente removê-las**, porque isso viola a licença da Fish.

---

## 5. Notas de risco e o que verificar antes de produzir
1. Abra o model card no Hugging Face e confirme a licença dos pesos de: Qwen3-TTS, OmniVoice (incluindo se treinou com Emilia/NC), Chatterbox pt-br, ZONOS3-Mini, Pocket TTS, Higgs v2 e Orpheus.
2. Se você for agência ou prestador para terceiros, a Fish Community License tem regras próprias (a seção III(a) permite entregar só o áudio final ao cliente). O teto de US$ 500 mil considera a receita bruta de você mais as afiliadas.
3. Chatterbox, Dia, CSM, Zonos v0.1, Spark e Orpheus estão sem manutenção. Funcionam, mas não espere correções.
4. VibeVoice: a própria Microsoft desaconselha o uso comercial, e o PT não é suportado. Descarte.
5. Faça um teste cego de 3 min do mesmo roteiro (EN e PT) com VoxCPM2, Qwen3-TTS, Chatterbox pt-br e OmniVoice, compare com a sua narração atual do ElevenLabs, e só então congele a escolha.
