# Geração local de stills cinematográficos 16:9 (RTX 5090 + Mac M4): estudo de licença, qualidade e velocidade

*Pesquisa feita em 15/11/2026. A cota de WebSearch estava esgotada e o huggingface.co está bloqueado neste ambiente. Por isso tudo veio do GitHub: READMEs e LICENSEs oficiais lidos via raw.githubusercontent.com, a tabela de licenças do código-fonte do Civitai (`civitai/civitai/src/server/common/constants.ts`) e dois benchmarks independentes publicados no GitHub. Os model cards do Hugging Face não foram lidos diretamente: confirme a licença de cada peso na página do HF antes de baixar. Isto não é parecer jurídico.*

---

## 0. Resumo executivo

**A paisagem mudou muito desde a lista original.** Hoje (nov/2026) existe uma geração nova de modelos abertos de 5 a 12B, mais rápidos e melhores que FLUX.1, SD3.5, HiDream-I1 etc. Vários deles são **Apache-2.0 de verdade**, sem limite de receita.

**Stack recomendado (100% Apache/MIT, uso comercial sem teto de receita):**

| Papel | Modelo principal | Alternativa |
|---|---|---|
| Text-to-image fotorrealista (volume) | **Z-Image-Turbo** (6B, Apache-2.0, 8 passos) | **Boogu-Image-0.1-Turbo** (10B, Apache-2.0, 4 passos) |
| "Hero shots" / prompt complexo | **Qwen-Image-2512** (20B, Apache-2.0) + LoRA Lightning 8 passos | MOSS-Image (5B, Apache) / ERNIE-Image (8B, Apache) |
| Edição / inpainting / trocar elemento / consistência por referência | **Qwen-Image-Edit-2511** (Apache-2.0, multi-referência) | **FLUX.2 [klein] 4B** (Apache-2.0, até multi-ref, ~8 GB) / Boogu-Image-0.1-Edit(-Turbo) (Apache) |
| Edição em 4K | BluePixel-Turbo (Apache-2.0, baseado em FLUX.2 klein 4B) | — |
| Consistência de personagem/locação | LoRA de personagem (Z-Image Base ou Qwen-Image) + edição multi-ref com Qwen-Edit-2511 | — |
| "Film look" consistente | LoRA de estilo treinado no **Z-Image (Base)** e aplicado no Turbo | LoRA no Qwen-Image |
| Upscale | SeedVR2 (ByteDance, Apache-2.0, também no mflux) | 4x-UltraSharp / tile ControlNet |
| Aceleração | **Nunchaku NVFP4** (Apache, suporta Z-Image-Turbo, Qwen-Image, Qwen-Edit) + FP8 nativo no ComfyUI | torch.compile / Cache-DiT / TeaCache |

**Os "quase grátis" (comercial só abaixo de um teto de receita):**
- **Krea 2 Turbo** (12B, o mais estético nos benchmarks): comercial só se a receita anual total for **< US$ 1M**, com filtro de conteúdo obrigatório.
- **FLUX 3 Image Klein** (5.6B, BFL, out/2026): saídas comerciais só para "Qualifying Users" com **< US$ 5M** de receita. Proibido usar as saídas para treinar outros modelos.
- **SD 3.5**: Stability Community License, < US$ 1M.

**Evite em produção monetizada:**
- **Qwen-Image-2.1** (set/2026): mudou para a *Qwen Research License*, que é **não comercial**. Atenção: o Qwen-Image original, o 2512 e o Edit-2511 continuam Apache.
- **FLUX.1 [dev], Kontext [dev], Krea-dev, FLUX.2 [dev], FLUX.2 klein 9B**: ver §2.

**Estimativa de vazão no 5090** (1344×768 ≈ 1 MP): **~1.000 a 1.800 imagens/h** brutas com Z-Image-Turbo NVFP4. Um vídeo de 200 stills, com 3 a 4 variações por plano mais edições e upscale, sai em **~25 a 45 min de GPU**.

---

## 1. Tabela de licenças e desempenho

Legenda de licença: ✅ comercial livre · 🟡 comercial com condições / teto · ❌ não comercial (ou arriscado)

Tempos medidos em ~1 MP (1024² ≈ 1344×768). "Fonte" indica de onde veio o número. Os tempos no 5090 são **estimativas minhas**: ~1,4–1,6× o 4090 em BF16/FP8, e mais com NVFP4.

### 1.1 Geração da nova safra (2025-2026), a mais relevante

| Modelo | Params | Licença dos pesos | Saídas comerciais? | VRAM | Velocidade publicada | 5090 (est.) | Notas de fotorrealismo |
|---|---|---|---|---|---|---|---|
| **Z-Image-Turbo** (Tongyi-MAI) | 6B | ✅ Apache-2.0 | Sim | "cabe em 16 GB"; 21,7 GB de pico no ComfyUI | **7,6 s** @1024², 8 passos, RTX 3090 (Raigor2) | ~2,5–3 s BF16; **~1,5–2 s** Nunchaku NVFP4 | Foi o #1 open-source no Artificial Analysis (dez/25). Realismo muito bom, pouca diversidade entre seeds (é Turbo). Base para LoRA: Z-Image (base, jan/26). Z-Image-Edit e Omni-Base estavam "to be released" no README |
| **Boogu-Image-0.1-Turbo** | 10B | ✅ Apache-2.0 | Sim | 20,6 GB de pico (3090) | **5,5 s** @1024², 4 passos, RTX 3090 | ~2–2,5 s | Ênfase em "realistic photography" e texto. Família com Base, Edit e Edit-Turbo (Apache). Nós ComfyUI oficiais |
| **Qwen-Image-2512** | 20B | ✅ Apache-2.0 | Sim | 28 GB em disco (fp8); no 4090 só roda com streaming | **112 s** (50 passos, 4090, streaming) | ~35–45 s com 50 passos fp8 cabendo em 32 GB; **~5–8 s com Lightning 8 passos**; ~3–5 s Nunchaku+Lightning | Melhor aderência a prompt complexo e texto. Nota humana 4,25 em realismo+anatomia (grawwww) |
| **Qwen-Image-Edit-2511** | 20B | ✅ Apache-2.0 | Sim | idem | Nunchaku 4-bit + Lightning 4/8 passos | ~4–8 s por edição | **Melhor editor Apache**: troca de objeto, inpainting por instrução, multi-imagem (2 ou 3 refs), preservação de identidade |
| **MOSS-Image** (OpenMOSS) | 5B (+9B TE) | ✅ Apache-2.0 | Sim | 18,6 GB (4090) | **27,6 s** (50 passos, 4090) | ~18 s; há destilação comunitária de 8 passos DMD | Realismo 4,0/5 (grawwww). Bom para layout/texto. Tem trainer LoRA (KohakuMossTrainer, DiffSynth) |
| **ERNIE-Image / Turbo** (Baidu) | 8B | ✅ Apache-2.0 | Sim | "roda em 24 GB" | Turbo 8 passos | ~3–4 s (Turbo) | Supera Z-Image-Turbo e FLUX.2-klein-9B nos benchmarks do próprio README. Cores "vívidas, alto contraste" (mflux) |
| **FLUX.2 [klein] 4B** (+Base 4B) | 4B | ✅ Apache-2.0 | Sim | **~8 GB** | "sub-second" em GPU de consumo (BFL) | <1 s | T2I + edição multi-ref num modelo só. Qualidade abaixo do Z-Image/Qwen em realismo, mas excelente como editor rápido |
| **BluePixel-Turbo** (vivo) | ~4B (klein 4B + DCAE) | ✅ Apache-2.0 | Sim | — | 4 passos, 4K nativo | — | Só edição. Útil para editar o still final já em 4K |
| **HiDream-O1-Image** | 8B | ✅ MIT | Sim | — | — | — | Unificado, sem VAE: T2I, edição, personalização por sujeito, storyboard. Promissor para consistência; pouco ecossistema ComfyUI |
| **Krea 2 Turbo / Raw** | 12B | 🟡 Krea 2 Community | Sim, **só se a receita anual (com afiliadas) for < US$ 1M**. Exige filtro de conteúdo e divulgação de IA onde a lei pedir | 20,9 GB (4090) | **12,6 s** (4090, 9 passos); 14,8 s (3090, 8 passos) | ~8 s | **Mais estético**: realismo 4,19 e a melhor composição no grawwww. LoRA no Raw, inferência no Turbo |
| **FLUX 3 Image Klein** | 5.6B | 🟡 FLUX Kommunity v1.0 | Saídas comerciais só para usuário com **< US$ 5M** de receita. O modelo em si é NC. **Proibido** treinar outros modelos com as saídas | 25–31 GB (B200); 23,5 GB no 4090 com streaming | **10,2 s** (4090, 16 passos) | ~6 s; NVFP4 nativo para Blackwell | Requer o "prompt upsampler". Ficou com 0 votos no blind test humano (grawwww). Bom em texto e layout com bounding boxes |
| **Qwen-Image-2.1 / Turbo** | 7B (+8B TE) | ❌ **Qwen Research License (NC)** | **Não**: "research or evaluation only"; precisa de licença comercial separada | 18,7 GB | 18,4 s (4090, 40 passos); Turbo 8 passos | — | Venceu o blind test humano (5,5 de 9 votos) e acertou 12/12 nos prompts difíceis. **Melhor qualidade, mas proibido para uso comercial** |
| FIBO 2.0-dev (Bria) | 8B | ❌ CC BY-NC (dev) | Não | 22,5 GB | 81,7 s (30 passos) | — | Fora |

### 1.2 Modelos da lista original

| Modelo | Licença dos pesos | Saídas comerciais? | VRAM / velocidade | Veredito para doc fotorrealista |
|---|---|---|---|---|
| **FLUX.1 [schnell]** | ✅ Apache-2.0 | Sim | 12B; 4 passos; ~1,5–2 s no 5090 com Nunchaku NVFP4 (o Nunchaku reporta ~3× sobre BF16 no 5090) | Superado. Pele "plástica", baixa diversidade |
| **FLUX.1 [dev] / Kontext [dev] / Krea-dev** | ❌ FLUX.1 [dev] Non-Commercial | **Ambíguo**: a §2(d) diz que as saídas podem ser usadas "for any purpose (including commercial)", mas a licença do *modelo* é só para "Non-Commercial Purposes", e a FLUX NC v2.1 exclui expressamente "revenue-generating activity". Rodar o modelo para produzir um canal monetizado fica fora da licença. Exige ainda filtro de conteúdo ou revisão e divulgação de IA | 12B; ~3–5 s Nunchaku | **Evitar** em produção monetizada, ou comprar licença BFL (bfl.ai/licensing) |
| **FLUX.2 [dev]** (32B) e **klein 9B** | ❌ FLUX Non-Commercial v2.1 | Mesma situação do FLUX.1 dev | 32B; pesado | Evitar |
| **Chroma** (lodestones, base schnell) | ✅ Apache-2.0 | Sim | 8,9B; ~20–30 passos | Bom e sem censura, mas superado pelo Z-Image para foto |
| **Qwen-Image (ago/25) / Edit / Edit-2509 / 2511 / 2512 / Layered** | ✅ Apache-2.0 | Sim | ver acima | **Sim**: núcleo do stack de edição |
| **HiDream-I1 / E1** | ✅ MIT. Atenção: usa o encoder Llama-3.1-8B, sob a Llama Community License, que permite uso comercial abaixo de 700M MAU | Sim | 17B; pesado (~60 GB BF16; GGUF/NF4 para caber) | Superado pelo HiDream-O1 e pelo Z-Image |
| **SD 3.5 Large / Medium** | 🟡 Stability Community License | Sim se a receita anual for < US$ 1M | 8B / 2,5B | Anatomia fraca; superado |
| **SDXL 1.0 + finetunes** (Juggernaut, RealVis etc.) | ✅ OpenRAIL++-M na base. Finetunes: verifique cada card no Civitai (alguns proíbem venda ou exigem crédito) | Geralmente sim | ~3–4 s, 8 GB | Ecossistema de ControlNet/IP-Adapter enorme, mas qualidade de 2023 |
| **Lumina-Image 2.0** | ✅ Apache-2.0 | Sim | 2,6B | Inferior aos novos |
| **OmniGen2** | ✅ Apache-2.0 | Sim | ~7B | Edição e sujeito razoáveis; superado pelo Qwen-Edit-2511 |
| **BAGEL** (ByteDance-Seed) | ✅ Apache-2.0 | Sim | 14B MoT; lento | Pesquisa; edição ok |
| **HunyuanImage 2.1 / 3.0** | 🟡 Tencent Hunyuan Community | Sim, **exceto na UE, Reino Unido e Coreia do Sul** (o Brasil está no "Territory"). Limite de 100M MAU. Proibido usar as saídas para melhorar outros modelos | 3.0 = 80B MoE: impraticável em 32 GB | 2.1 até dá; 3.0 não cabe. Se o canal mira público da UE, o risco aumenta |
| **Kolors** | 🟡 Kolors License | Comercial após **registro** junto à Kuaishou | SDXL-like | Superado |
| **PixArt-Σ** | ✅ OpenRAIL++ | Sim | 0,6B | Superado |
| **Sana** (NVlabs) | Código Apache-2.0. Pesos: verificar o card (versões antigas eram NC) | Verificar | 1,6B, muito rápido | Qualidade foto inferior |

### 1.3 Ferramentas de consistência (atenção às licenças)

| Ferramenta | Licença | Problema |
|---|---|---|
| **IP-Adapter** (tencent-ailab) | Apache-2.0 | OK. As variantes **FaceID** dependem do InsightFace (modelos *antelopev2 / buffalo_l* são **não comerciais**) |
| **PuLID / PuLID-FLUX** | Código Apache-2.0 | Os pesos rodam sobre FLUX.1-dev (NC) e usam o **InsightFace antelopev2 (NC)**. **Duplamente problemático** |
| **InfiniteYou** (ByteDance) | Código Apache-2.0 | Baseado em FLUX.1-dev, com o problema de licença dele, e também usa InsightFace |
| **ACE++** (ali-vilab) | Sem licença declarada no repo; baseado em FLUX.1 Fill [dev] (NC) | Evitar |
| **Krea 2 Identity Edit** | Derivado do Krea 2 (🟡 < US$ 1M) | Só para quem está abaixo do teto |
| **Qwen-Image-Edit-2511 multi-ref** | ✅ Apache | **Recomendado**: identidade de pessoas e produtos sem InsightFace |
| **FLUX.2 klein 4B multi-ref** | ✅ Apache | Recomendado (rápido) |
| **LoRA própria** (treinada com suas imagens) | Herda a licença do modelo base | Com base Apache, fica 100% sua |

### 1.4 Treino de LoRA ("film look" e personagens)

| Ferramenta | Licença da ferramenta | Suporte relevante |
|---|---|---|
| **ostris/ai-toolkit** | MIT | FLUX, Qwen-Image, Z-Image, Krea 2 etc. Tem instalador para a série 50 (`omgitsgb/ostris-ai-toolkit-50gpu-installer`) |
| **kohya-ss sd-scripts / musubi-tuner** | Apache-2.0 | SDXL, FLUX, Qwen-Image, Z-Image (musubi) |
| **OneTrainer** | AGPL-3.0 (a licença vale para o código, não para as LoRAs ou imagens que você gera) | Multi-modelo, GUI |
| **DiffSynth-Studio** (ModelScope) | Apache-2.0 | Qwen-Image, MOSS-Image, Z-Image |
| SimpleTuner, AcademiaSD LoRAlab (MIT) | — | Suportam Qwen-Image 2.1, FLUX.2 klein, FLUX.3 klein, Krea 2, Z-Image, MOSS, ERNIE |
| comfyUI-Realtime-Lora (MIT) | — | Treina LoRA de Z-Image / Klein dentro do ComfyUI |

**Receita para o "film look"**:
1. Junte 30 a 60 frames de referência **com direitos**: suas fotos, stills licenciados, ou gerações próprias curadas.
2. Legende tudo com um VLM e use um token de gatilho tipo `dbcfilm look`.
3. Treine uma LoRA rank 16–32, ~2.000–3.000 passos, no **Z-Image (Base)** com ai-toolkit ou musubi. O treino leva ~1–2 h no 5090 e cabe nos 32 GB sem truques.
4. Aplique a LoRA no Z-Image-Turbo com peso 0,6 a 0,9.

Faça o mesmo para personagens recorrentes: 15 a 30 imagens geradas e curadas de cada personagem, em ângulos variados, que viram uma LoRA por personagem. Para locações, a mesma coisa (LoRA de locação), ou referência multi-imagem no Qwen-Edit.

### 1.5 Aceleração no RTX 5090 (Blackwell sm_120)

- **Nunchaku (SVDQuant), Apache-2.0** (repo atual: `nunchux-ai/nunchaku`, v1.2+, com nós ComfyUI). Tem NVFP4 nativo no 5090, com **~3× sobre BF16** segundo o próprio projeto, e qualidade melhor que INT4. Suporta FLUX.1 (dev/schnell/Kontext/Krea), **Qwen-Image, Qwen-Image-Edit-2509 (+ Lightning 4/8 passos)**, **Z-Image-Turbo** (+20–30% na v1.2, com LoRA em nós nativos) e Sana. Dica: com o `ussoewwin/ComfyUI-QwenImageLoraLoader`, LoRAs funcionam nos Qwen e Z-Image do Nunchaku.
- **FP8 / NVFP4 nativo do ComfyUI**: os repacks Comfy-Org (fp8, int8 "ConvRot") rodam direto. O FLUX 3 Klein traz variante NVFP4 oficial.
- **Lightning / DMD / Turbo LoRAs** (lightx2v): Qwen-Image em 4 ou 8 passos é o maior ganho isolado (cerca de 6 a 12×).
- **torch.compile**, **Cache-DiT / TeaCache / First-Block-Cache**: mais 1,3 a 2× nos modelos de 20 a 50 passos. Ganham pouco nos Turbo de 4 a 8 passos.
- **TensorRT**: pouco vantajoso hoje para DiTs novos, porque o suporte chega tarde. Prefira Nunchaku ou FP8.
- **Requisitos do 5090**: PyTorch com CUDA 12.8+ (ideal **cu130**, torch ≥ 2.9), ComfyUI recente (≥ 0.42) e wheels do Nunchaku compiladas para sm_120. O ComfyUI portable atual já vem com cu130.

### 1.6 Mac M4

| Opção | Licença | Modelos | Uso sugerido |
|---|---|---|---|
| **mflux** (`mflux-community/mflux`, MIT, MLX) | MIT | **Z-Image, FLUX.2 klein, Qwen-Image / Edit, Boogu, ERNIE, MOSS, Krea 2, FLUX 3 Klein, SeedVR2** e outros; LoRA, ControlNet, inpainting | Melhor opção no Mac: previews, edições e upscale SeedVR2 em paralelo ao PC |
| **Draw Things** | App gratuito | FLUX, Qwen, Z-Image etc., com treino de LoRA embutido | GUI amigável |
| **DiffusionKit** (argmax, MIT) | MIT | SD3 / FLUX (parado desde abr/2025) | Não recomendado |
| ComfyUI em MPS | — | Funciona, mas é lento | Não recomendado |

Velocidade esperada no M4: algo como 15 a 60 s por imagem de 1 MP com Z-Image-Turbo ou klein 4B (depende de M4, Pro ou Max e da quantização). Isso é **10 a 20× mais lento que o 5090**. Use o Mac como estação secundária: edição, upscale e revisão.

---

## 2. Os detalhes de licença que realmente importam

1. **"Outputs liberados" ≠ "uso liberado".** As licenças BFL não comerciais (FLUX.1 dev, Kontext, FLUX.2 dev, klein 9B) dizem que você pode usar as *saídas* comercialmente. Mas o *acesso e uso do modelo* só vale para "Non-Commercial Purposes", e a FLUX NC v2.1 define que uso "for revenue-generating activity" **não** é não comercial. Num canal monetizado, gerar imagens com esses pesos é uso comercial do modelo. **Conclusão: compre a licença BFL ou fique nos Apache.**
2. **Qwen-Image-2.1 (set/2026) mudou para licença de pesquisa.** Não confunda com o Qwen-Image / 2512 / Edit-2511, que continuam Apache-2.0. Confira no card do HF a versão exata que baixar.
3. **Tetos de receita**: Krea 2 < US$ 1M (soma de **todas** as receitas da empresa e afiliadas, em 12 meses móveis); SD3.5 < US$ 1M; FLUX 3 Klein < US$ 5M; Hunyuan < 100M MAU e fora da UE/UK/KR. Se o negócio crescer, você perde o direito.
4. **InsightFace** (FaceID, PuLID, InfiniteYou, InstantID, ReActor): os modelos de face são **não comerciais**. Prefira consistência por LoRA e edição multi-ref (Qwen-Edit / klein 4B).
5. **Filtro de conteúdo e divulgação de IA** são exigidos por FLUX dev/NC, Krea 2 e Kommunity. Para doc no YouTube: marque o "conteúdo alterado/sintético" quando aplicável e revise as saídas manualmente.
6. **Finetunes do Civitai** herdam a licença da base e podem somar restrições. Use o filtro "commercial use" do Civitai e guarde print da licença.

---

## 3. Workflows ComfyUI sugeridos

### WF-1: "Batch de storyboard" (volume, Z-Image-Turbo)
```
CSV/JSON de planos (id, prompt, seed, personagem, locação)
  → [Load Diffusion Model: z_image_turbo (Nunchaku NVFP4 ou fp8)]
  → [LoRA Loader: dbcfilm_look 0.75] → [LoRA: personagem_X 0.8 (opcional)]
  → [Text Encode (Qwen3-4B)] com template fixo:
      "<descrição do plano>, cinematic 35mm film still, anamorphic, natural light,
       shallow depth of field, subtle film grain, <paleta do episódio>"
  → [Empty Latent 1344×768 (ou 1536×864)] → [KSampler: 8 passos, cfg 1, euler/simple]
  → [VAE Decode] → [Save Image com prefixo shot_id_seed]
```
- Gere 4 seeds por plano (batch 4) e escolha. Dirija com a API do ComfyUI (script Python lendo o CSV) para rodar a noite toda.
- Para mais diversidade de composição, use o **Z-Image (Base)** com 20–30 passos e CFG, ou ControlNet Union (Z-Image tem Union ControlNet) com esboço de pose ou profundidade.

### WF-2: "Hero shot" (Qwen-Image-2512 + Lightning)
```
[Qwen-Image-2512 fp8 ou Nunchaku] + [Lightning LoRA 8-step] + [LoRA film look treinada no Qwen]
  → KSampler 8 passos, cfg 1 → 1664×928 → upscale SeedVR2 até 4K
```
Use nos planos com muitos elementos, texto em cena (placas, jornais de época) ou composição exigente.

### WF-3: "Editar / trocar elemento / inpainting" (Qwen-Image-Edit-2511)
```
[Load Image (still)] (+ máscara opcional)
  → [TextEncodeQwenImageEditPlus: "replace the car with a 1970s Ford Galaxie, keep lighting"]
     ref2 = foto do personagem, ref3 = foto da locação (multi-ref)
  → [Qwen-Image-Edit-2511 Nunchaku + Lightning 4/8 passos] → KSampler
  → (opcional) [Inpaint Crop & Stitch] para editar só a região mascarada e preservar o resto em pixel
```
- Para edição rápida ou em lote, troque por **FLUX.2 klein 4B** (Apache, <1 s). Para o still final em 4K, use **BluePixel-Turbo**.
- Também serve para recompor um personagem em outro cenário: imagem do personagem + imagem da locação + "place the man from image 1 in the office from image 2, seated at the desk".

### WF-4: "Bíblia de personagens e locações" (consistência)
1. Gere de 1 a 3 retratos "canônicos" de cada personagem (frente, 3/4, perfil) com o WF-1.
2. Com o Qwen-Edit-2511, derive 20 a 30 variações: roupas, ângulos, luz.
3. Treine uma LoRA por personagem e por locação no Z-Image Base (ai-toolkit).
4. Na produção, empilhe film look + personagem (+ locação) no WF-1. Corrija os desvios com o WF-3 usando a imagem canônica como referência.

### WF-5: Pós
SeedVR2 (upscale 2×), depois grão de filme e LUT unificada (no ComfyUI com nós de film grain/LUT, ou no DaVinci). Isso amarra a consistência de cor entre modelos diferentes.

**Nós e pacotes úteis**: ComfyUI-nunchaku, ComfyUI-QwenImageLoraLoader, ComfyUI-Boogu, ComfyUI-DyPE (gera em 4K+ sem artefatos em Z-Image, Qwen e Flux), comfyui-inpaint-cropandstitch, ComfyUI-SeedVR2, rgthree e KJNodes.

---

## 4. Estimativa de imagens por hora (RTX 5090, ~1344×768)

| Configuração | s/imagem (est.) | Imagens/h | 200 stills ×4 variações (800 img) |
|---|---|---|---|
| Z-Image-Turbo **Nunchaku NVFP4**, 8 passos | ~1,5–2,5 | **1.400–2.400** | ~25–35 min |
| Z-Image-Turbo fp8/bf16, 8 passos + LoRA | ~2,5–3,5 | 1.000–1.400 | ~40–50 min |
| Boogu-Turbo, 4 passos | ~2–3 | 1.200–1.800 | ~30–40 min |
| FLUX.2 klein 4B (T2I ou edição) | ~0,6–1 | 3.600+ | <15 min |
| Qwen-Image-2512 Nunchaku + Lightning 8 passos | ~3–5 | 700–1.200 | ~45–70 min |
| Qwen-Image-2512 fp8, 50 passos (máxima qualidade) | ~35–45 | 80–100 | inviável em lote; só para heróis |
| Qwen-Edit-2511 Lightning (edição) | ~4–8 | 450–900 | — |
| Krea 2 Turbo (🟡 < US$ 1M) | ~8 | ~450 | ~1h45 |
| SeedVR2 upscale 2× (1 MP → 4 MP) | ~3–6 | 600–1.200 | 200 finais em ~15 min |

Os números são inferidos dos benchmarks medidos (3090: Z-Image 7,6 s, Boogu 5,5 s, Krea 14,8 s; 4090: Klein 10,2 s, Krea 12,6 s, Qwen-2.1 18,4 s, MOSS 27,6 s, Qwen-2512 112,7 s com streaming), escalados para o 5090, mais o ganho de ~3× do NVFP4 que o Nunchaku reporta. **Meça no seu hardware** antes de planejar prazos.

**Pipeline realista por vídeo (200 stills):** 800 gerações (4 por plano) + ~60 edições + 200 upscales ≈ **40 a 60 min de GPU**, contra ~US$ 8–40 por vídeo nas APIs pagas (ordem de grandeza). O gargalo passa a ser **curadoria humana**, não GPU.

---

## 5. Plano de adoção (2 semanas)

1. **Dia 1–2**: ComfyUI portable cu130 + Nunchaku (wheel para sm_120). Baixe Z-Image-Turbo, Qwen-Image-2512, Qwen-Image-Edit-2511 e as Lightning LoRAs, FLUX.2 klein 4B e SeedVR2.
2. **Dia 3**: A/B cego com 20 prompts reais do roteiro: Z-Image-Turbo × Boogu-Turbo × Qwen-2512-Lightning × (se estiver < US$ 1M) Krea 2 Turbo × (para referência) o atual GPT-Image/Seedream.
3. **Dia 4–6**: dataset e treino da LoRA "film look" no Z-Image Base, mais as LoRAs de 2 ou 3 personagens recorrentes.
4. **Dia 7–10**: script de lote via API do ComfyUI (CSV de planos → pastas por cena), WF-3 de edição e WF-5 de pós.
5. **Contínuo**: arquive a licença (print e hash) de cada peso e LoRA usada, mais o log de prompt e seed de cada still publicado.

---

## 6. Fontes (GitHub)

- Qwen-Image (Apache-2.0, notícias de 2512 / Edit-2511 / 2.0): `QwenLM/Qwen-Image` README
- Qwen-Image-2.1 (Qwen Research License, NC): `QwenLM/Qwen-Image-2.1` README + LICENSE
- FLUX.1 [dev] license (cláusulas de Outputs e Content Filters): `black-forest-labs/flux/model_licenses/LICENSE-FLUX1-dev`
- FLUX.2 (tabela de licenças; klein 4B Apache) + FLUX NC v2.1: `black-forest-labs/flux2` README + `model_licenses/LICENSE-FLUX-NON-COMMERICAL`
- FLUX 3 Image Klein (Kommunity; VRAM): `black-forest-labs/flux-3-image-klein` README. Termos resumidos em `sgl-project/sglang` docs, `invoke-ai/InvokeAI` starter_models/flux3.py e Civitai constants.ts
- Krea 2 Community License (< US$ 1M): `krea-ai/krea-2/docs/KREA-2-COMMUNITY-LICENSE`
- Tabela de licenças por base model: `civitai/civitai/src/server/common/constants.ts`
- Tencent Hunyuan license (Territory): `Tencent-Hunyuan/HunyuanImage-3.0/LICENSE`
- Z-Image: `Tongyi-MAI/Z-Image`; Boogu: `boogu-project/Boogu-Image`; MOSS: `OpenMOSS/MOSS-Image`; ERNIE: `baidu/ERNIE-Image`; HiDream-O1: `HiDream-ai/HiDream-O1-Image`; BluePixel: `vivo/BluePixel`
- Benchmarks: `Raigor2/local-inference-benchmarks` (RTX 3090) e `grawwww-studio/image-model-text-test` (RTX 4090, notas cegas, s/img e VRAM)
- Nunchaku: `nunchux-ai/nunchaku` (NVFP4 no 5090 ~3×; Z-Image / Qwen)
- mflux: `mflux-community/mflux`; Kolors: `Kwai-Kolors/Kolors/MODEL_LICENSE`; trainers: OneTrainer (AGPL), ai-toolkit (MIT)
