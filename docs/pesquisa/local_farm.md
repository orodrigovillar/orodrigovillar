# Fazenda local de documentários faceless (15–30 min): RTX 5090 + Mac M4, orquestrada pelo Claude

> Data: 15/11/2026. **Limitação desta pesquisa:** a cota de busca web acabou e `developers.google.com` não está liberado na rede desta sessão. Por isso as informações vêm de READMEs e licenças do GitHub (estrelas e datas consultadas hoje) e do meu conhecimento prévio. Os itens marcados **[CONFIRMAR]** devem ser checados na documentação oficial antes de entrar em produção.

---

## 0. Resumo executivo

- **Arquitetura recomendada:** um orquestrador **Python determinístico** que roda 24/7, com **Prefect** (ou uma fila SQLite simples) chamando serviços locais: **ComfyUI** em modo API para imagem e vídeo, **Ollama/llama.cpp** para o LLM local, um servidor TTS (**Kokoro-FastAPI** ou **Chatterbox**), **WhisperX/stable-ts** para alinhamento e **ffmpeg com NVENC** para a montagem. O **Claude Code fica de diretor criativo e supervisor**: escreve e revisa roteiros, faz o fact-check, cuida da QA e corrige falhas. Ele **não** fica no loop quente de cada frame.
- **Custo:** R$0 em APIs, com todos os modelos locais sob licenças comerciais permissivas (Apache/MIT). Os gastos reais são a energia elétrica (~575 W de pico na 5090) e o plano Claude que você já paga.
- **Gargalo real:** a GPU **não** é o gargalo. A 5090 produz de **8 a 12 vídeos de 20 min por dia**. O que limita é a **cota da YouTube Data API**: o padrão de 10.000 unidades/dia dá **~6 uploads/dia por projeto GCP**. Há ainda a política de monetização contra "conteúdo inautêntico/produzido em massa", e a recomendação prática é **1–2 vídeos/dia por canal**.
- **Antes de tudo:** projetos de API criados depois de 28/07/2020 e **não auditados** sobem os vídeos **travados em privado**. Peça a **auditoria de conformidade da YouTube API** (gratuita) logo no primeiro dia.

---

## 1. Diagrama de arquitetura (ASCII)

```
                         ┌───────────────────────────────────────────┐
                         │  CLAUDE CODE (diretor / supervisor)       │
                         │  A) sessão na nuvem + Remote Control  ou  │
                         │  B) `claude` local no WSL2 do PC          │
                         │  - escolhe pautas, escreve/revisa roteiro │
                         │  - fact-check com fontes, QA, corrige jobs│
                         │  - lê logs/relatórios, nunca lê segredos  │
                         └──────────────┬────────────────────────────┘
                                        │ edita arquivos em farm/queue/*.json,
                                        │ roda `farm` CLI, lê farm/reports/
┌───────────────────────────────── PC RTX 5090 (Windows 11 + WSL2 Ubuntu, usuário "farm") ─────────────────────────┐
│                                                                                                                  │
│  ┌──────────────┐   ┌──────────────────────── ORQUESTRADOR (Prefect 3 / fila SQLite) ───────────────────────┐    │
│  │ farm/queue/  │──▶│ 1 research → 2 script → 3 factcheck → 4 TTS → 5 align → 6 shotlist → 7 imagens →    │    │
│  │ (jobs JSON)  │   │ 8 I2V hero → 9 música/SFX → 10 montagem → 11 legendas → 12 thumb → 13 metadata →    │    │
│  └──────────────┘   │ 14 QA gate (humano/Claude) → 15 upload agendado YT → 16 cross-post FB               │    │
│                     └──┬────────┬─────────┬──────────┬───────────┬──────────┬─────────────┬──────────────────┘    │
│                        │        │         │          │           │          │             │                       │
│              ┌─────────▼──┐ ┌───▼─────┐ ┌─▼────────┐ ┌▼─────────┐ ┌▼───────┐ ┌▼─────────┐ ┌▼────────────────┐     │
│              │ Ollama /   │ │ TTS srv │ │ WhisperX │ │ ComfyUI  │ │ACE-Step│ │ ffmpeg   │ │ uploader (OAuth) │     │
│              │ llama.cpp  │ │ Kokoro/ │ │ stable-ts│ │ :8188    │ │ música │ │ NVENC    │ │ YouTube v3 +     │     │
│              │ Qwen3 32B  │ │Chatterbx│ │ (align)  │ │ Z-Image/ │ │        │ │ + Python │ │ FB Graph API     │     │
│              │ :11434     │ │ :8880   │ │          │ │ Flux/Wan │ │        │ │ (moviepy)│ │ tokens em secrets│     │
│              └────────────┘ └─────────┘ └──────────┘ └──────────┘ └────────┘ └──────────┘ └──────────────────┘     │
│                    GPU agendada por "lease": 1 job pesado por vez (LLM ↔ ComfyUI ↔ TTS revezam a VRAM 32 GB)        │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┘
                                               │ Syncthing / SMB (somente farm/projects e farm/out)
                          ┌────────────────────▼────────────────────┐
                          │ MAC M4 (worker CPU/Neural Engine)        │
                          │ - LLM leve (MLX/Ollama) p/ tradução,     │
                          │   títulos, descrições, legendas PT/EN/ES │
                          │ - Kokoro MLX (TTS de backup)             │
                          │ - ffmpeg VideoToolbox (montagem 2ª fila) │
                          │ - thumbnails (Pillow) e QA visual        │
                          └──────────────────────────────────────────┘
```

---

## 2. Stack escolhida por etapa (somente opções gratuitas e com licença verificada)

| Etapa | Ferramenta recomendada | Licença | Alternativa | Observação |
|---|---|---|---|---|
| Pesquisa de pauta | Claude Code (WebSearch/WebFetch) + RSS/Wikipedia API + DuckDuckGo | – | Qwen3 local + `duckduckgo-search` | O "anti-hallucination gate" do *Verticals* (abaixo) é um bom padrão: o roteiro só pode usar fatos do dossiê |
| Roteiro (3–5 mil palavras) | **Claude** (melhor qualidade narrativa) | – | **Qwen3-32B/30B-A3B** via Ollama | Use o LLM local para rascunhos, variações e tradução |
| Fact-check | Claude, com cada afirmação ligada a uma URL do dossiê | – | Qwen3 + busca | Gera `claims.json` com status ok, duvidoso ou removido |
| TTS | **Kokoro-82M** (Apache-2.0, `remsky/Kokoro-FastAPI` ★5,7k) | Apache-2.0 | **Chatterbox** (MIT, ★27,8k; tem multilíngue e clonagem; insere marca d'água Perth) | ⚠ **Evite em monetização** F5-TTS (código MIT, mas pesos CC-BY-NC), Fish-Speech (pesos NC) e XTTS-v2 (licença Coqui não comercial) |
| Alinhamento forçado | **WhisperX** (BSD-2, ★25,3k) ou **stable-ts** (MIT, ★2,3k; tem `align()` texto+áudio) | BSD/MIT | MFA (MIT, modelos CC-BY-4.0), aeneas (**AGPL**, antigo, evite) | Como você já tem o texto, prefira o `stable_ts.align(audio, texto)`: dá timestamps exatos por palavra sem erro de ASR |
| Shot list | LLM (Claude/Qwen) lê o roteiro e os timestamps e gera `shots.json` com cena, duração, prompt, tipo (still/ken-burns/hero-I2V/mapa/arquivo) | – | – | Uma imagem a cada 4–7 s, ou seja, ~200–300 shots num vídeo de 20 min |
| Imagens | **Z-Image-Turbo** (Apache-2.0, ★12k) ou **Qwen-Image** (Apache-2.0) ou **FLUX.1-schnell** (Apache-2.0) no ComfyUI | Apache | FLUX.1-dev (**pesos não comerciais**; as saídas podem ser usadas comercialmente pela licença, mas prefira os Apache) | Rode um batch de prompts via API |
| Image-to-video (hero) | **Wan2.2 I2V-A14B** (Apache-2.0, ★18,7k) com LoRA de poucos passos (lightx2v) ou **Wan2.2 TI2V-5B** (mais rápido) | Apache | LTX-Video/LTX-2 (Lightricks; o repo diz Apache-2.0, mas os pesos do LTX-2 têm licença própria com teto de receita **[CONFIRMAR]**) | 8–20 clipes hero de 5 s por vídeo; o resto é Ken Burns |
| Música | **ACE-Step** (Apache-2.0) + YouTube Audio Library | Apache | MusicGen (pesos **CC-BY-NC**, evite) | Gere 3–4 faixas de "mood" por vídeo e use ducking sob a voz |
| SFX | Freesound filtrado por **CC0**, biblioteca própria | CC0 | – | Mantenha um `assets/sfx/LICENSES.csv` |
| Montagem | **ffmpeg** (h264_nvenc/hevc_nvenc) + Python (MoviePy 2 ou geração de filtergraph) | LGPL/GPL | – | Pré-renderize o Ken Burns por shot e concatene: mais rápido que um `zoompan` gigante |
| Legendas | SRT/ASS gerados dos timestamps (sem refazer ASR) | – | – | Envie o SRT ao YouTube e queime só no Shorts derivado |
| Thumbnail | Z-Image/Flux (1280×720) + Pillow com texto e fonte fixa | – | – | Teste A/B nativo do YouTube ("Test & Compare") é manual no Studio |
| Metadados | LLM gera título, descrição, capítulos (dos timestamps), tags | – | – | Capítulos saem de graça do `shots.json` |
| Upload | Script Python próprio (`google-api-python-client`) ou **porjo/youtubeuploader** (Go, Apache-2.0, ★895) | Apache | `tokland/youtube-upload` (abandonado desde 2024) | Upload resumable com `privacyStatus=private` + `publishAt` |
| Facebook | Graph API `/{page-id}/videos` (upload resumable) | – | `mrdotb/facebook-api-video-upload` (MIT) como referência | Agendamento com `published=false` + `scheduled_publish_time` |

### Licenças dos LLMs locais (para rascunho e tradução)

- **Qwen3 / Qwen3-Coder / Qwen3-30B-A3B:** Apache-2.0, a melhor escolha. Na 5090 (32 GB), o Qwen3-32B Q4_K_M ou o 30B-A3B (MoE, muito rápido) cabem com folga.
- **Gemma:** o código do `google-deepmind/gemma` é Apache-2.0. Os **pesos** das gerações 1–3 usam os "Gemma Terms of Use" (uso comercial liberado, mas com política de uso proibido que se repassa adiante). Verifique a licença da geração mais nova **[CONFIRMAR]**.
- **Llama 3.x/4:** Llama Community License. O uso comercial é liberado abaixo de 700 milhões de MAU, mas exige atribuição ("Built with Llama") e respeito à AUP. Funciona, mas é menos limpa que a Apache.
- **Veredito:** use **Claude para o roteiro final e o fact-check** (qualidade, raciocínio e busca com fontes) e **Qwen3 local** para o volume: traduções PT/EN/ES, descrições, prompts de imagem para 250 shots e reescritas. O Claude, via plano Max/Pro em `claude -p`, não tem custo por token, mas tem **limites de uso por janela**. Por isso convém tirar do Claude as tarefas repetitivas.

---

## 3. Orquestração: as opções comparadas

| Opção | Prós | Contras | Uso aqui |
|---|---|---|---|
| **ComfyUI API** (`Comfy-Org/ComfyUI` ★147k, GPL-3.0) | Padrão de fato para Flux/Wan/Z-Image. A API HTTP é simples: `POST /prompt` com o workflow exportado em "Export (API)" e `client_id`; progresso por `ws://127.0.0.1:8188/ws?clientId=…`; resultado por `GET /history/{prompt_id}` e `GET /view?filename=…`; entradas por `POST /upload/image` | Não é orquestrador de pipeline. Custom nodes são vetor de malware (houve casos reais em 2024) | **Serviço de imagem/vídeo**, chamado pelo orquestrador. Faça *pin* de versões e de custom nodes |
| **comfy-cli** (GPL-3.0, ★1k) | Instala, atualiza e roda ComfyUI e nodes por CLI | – | Bom para setup reproduzível |
| **Prefect 3** (Apache-2.0, ★24k) | Flows Python, retries, cache por etapa, UI local, agendamento, concorrência por tag (`gpu=1`) | Mais uma peça para operar | **Recomendado** como espinha dorsal |
| **Celery** (BSD, ★29k) | Filas distribuídas maduras (PC + Mac) | Exige Redis/RabbitMQ e não traz UI de pipeline | Só se quiser workers distribuídos complexos |
| **n8n** self-hosted (★210k, *Sustainable Use License*, gratuita para uso interno) | Visual, com templates "faceless" prontos (`aruntemme/n8n-faceless-youtube`, `Cesium1377/youtube-documentary-automation`) e um MCP (`czlonkowski/n8n-mcp`, MIT) que deixa o Claude operar o n8n | Lógica de vídeo pesada fica feia em nós; versionamento pior | Opcional para **gatilhos e notificações** (Telegram/Discord, aprovação humana) |
| **Pinokio** (MIT, ★8,4k) | Instalação em 1 clique de ComfyUI, Wan, TTS e similares | Não é orquestrador e cria ambientes opacos | Atalho para **testar** modelos e não serve para produção |
| Fila SQLite + script `farm` | Zero dependências, fácil para o Claude ler | Retries e UI ficam por sua conta | Bom para o **MVP da semana 1**, depois migre para Prefect |

**Padrão "idempotente por etapa":** cada etapa grava em `projects/<slug>/<NN_etapa>/` e um `done.json` com hash dos insumos. Se a etapa falha, o retry refaz só ela. O Claude consegue inspecionar e consertar qualquer job lendo arquivos, sem nenhum estado escondido.

---

## 4. YouTube Data API v3 e Facebook Graph API

### YouTube

- **Cota padrão:** 10.000 unidades/dia por projeto GCP, com reset à meia-noite (horário do Pacífico).
- **Custos de cota:**
  - `videos.insert` custa **1.600 unidades**, ou seja, **~6 uploads/dia**. O README do `porjo/youtubeuploader` confirma: *"By default you will only be able to upload ~6 videos every 24 hours"*. **[CONFIRMAR]** o valor atual na *Quota Calculator*, porque o Google pode ter alterado o custo.
  - `thumbnails.set` custa ~50.
  - `captions.insert` custa ~400.
  - `playlistItems.insert` custa ~50.
  - Leituras custam 1.
  - Conta típica por vídeo completo: 1.600 + 50 + 400 + 50 ≈ **2.100**, o que dá **4 vídeos completos/dia** por projeto.
- **Para escalar:**
  - Peça aumento de cota no formulário *YouTube API Services – Audit and Quota Extension* (gratuito, leva semanas).
  - Ou use um projeto GCP por canal. Não use vários projetos para burlar a cota de um mesmo canal, porque isso viola os ToS.
- **Vídeos travados em privado:** projetos **não verificados** criados após 28/07/2020 têm todo upload "restricted to private" (citado do README do porjo). **Agendamento por `publishAt` só funciona depois da auditoria.** Até lá, há duas saídas: subir como privado e publicar/agendar manualmente no Studio **[CONFIRMAR se vídeos travados podem ser liberados manualmente]**, ou subir pelo Studio.
- **Agendamento:** `status.privacyStatus="private"` + `status.publishAt="2026-11-20T15:00:00-03:00"`.
- **Envio:** upload resumable (`MediaFileUpload(chunksize=-1, resumable=True)`), escopo OAuth `youtube.upload` (+ `youtube.force-ssl` para legendas), com refresh token guardado fora do repositório.
- **Conteúdo sintético:** declare `status.containsSyntheticMedia=true` quando houver cenas realistas geradas por IA **[CONFIRMAR o nome do campo]**. Atenção também à política do YPP de **conteúdo inautêntico/repetitivo** (atualizada em jul/2025): vídeo em massa com template idêntico e TTS genérico corre risco de desmonetização. Varie formato, narração e pesquisa.
- **Limite separado do canal:** existe um limite diário de uploads por canal (inclusive pelo Studio, ~10–15 dependendo da verificação) **[CONFIRMAR]**.

### Facebook (Página)

- **Permissões:** app Meta em modo desenvolvimento (basta para as suas próprias Páginas, já que você é admin do app) com `pages_manage_posts`, `pages_read_engagement` e `publish_video`. Use um **Page access token de longa duração**.
- **Upload:** `POST /{page-id}/videos` no fluxo resumable, com `upload_phase=start` e depois `transfer` (chunks) e `finish`, ou o *Resumable Upload API* novo (`rupload.facebook.com`). Inclua `title`, `description` e `thumb`.
- **Agendamento:** `published=false` + `scheduled_publish_time` (unix). A janela permitida fica entre ~10 minutos e alguns meses à frente **[CONFIRMAR o limite]**.
- **Reels:** para 9:16 curtos, o endpoint é `/{page-id}/video_reels`, com fluxo próprio.
- **Alternativa:** existe um conector Postiz nesta conta. Ele agendaria o FB e outras redes, mas é serviço externo e não é "100% local".

---

## 5. Repositórios open source: o que reaproveitar

| Repo | ★ / licença | O que reaproveitar |
|---|---|---|
| `harry0703/MoneyPrinterTurbo` | 143,8k / MIT | Estrutura de tarefas, legendas, BGM e WebUI/API. É focado em vídeo curto com stock footage |
| `AIDC-AI/Pixelle-Video` (ATH-MaaS) | 30k / Apache-2.0 | **O mais próximo do que você quer:** roteiro → imagem por frase → I2V (Wan) → TTS → composição, **sobre workflows ComfyUI** e com templates. Estude os workflows e o "split por sentença" |
| `rushindrasinha/youtube-shorts-pipeline` (Verticals v3) | 2,4k / MIT | Estágios **resumíveis**, *niche profiles*, *anti-hallucination gate* (o roteiro só usa fatos da pesquisa), ASS com palavra destacada, Ken Burns + ducking, **upload privado por padrão**. Aceita Claude CLI como provider |
| `aruntemme/n8n-faceless-youtube` | 74 / MIT | Exemplo de fluxo n8n, útil se quiser n8n para gatilhos |
| `Cesium1377/youtube-documentary-automation` | 4 / sem licença | Ideia de roteiro longo por capítulos. **Sem licença: só leia, não copie** |
| `ndpvt-web/short-movie-maker` | 1 / sem licença | "Pipeline para Claude Code" de 1–25 min. Vale ler o desenho, mas não copie código |
| `abus-aikorea/voice-pro` | 13k / GPL-3.0 | Referência de multi-TTS e tradução |
| `diodiogod/TTS-Audio-Suite` | 1,3k | TTS (Chatterbox/F5 etc.) **dentro do ComfyUI**. Atenção às licenças dos pesos |
| `sasharun/awesome-faceless` | CC0 | Lista de ferramentas |

**Conclusão:** nenhum desses repos faz bem o **documentário longo de 20–30 min**, porque todos são feitos para Shorts. O melhor caminho é **escrever o seu próprio orquestrador**, de ~1.500 linhas de Python, e reaproveitar ideias do Verticals (estágios resumíveis e gate de fatos) e do Pixelle (workflows ComfyUI). O Claude Code escreve esse código para você.

---

## 6. Como o Claude Code dirige o PC

### Opção A: Claude Code local no PC (recomendada para a operação diária)

- Instale o Claude Code **dentro do WSL2 (Ubuntu)**, logado com o usuário Windows dedicado `farm`.
- O orquestrador (Prefect) roda **sozinho** como serviço `systemd` (WSL2 com `systemd=true`).
- O Claude entra por agendamento:
  - `claude -p "leia farm/reports/hoje.md, escolha 2 pautas da fila de ideias, escreva roteiro + claims.json conforme farm/docs/ROTEIRO.md" --allowedTools ...` disparado por `cron`/`systemd timer` 2–4×/dia.
  - Também pode rodar interativamente com uma tarefa longa: `/loop 30m verificar falhas do pipeline e corrigir`.
- Restrinja as permissões em `farm/.claude/settings.json`: `deny` para `Read(secrets/**)` e `Bash(curl *)` fora de uma lista de hosts. Permita só `Bash(farm *)`, `Bash(ffmpeg *)`, `Bash(python -m farm *)`.

### Opção B: sessão na nuvem + Remote Control (para supervisionar pelo celular ou navegador)

- No **app Claude Desktop** do PC: **Settings → Claude Code → Remote Control**. Escolha a pasta a compartilhar.
- **Restrições de pasta:** **não pode ser a home** nem uma pasta oculta direto sob a home (`~/.algo`) ou sob `~/Library`. Use algo como `C:\Users\farm\farm` ou `/home/farm/farm`.
- Alternativa: rodar `claude remote-control` num terminal dentro da pasta. A sessão aparece no app Claude Code.
- O app/Remote Control precisa ficar **aberto** no PC para responder. Uma sessão fica presa ao primeiro computador a que se conecta.
- **Uso típico:** você abre uma sessão no celular, ela pede acesso à pasta `farm` e o Claude roda comandos **no PC** (ver fila, rerodar etapa, aprovar roteiro).

### Segurança

1. **Usuário Windows separado** (`farm`, sem admin) e **WSL2** para tudo. ComfyUI, Ollama e TTS escutam **só em `127.0.0.1`**. Se o Mac precisar chamar, use **Tailscale** (gratuito) em vez de abrir portas.
2. **Nenhum segredo em scripts ou no repositório.** OAuth do YouTube (`client_secret.json`, `token.json`) e token da Página FB ficam em `~/.config/farm-secrets/` com `chmod 600`, fora da pasta compartilhada com o Claude. O uploader lê dali. O Claude é bloqueado por regra `deny`.
3. **Custom nodes do ComfyUI e repositórios de modelos:** instale só de fontes conhecidas, com versão fixada (`comfy-cli` + lockfile). Prefira `.safetensors` (nunca `.ckpt`/pickle) e faça varredura periódica. Já houve nodes maliciosos roubando credenciais.
4. Faça backups de `farm/projects/*/final/` e do banco da fila. Ponha um limite de disco: 1 vídeo com assets tem ~5–15 GB, então limpe os intermediários após 7 dias.
5. **Aprovação humana** antes do upload público (gate 14). Pelo menos nas primeiras semanas, o Claude só agenda como privado.

---

## 7. Layout de pastas

```
/home/farm/farm/                      ← pasta compartilhada via Remote Control (NÃO é a home)
├── CLAUDE.md                         ← regras para o Claude: estilo do canal, gates, comandos permitidos
├── .claude/settings.json             ← permissões (deny secrets, allow farm/ffmpeg/python)
├── docs/
│   ├── ROTEIRO.md                    ← guia de roteiro (estrutura 20 min, ganchos, capítulos)
│   ├── ESTILO_VISUAL.md              ← prompts-base, paleta, LoRAs, negative prompts
│   └── CANAIS.yaml                   ← canais, idiomas, horários de postagem
├── farm/                             ← código do orquestrador (pacote Python)
│   ├── cli.py                        ← `farm new|run|retry|status|publish`
│   ├── flows/                        ← Prefect flows (1 arquivo por etapa)
│   ├── clients/comfy.py              ← POST /prompt, websocket, /history, /view
│   ├── clients/tts.py, llm.py, yt.py, fb.py
│   └── workflows/                    ← JSON do ComfyUI exportados em "API format" (versionados)
├── queue/
│   ├── ideas.yaml                    ← backlog de pautas
│   └── jobs.sqlite                   ← estado da fila
├── projects/<AAAA-MM-DD_slug>/
│   ├── 01_research/dossie.md, fontes.json
│   ├── 02_script/roteiro.md
│   ├── 03_factcheck/claims.json
│   ├── 04_tts/narracao.wav
│   ├── 05_align/words.json
│   ├── 06_shots/shots.json
│   ├── 07_images/s0001.png …
│   ├── 08_hero/h01.mp4 …
│   ├── 09_audio/music_*.wav, sfx/
│   ├── 10_render/clips/, master.mp4
│   ├── 11_subs/pt.srt, en.srt
│   ├── 12_thumb/thumb_a.jpg, thumb_b.jpg
│   ├── 13_meta/youtube.json, facebook.json
│   └── STATUS.json                   ← etapa atual, erros, hashes
├── assets/{fonts,music,sfx,luts,logos}/ + LICENSES.csv
├── reports/AAAA-MM-DD.md             ← relatório diário (o Claude lê)
└── logs/
/home/farm/models/                    ← pesos (fora da pasta compartilhada)
/home/farm/ComfyUI/                   ← instalação ComfyUI
/home/farm/.config/farm-secrets/      ← OAuth YouTube, token FB (chmod 600, nunca compartilhado)
```

---

## 8. Estimativa de throughput (1× RTX 5090, vídeo de 20 min 1080p)

Hipóteses: ~3.000 palavras de narração, 1 imagem a cada ~5 s (~240 imagens), 12 clipes hero I2V de 5 s e música gerada. Os tempos são **estimativas** para modelos otimizados (FP8/NVFP4 + LoRAs de poucos passos). Meça no seu hardware na semana 1.

| Etapa | Onde | Tempo estimado |
|---|---|---|
| Pesquisa + roteiro + fact-check | Claude (nuvem) ou Qwen3-32B local (~50–60 tok/s) | 10–20 min (não usa a GPU se for o Claude) |
| Prompts dos 240 shots | Qwen3-30B-A3B local | 3–5 min |
| TTS 20 min | Kokoro (≫ tempo real) / Chatterbox (~2–4× tempo real) | 1–2 min / 6–10 min |
| Alinhamento | stable-ts/WhisperX | 1–2 min |
| 240 imagens 1344×768 | Z-Image-Turbo / FLUX-schnell (~1,5–3 s cada) | 6–12 min |
| 12 clipes hero I2V 720p 5 s | Wan2.2 I2V-A14B com LoRA 4–8 passos (~1,5–3 min cada) | 18–36 min |
| Música (3 faixas) | ACE-Step | 1–3 min |
| Montagem + Ken Burns + mix | ffmpeg NVENC (CPU + NVENC; pode ir para o Mac) | 8–15 min |
| Thumb + metadados + SRT | GPU/LLM | 2–4 min |
| **Total de GPU por vídeo** | | **~45–80 min** |

- **Teórico, 24 h:** ~18–30 vídeos/dia.
- **Realista, com retries, QA e janelas para o Claude:** **8–12 vídeos/dia**. Sem I2V hero, só Ken Burns, sobe para 20+.
- **Limite efetivo:** a cota da API, de **~6 uploads/dia por projeto** (≈4 com thumbnail e legenda via API). A estratégia de canal recomenda **1–2/dia por canal**.
- **Uso da capacidade sobrando:** versões em outros idiomas (EN/ES com TTS próprio, outro canal), Shorts derivados e regeneração de cenas fracas.
- **Papel do Mac M4:** tira da 5090 a montagem e encode (VideoToolbox), a tradução e as descrições (Qwen3 8–14B em MLX), as thumbnails e a QA. Na prática libera ~20–30% do tempo de GPU.

---

## 9. Checklist de setup, passo a passo

### Semana 0: contas e burocracia (comece já, porque demora)

1. [ ] Crie um projeto no Google Cloud **dedicado ao canal**, ative a *YouTube Data API v3* e crie a tela de consentimento OAuth e um **OAuth Client "Desktop app"**.
2. [ ] Envie o formulário **YouTube API Services – Audit & Quota Extension**, que tira a trava de privado e pode aumentar a cota. Descreva o uso honestamente: "upload do próprio canal, conteúdo próprio".
3. [ ] Confira na *Quota Calculator* oficial os custos atuais de `videos.insert`, `thumbnails.set` e `captions.insert` **[CONFIRMAR]**.
4. [ ] Crie um app Meta (tipo Business), adicione o produto Páginas, gere um Page token de longa duração com `pages_manage_posts`, `pages_read_engagement` e `publish_video`.
5. [ ] Leia as políticas do YPP sobre **conteúdo inautêntico/repetitivo** e **divulgação de conteúdo alterado/sintético**.

### Semana 1: base no PC

6. [ ] Crie o usuário Windows `farm` (padrão, sem admin). Atualize o driver NVIDIA (série 50 / Blackwell exige CUDA 12.8+ e PyTorch com `cu128` ou superior).
7. [ ] `wsl --install -d Ubuntu-24.04`. Em `/etc/wsl.conf`, ponha `[boot] systemd=true`. Limite RAM e swap em `.wslconfig`.
8. [ ] No WSL: `nvidia-smi` funcionando, `uv`/Python 3.12, `ffmpeg` com NVENC (`ffmpeg -encoders | grep nvenc`).
9. [ ] **ComfyUI** via `comfy-cli`, ouvindo em `--listen 127.0.0.1 --port 8188`. Instale ComfyUI-Manager, baixe Z-Image-Turbo (ou FLUX.1-schnell) e Wan2.2 (I2V-A14B + LoRA lightx2v, ou TI2V-5B). Monte 2 workflows (txt2img e img2vid) e **exporte em formato API** para `farm/workflows/`.
10. [ ] **Ollama** (`ollama pull qwen3:32b` e `qwen3:30b-a3b`), ouvindo em 127.0.0.1.
11. [ ] **TTS:** Kokoro-FastAPI (Docker ou uv) na porta 8880. Teste a voz PT-BR. Se quiser clonagem e mais naturalidade, use Chatterbox multilíngue (MIT). Verifique a licença de cada voz/peso.
12. [ ] **Alinhamento:** `pip install stable-ts whisperx`. Teste `stable_whisper.load_model('large-v3').align('narracao.wav', texto, language='pt')`.
13. [ ] **Música:** ACE-Step. Monte também a pasta `assets/music` com faixas da YouTube Audio Library.
14. [ ] **Claude Code** no WSL (`npm i -g @anthropic-ai/claude-code`), com login e `cd ~/farm && claude`.

### Semana 1–2: pipeline

15. [ ] Peça ao Claude Code para gerar o pacote `farm/`: CLI, clientes (comfy/tts/llm/yt/fb), flows Prefect por etapa, `STATUS.json` idempotente e lease de GPU (1 job pesado por vez).
16. [ ] Escreva `CLAUDE.md`, `docs/ROTEIRO.md` e `docs/ESTILO_VISUAL.md` (tom do canal, estrutura de 20 min com gancho, 5–7 capítulos e CTA; regras de fact-check).
17. [ ] Rode **1 vídeo ponta a ponta** manualmente, etapa por etapa. Meça os tempos reais e ajuste a tabela da seção 8.
18. [ ] Uploader: primeiro OAuth interativo (gera `token.json` em `~/.config/farm-secrets/`), teste com vídeo **privado** e só depois `publishAt`.
19. [ ] Cross-post FB: teste com `published=false` + `scheduled_publish_time`.
20. [ ] Configure o gate de QA: o relatório diário mostra thumbnail, 10 frames amostrados, `claims.json` e trechos de áudio. Aprovação via `farm approve <slug>` (ou botão no n8n/Telegram).

### Semana 2: automação 24/7

21. [ ] `systemd` units: `comfyui.service`, `ollama.service`, `tts.service`, `prefect-worker.service`. Ponha `Restart=always`.
22. [ ] Agendamentos:
    - `claude -p` 2×/dia: pauta, roteiro e fact-check.
    - 1×/dia: revisão de falhas e relatório.
    - Prefect: render contínuo e uploads nos horários do `CANAIS.yaml`, respeitando a cota.
23. [ ] **Remote Control:** no Claude Desktop, Settings → Claude Code → Remote Control, adicione a pasta `farm` (não a home). Teste uma sessão pelo celular.
24. [ ] **Mac M4:** Syncthing (só `projects/` e `out/`), Tailscale, Ollama/MLX com Qwen3 8–14B para traduções e um worker Prefect com tag `mac` para encode via VideoToolbox.
25. [ ] **Segurança final:** regras `deny` em `.claude/settings.json`, portas só em localhost/Tailscale, custom nodes fixados, backup semanal, limpeza de intermediários com mais de 7 dias.
26. [ ] **Escala:** depois da auditoria e de 2–4 semanas de métricas (retenção, CTR), aumente para 2/dia, adicione canais por idioma e Shorts derivados.
