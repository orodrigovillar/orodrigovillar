# Lost Money Playbook — O que falta para rodar

## O que já está pronto
- `guide/The-Lost-Money-Playbook.pdf`: produto (12 páginas, fontes oficiais, 3 modelos de carta, tracker)
- `site/index.html`: página com quiz de 6 perguntas e oferta de US$ 9, histórias reais e garantia de 60 dias
- `creatives/ad-*.png`: 6 criativos 1080×1350 (re-gerar com foto: `node creatives/make.js`)
- `ads/ads.md`: 4 textos principais, headlines, prompts de foto para o GPT e estrutura da campanha
- `../../research/stories-unclaimed-money.md`: casos reais com links

## Cadastros (você faz, com seus documentos; NUNCA me mande senha)
1. **Hotmart** (hotmart.com): criar conta de Produtor e verificar identidade e conta bancária.
   - Cadastrar produto: E-book, moeda **USD**, preço **US$ 9**, idioma inglês, entregar o PDF via Hotmart.
   - Order bump: "Family Heir Search Kit" US$ 7 (eu escrevo assim que o produto principal for aprovado).
   - Aprovação do produto: normalmente de algumas horas a 2 dias úteis.
   - Copiar o link de checkout e me mandar. Eu troco `#CHECKOUT_URL` na página.
2. **Hospedar a página** (grátis): criar conta em netlify.com, arrastar a pasta `site/` e pronto. Domínio próprio .com custa ~US$ 10/ano e passa mais confiança (recomendado).
3. **Meta Business Suite** (business.facebook.com):
   - Criar BM nova, página do Facebook "The Lost Money Playbook" e conta de anúncios em **USD**, fuso America/New_York.
   - Criar Pixel, colar na página (marcado no código) e integrar o Pixel na Hotmart (evento Purchase).
   - Verificar o domínio da página na BM.
   - Cartão internacional cadastrado.
4. **Conector Adspirer Social Ads** em claude.ai → Configurações → Conectores, autorizando a conta de anúncios. Assim eu subo e acompanho as campanhas (sobem pausadas; você ativa).
5. **Fotos**: gerar as 6 fotos no seu GPT com os prompts de `ads/ads.md` e me mandar.

## A conta (projeção, não promessa)

| | US$ 9 | US$ 17 |
|---|---|---|
| Ticket médio (bump 30% × $7 + upsell 10% × $27) | $13,80 | $21,80 |
| Líquido após taxa Hotmart (~10%) e reembolso (~5%) | ~$11,70 | ~$18,50 |
| **CPA máximo para empatar** | **$11,70** | **$18,50** |
| CPA provável EUA (low ticket, tráfego frio) | $7–15 | $12–25 |
| Lucro por venda no CPA de $8 / $13 | ~$3,70 | ~$5,50 |

**Para R$ 10 mil/dia (~US$ 1.800 de lucro):** cerca de 330 a 490 vendas por dia em UMA oferta, com US$ 4–5 mil/dia de anúncio. Isso só se consegue escalando uma oferta já validada. O caminho real são **3 a 5 ofertas vencedoras rodando juntas**, cada uma dando US$ 300–600/dia.

**Plano de teste:** US$ 50/dia por 3–5 dias (≈ US$ 250 / R$ 1.400). Testar os preços US$ 9 e US$ 17. Se o ROAS ficar ≥ 1,8, escalar 20% a cada 48h. Se não chegar a 1,2 com US$ 250 gastos, trocar ângulo/criativo antes de colocar mais dinheiro.
