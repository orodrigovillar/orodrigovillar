# Memória completa da sessão na nuvem (15/11/2026)

> Para o Claude do PC: este arquivo é a memória da conversa entre o dono e o Claude da nuvem.
> A partir de agora **você é o responsável principal pela operação**. Leia junto com `HANDOFF.md`.
> Em conflito, vale o que o dono disser por último a você diretamente.

## 1. Quem é o dono e como ele gosta de trabalhar
- Fala português (Brasil), escreve rápido e informal. Responder em PT-BR, direto, sem enrolação.
- Quer **automação máxima** e tudo entregue pronto; gosta de ver muitos agentes trabalhando em paralelo.
- Quer **qualidade máxima com custo mínimo**. Achou caro R$125/vídeo. Meta: quase de graça usando o PC.
- Tem: PC com **RTX 5090** (Windows, pasta `TIO CLAUDIO` = apelido carinhoso para o Claude), **Mac M4**,
  assinatura **ElevenLabs Pro** (600k créditos/mês), ChatGPT. Pode deixar os PCs ligados 24h.
- Prioriza **não ter problema de direitos autorais**. Pediu cuidado explícito.
- **Amou a amostra D.B. Cooper** ("NÃO! EU AMEIIII", "ficou perfeito"). É o padrão de qualidade.

## 2. Linha do tempo das decisões
1. Ideia: canal de documentários bem produzidos, monetizado, "no automático".
2. Idioma: **inglês** (RPM muito maior). Português depois, eventualmente.
3. Três canais (um por nicho): **crimes & mistérios** (primeiro), história, dinheiro & negócios.
4. Ritmo desejado: até 2 vídeos/dia **todos diferentes e autênticos** (não template). Alertado sobre a regra
   "inauthentic content" do YouTube (jul/2025) → começar com 5 vídeos de teste e medir.
5. Nome do canal: **ainda não definido** (o dono preferiu provar a qualidade primeiro).
   Sugestões antigas: The Cold Archive, Unsealed Files, Midnight Dossier, Case Vanished.
6. Amostra de 3 min em PT-BR feita na nuvem (ver `dbcooper-amostra/`). Aprovada.
7. Custos: amostra ~20k créditos ElevenLabs (~US$3,30). Vídeo completo de 22 min só com ElevenLabs ≈ US$23 (~R$125).
   Conclusão honesta dada ao dono: **não compensa pagar isso agora** (canal sem monetização até 1.000 inscritos +
   4.000 h em 12 meses). Fazer os 5 testes quase de graça.
8. Voz: primeiro o dono disse "pode usar ElevenLabs no PC" para qualidade. Depois (no PC) pediu **voz grátis**.
   No teste cego PT-BR só o ElevenLabs passou; VoxCPM2 e Qwen3 reprovados (Qwen com sotaque de Portugal).
   Em teste: Gemini 3.8 Flash TTS (grátis; Google usa dados p/ treino) e Fish Audio Drama 3 local (grátis < US$500k/ano).
   **Regra prática:** se nenhuma grátis empatar, usar ElevenLabs só na narração (já pago na assinatura) e o resto grátis.
9. ElevenLabs: o dono exige **sempre 1 take** (generations_count=1), nunca 2.
10. Imagens: local na 5090 (Z-Image-Turbo / Qwen-Image). ChatGPT pode ser usado à mão para poucas imagens-chave
    (não automatizar a interface do ChatGPT — viola os termos; API é paga à parte).
11. Vídeo IA: local (Wan 2.2 Apache é o principal). Usar o que já está instalado se tiver licença comercial.
12. Primeiro vídeo a publicar sugerido: **D.B. Cooper** (55 anos do caso em 24/11/2026). O PC começou pelo Antwerp — ok.

## 3. Estilo aprovado (o que fez a amostra funcionar)
- Abertura com tempestade + trovão antes da voz; card de data em máquina de escrever.
- Narrador grave e calmo (ElevenLabs "Nassif", eleven_v4); frases curtas; pausas.
- Imagens cinematográficas 35mm, teal & amber, grão pesado; letterbox; vinheta.
- Cortes a cada 3–6 s ancorados nas palavras da narração; dissolves curtos; cortes secos nos momentos de impacto.
- Gráficos: título grande (Bebas Neue) com linha vermelha; carimbo vermelho; contadores de dinheiro;
  mapas animados escuros com rota vermelha; bilhete manuscrito; cards pretos de "punch" ("NEM CORPO.").
- Legendas queimadas palavra-a-palavra (Inter), trilha tensa com ducking, SFX (trovão, vento, cabine, máquina de escrever).
- Final com gancho ("E é aqui que a história fica estranha...") + "CONTINUA...".
- Tudo isso está implementado em `dbcooper-amostra/scripts/render.py`.

## 4. Regras de direitos autorais e políticas (resumo dos relatórios)
- Proibido: trechos de filmes, telejornais, documentários, vídeos de outros canais, música comercial.
- Não existe "trecho curto liberado" — Content ID pega trechos curtos.
- Arquivo público: obras do governo federal dos EUA (FBI, NARA, NASA) são domínio público — mas imagens de terceiros
  dentro delas podem não ser; logos da NASA não são PD. Já houve claims falsos do Content ID em material PD → guardar prova.
- British Pathé é pago. Free Music Archive: só CC0/CC BY (nunca NC/ND). Pixabay Music tem risco de claim.
- Música mais segura: gerada por nós (ACE-Step local ou drones por código) + YouTube Audio Library ("attribution not required").
- SFX: `wyzowl/sfx-kit` (CC0), síntese ffmpeg, Freesound filtrado CC0. BBC SFX é não comercial.
- IA: marcar "conteúdo alterado/sintético" em cenas realistas; **nunca** recriar com IA rosto de vítima/suspeito real;
  "suspeito/acusado" para quem não foi condenado; fonte para cada afirmação (planilha `*_fontes.md`).
- Imagens 100% IA não têm copyright nos EUA (podemos usar, mas não "somos donos" exclusivos).
- Modelos com pesos NÃO comerciais: F5-TTS, XTTS-v2, Spark-TTS, Higgs v3, Fish S2-Pro, FLUX dev/Kontext/FLUX.2 dev,
  Qwen-Image-2.1, MusicGen/MAGNeT/JASCO, MMAudio, AudioLDM2, DA-V2 Base/Large; Hunyuan/FramePack/SkyReels V1 excluem UE/UK.
- Facebook: monetização por convite; rótulo "AI info" para realismo; repostar conteúdo próprio do YouTube é permitido.

## 5. Mercado (resumo dos relatórios em `docs/pesquisa/`)
- Referências true crime/mistério: LEMMiNO, JCS, Wendigoon, Nexpo, Barely Sociable, Lazy Masquerade, Fascinating Horror,
  Coffeehouse Crime, Bedtime Stories. Padrões: poucos vídeos muito bons > volume; abrir pelo clímax; título com
  transformação dramática + nome próprio; thumbnail com 1 sujeito escuro e 1 cor de destaque.
- Canais IA que caíram: os que inventaram fatos/metadados ou repetiram template. Sobreviveu quem agrega valor.
- YouTube Data API: ~6 uploads/dia por projeto; pedir auditoria cedo para agendar.
- Dublagem multi-idioma: para canal novo, canal separado por idioma parece melhor que faixas de áudio.

## 6. Próximos passos combinados
1. Dono escolhe a voz EN (teste cego Gemini / Drama 3 / ElevenLabs).
2. Produzir o vídeo 02 Antwerp (roteiro já verificado: `02_antwerp_heist_final.md`), no estilo da amostra, tudo local.
3. Mostrar ao dono antes de seguir. Depois: 01 D.B. Cooper (publicar perto de 24/11), 03, 04, 05.
4. Thumbnails (template PIL), títulos/descrições, upload "não listado" para checar Content ID antes de publicar.
5. Continuar pesquisando ferramentas grátis melhores e registrar em `docs/pesquisa/achados.md`.
6. O Claude da nuvem continua disponível como revisor/consultor; ele recebe mensagens do PC.
