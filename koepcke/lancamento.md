# Pacote de lançamento — Juliane Koepcke (LANSA Flight 508, 1971) · Canal EN

> Instruções em português; todo texto voltado ao público em **inglês**.
> Fontes de verdade: `koepcke/roteiro.json` (18 segmentos) e `docs/BIBLIA_PRODUCAO.md` (seções 1, 2.4, 5, 6, 7).
> Duração real da narração (soma de `audio/s01..s18.mp3`): **14:12**. Timestamps abaixo vêm da soma das durações dos áudios, sem pausas entre segmentos nem title card. **São aproximados: recalcular após o render final.**
> Regra: só usar afirmações que estão no roteiro. Nada abaixo extrapola o roteiro.

---

## 0. Ações de edição antes do upload (gates da Bíblia)

1. **Elemento da thumbnail até 0:15 (Checklist 1).** Hoje o cold open usa `v1`, `k01`, `k02`, `k03`, `k04`. Nenhum desses é a base das thumbs abaixo. Inserir **`k27`** (fileira de assentos caindo) na frase *"She is still strapped into her seat…"* (s01, ~0:13). Se a thumb B vencer, inserir também um flash de **`k45`** em s02 *"…and only one shoe"* (~0:50). Se a thumb C vencer, mostrar `k38` por ~1 s em s01 *"Ninety-one of them would never come home"* (~0:26).
2. **Não usar `k58` em thumb nem em Short:** a garota aparece com mochila, que não existe no roteiro.
3. **`k38` mostra uma fuselagem à esquerda.** O roteiro diz que o avião se desintegrou, então cortar a fuselagem fora (ver thumb C).
4. **Upload não listado. Esperar o ícone verde de monetização (24–48 h) antes de agendar (Checklist 5).**
5. **Studio → "Altered or synthetic content" = YES.** Há recriações realistas de eventos reais e a narração é uma voz sintética (ElevenLabs).

---

## 1. Títulos (8 opções, ranqueados por potencial de clique)

Todos com menos de 60 caracteres. O nº de caracteres está entre parênteses. Todos são pagos no 1º minuto (s01 cobre queda, assento, 92/91, 11 dias e nome).

| # | Título | Por quê |
|---|---|---|
| 1 | **She Fell 10,000 Feet Into the Amazon. Then She Walked Out.** (58) | Fato impossível + segunda virada. Pago em s01/s07/s15. **Recomendado como título fixo do teste A/B.** |
| 2 | Her Plane Broke Apart. She Was Still Strapped to Her Seat. (58) | Imagem mental forte (contradição). Pago em s01/s06. |
| 3 | 17, Alone, One Shoe: 11 Days After Falling From the Sky (55) | Detalhes específicos e concretos geram curiosidade. Pago em s01/s02/s10. |
| 4 | 92 Boarded Flight 508. Only a 17-Year-Old Survived. (51) | Stat slam. Pago aos 0:23–0:28. |
| 5 | She Survived a 10,000-Foot Fall. Then the Ordeal Began. (55) | Loop aberto. Espelha a fala de s08 *"Juliane's ordeal was only beginning."* |
| 6 | Her Father's Advice Saved Her After a 10,000-Foot Fall (54) | Ângulo emocional/educativo. Pago em s02 e s10. |
| 7 | The Girl Who Fell From the Sky and Walked Out of the Amazon (59) | Ecoa o title card do vídeo (s01, ~0:28) e o livro dela. |
| 8 | The Only Survivor of LANSA Flight 508 \| Juliane Koepcke (55) | Título de busca (SEO). Bom para retestar depois de 90 dias como evergreen. |

Evitar: "2 miles" (3.000 m ≈ 1,86 mi), "world record" (o roteiro diz que o recorde é de Vulović) e qualquer termo gráfico.

---

## 2. Thumbnails — 3 conceitos para Test & Compare

Rodar com o **título #1 fixo** e as 3 thumbs como variações. O vencedor é decidido por watch-time share. Os três conceitos são deliberadamente diferentes: **céu/queda** vs. **pessoa/sobrevivência** vs. **objeto/local**. Saída em 1280×720. As fontes têm 1280×720, então todo crop precisa de upscale 2× (ex.: Real-ESRGAN) antes da arte final. Testar a leitura em 160×90 px.

### A — "A queda" · base `k27.png`
- **Imagem:** fileira de 3 assentos minúscula, com uma figura presa, no meio de nuvens de tempestade, com uma luz rompendo no canto superior direito.
- **Crop:** recortar ~45% do quadro (≈ x 330–910, y 60–390), deixando os assentos no terço esquerdo e a luz no terço direito. Os assentos devem ocupar ≥20% da altura final. Girar 8–10° para dar sensação de queda.
- **Texto (3 palavras):** **STILL IN HER SEAT**. Duas linhas, à direita, sobre a nuvem escura.
- **Cor/contraste:** dessaturar as nuvens para cinza-azulado frio. Texto branco com a palavra **SEAT** em laranja-fogo (#FF7A1A). Vinheta forte. Rim light quente sutil nos assentos para separá-los do fundo.
- **Por que deve vencer:** é a imagem impossível da história (cair sem avião) e se lê como uma pergunta em 0,5 s. Complementa o título (que fala em "fell") em vez de repeti-lo. Não tem nada gráfico.

### B — "A sobrevivente" · base `k45.png`
- **Imagem:** garota de costas, vestido rasgado, andando num riacho, **com uma sandália só**. Esse detalhe está no roteiro.
- **Crop:** ~60% do quadro (≈ x 250–1010, y 0–430 → reenquadrar até os pés). A figura fica no terço esquerdo e o pé com a sandália visível. Se o crop cortar os pés, usar a imagem inteira e fazer um zoom 115% centrado na figura.
- **Texto (4 palavras):** **11 DAYS. ONE SHOE.** à direita, empilhado.
- **Cor/contraste:** verde mais escuro e menos saturado no fundo (−30% saturação, −0,7 EV), pele e vestido mais quentes. Texto branco com **11 DAYS** em amarelo (#FFD400). Leve glow atrás do texto para separar do verde.
- **Por que deve vencer:** tem uma figura humana (rosto não é necessário) e transmite uma escala de tempo concreta. Atrai o público de "survival", que costuma ter AVD alto. O texto é um número específico e não repete o título.

### C — "1 de 92" · base `k38.png`
- **Imagem:** fileira de assentos no chão da floresta, ao amanhecer, com um assento vazio.
- **Crop:** **cortar fora a fuselagem à esquerda** (usar ≈ x 400–1280, y 80–720 e escalar para 16:9). Os assentos ficam centralizados à direita e o feixe de luz entra pela esquerda.
- **Texto (3 palavras):** **1 OF 92** em tipografia enorme, com o **1** em vermelho (#E02424) e "OF 92" em branco. Opcional: "SURVIVED" pequeno embaixo (total de 4 palavras).
- **Cor/contraste:** reduzir o musgo/verde nos assentos (eles parecem envelhecidos por anos). Granulação de arquivo, sombras mais frias, raio de sol dourado preservado.
- **Por que deve vencer:** é a fórmula "local isolado + número" da Bíblia (6.1 #3/#5). O stat slam gera a pergunta "quem foi o 1?". É a mais segura em compliance e funciona sem tradução nas faixas PT/ES (texto numérico universal, Bíblia 8.3).

---

## 3. Descrição do YouTube (colar como está)

> Os timestamps não podem ter "~" (isso quebra os capítulos). A aproximação é indicada no cabeçalho. Recalcular após o render.

```
Christmas Eve, 1971. LANSA Flight 508 breaks apart in a thunderstorm over the Peruvian rainforest. Ninety-two people were on board. One seventeen-year-old girl, Juliane Koepcke, fell roughly 10,000 feet still strapped into her row of seats, and survived. Then, injured, half blind and wearing one shoe, she spent eleven days alone in the Amazon, following a few words her father once told her.

This is the true story of how she got out.

CHAPTERS (approximate)
00:00 Falling, with no plane around her
01:00 The girl who knew the rules of the jungle
02:00 "Any other airline... but not LANSA"
02:48 Flight 508
03:20 The storm
04:01 10,000 feet
04:47 How did she survive?
05:48 Christmas morning, alone
06:35 Her father's rule
07:22 Walking in the water
08:08 The king vultures
08:46 One step, then another
09:31 Something on the riverbank
10:21 Voices
11:09 What the search teams found
11:52 "Why me?"
12:43 What really saved her

SOURCES
- LANSA Flight 508 (Wikipedia): https://en.wikipedia.org/wiki/LANSA_Flight_508
- Juliane Koepcke (Wikipedia): https://en.wikipedia.org/wiki/Juliane_Koepcke
- HowStuffWorks: https://history.howstuffworks.com/historical-figures/juliane-koepcke.htm
- ABC News (Australia), 2022: https://www.abc.net.au/news/2022-10-02/the-girl-who-fell-3km-into-the-amazon-and-survived/101413154
- CNN, 2009: https://edition.cnn.com/2009/WORLD/europe/07/02/germany.aircrash.survivor/
- Juliane Koepcke, "When I Fell From the Sky" (memoir, 2011)
- Werner Herzog, "Wings of Hope" (documentary)
- NPR, 2023 (Colombian Amazon children): https://www.npr.org/2023/06/16/1182630213/how-4-children-lost-in-the-amazon-jungle-for-40-days-were-able-to-stay-alive
- ExplorersWeb: https://explorersweb.com/juliane-koepckes-impossible-peruvian-survival/
- Today I Found Out: https://www.todayifoundout.com/index.php/2012/04/a-17-year-old-girl-survived-a-2-mile-fall-without-a-parachute-then-trekked-alone-10-days-through-the-peruvian-rainforest/

AI DISCLOSURE
The visuals in this documentary are realistic AI-generated recreations, not archival footage or photographs of the real people, aircraft or locations. The narration uses a synthetic (AI) voice. All facts are drawn from the sources listed above.

#JulianeKoepcke #SurvivalStory #TrueStory
```

---

## 4. Tags (15)

```
Juliane Koepcke, LANSA Flight 508, girl who fell from the sky, plane crash survivor, Amazon survival story, true survival story, Peru plane crash 1971, sole survivor plane crash, survived fall without parachute, Wings of Hope Werner Herzog, When I Fell From the Sky, Panguana, Lockheed Electra crash, rainforest survival, survival documentary
```

---

## 5. Shorts / Reels (6 cortes, 30–58 s)

Specs (Bíblia 7.3): 9:16, 1080×1920, hook de texto no topo da zona segura no frame 1, legenda palavra a palavra, hit sonoro no frame 1 e **related video → vídeo longo**. Tempos são relativos ao início do segmento (`audio/sNN.mp3`, medidos em `words/sNN.json`). **Nenhum corte inclui a descrição da ferida/larvas (s13, s14) nem a cena dos passageiros mortos (s12):** em um Short, fora de contexto, esses trechos perdem a proteção EDSA.

Ordem de publicação sugerida: **#1 e #3 entre 24 e 48 h antes** do vídeo longo (teasers). Os outros 4 saem ao longo de 7–14 dias depois.

### Short 1 — "Not inside an airplane" · s01 · **~37 s**
- **Início:** s01 3.3 s, *"Somewhere above the Peruvian rainforest, a seventeen-year-old girl is falling."*
- **Fim:** s01 40.6 s, *"…is one of the most extraordinary survival stories ever told."*
- **Hook na tela (0–1 s):** `There was no plane anymore. She was still falling.`
- **Loop:** termina em "…ever told." sobre o mesmo plano de `k27` (assentos caindo) que abre o Short. A primeira frase ("Somewhere above… a girl is falling") volta a começar sem emenda.

### Short 2 — "Fire on the wing" · s06 → s07 · **~44 s**
- **Início:** s06 17.8 s, *"Through the window, Juliane saw flashes of lightning all around them."*
- **Fim:** s07 20.3 s, *"She could see the forest below her, turning in circles, like a sea of green."*
- **Hook na tela:** `Her mother said: "This is the end."`
- **Loop:** termina no plano girando sobre a floresta (`k28`/`k02` com spin). O raio do início do Short corta direto sobre o giro, como se a queda recomeçasse. Hit seco no corte.

### Short 3 — "How did she survive?" · s08 · **~37 s**
- **Início:** s08 0.0 s, *"How did she survive?"*
- **Fim:** s08 37.4 s, *"But it was real."*
- **Hook na tela:** `No one can say for certain how she survived this.`
- **Loop:** "But it was real." → "How did she survive?" é um loop perfeito de pergunta e resposta. Usar o mesmo plano (`k32` girando) no fim e no início.

### Short 4 — "Her father's rule" · s10 · **~40 s**
- **Início:** s10 7.4 s, *"And she knew, from everything her parents had taught her, that waiting in the jungle could mean dying in the jungle."*
- **Fim:** s10 47.1 s, *"…seventeen-year-old Juliane Koepcke started walking."*
- **Hook na tela:** `Lost in the Amazon at 17. Her dad had told her one rule.`
- **Loop:** termina em "started walking" com o card `FIND WATER. FOLLOW IT DOWNSTREAM.` ainda na tela. O início ("waiting… could mean dying") volta como o motivo da regra.

### Short 5 — "They couldn't see her" · s11 · **~45 s**
- **Início:** s11 0.0 s, *"She walked in the water whenever she could."*
- **Fim:** s11 45.1 s, *"And then it stopped completely."*
- **Hook na tela:** `She could hear the search planes. They couldn't see her.`
- **Loop:** "And then it stopped completely." → 0,5 s de silêncio (só som de água) → "She walked in the water…". Ela continua andando e o ciclo recomeça.

### Short 6 — "A boat" · s14 + s15 (com 1 jump cut) · **~49 s**
- **Parte A:** de s14 0.0 s *"Then, on the tenth day, almost at the end of her strength, she saw something on the riverbank that did not belong to nature."* até s14 15.1 s *"People had been here."*
- **Jump cut** (pula a parte do combustível na ferida) **→ Parte B:** de s14 41.4 s *"She could have taken the boat."* até s15 24.4 s *"…that they wondered if she might be some kind of water spirit."*
- **Hook na tela:** `Day 10 alone in the Amazon. Then she found a boat.`
- **Loop/cliffhanger:** termina em "water spirit" sobre `k65`/`k64`. A pergunta implícita ("ela é real?") leva de volta ao "Day 10" do hook, e o related video entrega o resto.

---

## 6. Comentário fixado

```
Her father's rule, the one that got her out:
"Find water. Follow it downstream. A small stream will lead to a bigger stream. A bigger stream will lead to a river. And rivers lead to people."

Luck kept her alive in the air. Knowledge kept her alive on the ground.
Which one do YOU think mattered more? And what's the one survival rule someone taught you that you've never forgotten? 👇
```

(O emoji é opcional. Se o canal não usa emoji, remover.)
