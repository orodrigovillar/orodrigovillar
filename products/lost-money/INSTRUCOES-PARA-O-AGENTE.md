# LOST MONEY PLAYBOOK — Instruções completas para o agente

Objetivo: colocar no ar um funil de produto digital (e-book em inglês, público EUA) e rodar anúncios no Meta.
Siga as etapas NA ORDEM. Cada etapa diz o que entregar ao final.

## Estrutura do pacote
```
hotmart/        -> passo a passo da Hotmart + 4 capas (600x600)
guide/          -> os produtos: 3 PDFs + 1 planilha .xlsx
site/           -> o site pronto (index, upsell, downsell, thanks, privacy, terms + img/)
creatives/      -> 6 anúncios estáticos (ad-*.png) e 3 vídeos (video/ad-video-*.mp4)
ads/ads.md      -> textos dos anúncios + estrutura da campanha
emails/         -> 2 sequências de e-mail (leads e compradores)
```

## Regras que NÃO podem ser quebradas (derrubam conta)
- Não inventar depoimentos, números ou histórias. Os 3 depoimentos e as 6 histórias da página são reais, não alterar.
- Não prometer que a pessoa VAI achar dinheiro. Não usar logo/nome de governo como se fosse oficial.
- Não usar cloaking (página diferente para o Meta).
- Não alterar dados bancários, de saque ou de segurança das contas.

---

## ETAPA 1 — Hotmart (produtos, bump, funil)
Siga `hotmart/HOTMART-PASSO-A-PASSO.md` exatamente (4 produtos em USD, order bump, funil upsell/downsell).
**Entregar:** (a) link de checkout do "The Lost Money Playbook"; (b) código/widget do funil para upsell e downsell; (c) prazo de garantia configurado.

## ETAPA 2 — Colocar os links nos arquivos do site
Abrir os arquivos da pasta `site/` num editor de texto e substituir:

| Procure por | Substitua por | Arquivo(s) |
|---|---|---|
| `#CHECKOUT_URL` | link de checkout do Playbook (Etapa 1a) | index.html (todas as ocorrências) |
| `<div id="hotmart-sales-funnel"></div>` + o botão `#HOTMART_UPSELL_ACCEPT_URL` logo abaixo | o widget do upsell (Etapa 1b) | upsell.html (aparece 2 botões; trocar os dois ou remover e deixar só o widget) |
| `#HOTMART_DOWNSELL_ACCEPT_URL` e o div do funil | o widget do downsell | downsell.html |
| `support@YOURDOMAIN.com` | o e-mail de suporte real | index.html, thanks.html, privacy.html, terms.html |
| `<!-- META PIXEL: cole aqui ... -->` | o código base do Pixel do Meta (Etapa 4) | index, upsell, downsell, thanks |
| `MAILERLITE_FORM_ACTION_URL` | URL "action" do formulário do MailerLite (Etapa 5) | index.html |

Se a garantia da Hotmart for menor que 60 dias: trocar "60-day"/"60-Day"/"60 days" pelo prazo real em index.html, upsell.html e terms.html.

## ETAPA 3 — Publicar o site (grátis)
1. Criar conta em **app.netlify.com** (login com Google).
2. **Add new site → Deploy manually** → arrastar a pasta `site/` inteira.
3. Em **Site configuration → Change site name**: `lostmoneyplaybook` (ou o mais próximo disponível) → endereço final `https://lostmoneyplaybook.netlify.app`.
4. Testar no celular: fazer o quiz, pular o e-mail, clicar no botão de compra → deve abrir o checkout da Hotmart.
5. Voltar na Hotmart e preencher a **URL da página de vendas** com esse endereço; no funil, usar `.../upsell.html`, `.../downsell.html`, `.../thanks.html`.
(Opcional depois: comprar domínio .com ~US$10/ano e ligar na Netlify em *Domain management*.)
**Entregar:** URL do site.

## ETAPA 4 — Meta (BM, conta de anúncios, Pixel)
1. business.facebook.com → criar **BM** → criar **Página do Facebook** "The Lost Money Playbook" (foto: `hotmart/cover-1-playbook.png`).
2. **Conta de anúncios**: moeda **USD**, fuso **America/New_York** (não dá para mudar depois) + cartão.
3. **Events Manager → Conectar dados → Web → Pixel**. Copiar o código base e colar nas páginas (Etapa 2). Republicar o site na Netlify (arrastar a pasta de novo).
4. Na Hotmart: **Ferramentas → Pixel de rastreamento** → adicionar o ID do Pixel do Meta no produto (dispara Purchase).
5. Na BM: **Segurança da marca → Domínios** → verificar o domínio (se usar domínio próprio).

## ETAPA 5 — MailerLite (e-mails automáticos, grátis)
1. Criar conta em mailerlite.com.
2. **Forms → Embedded form** com campos `name` e `email` + 2 campos ocultos `quiz_score` e `quiz_answers`. Copiar a URL do "action" e colar no index.html (Etapa 2).
3. **Automations**:
   - "Leads": gatilho = entrou no formulário → 5 e-mails de `emails/leads-sequence.md` (dias 0, 1, 2, 4, 6). Parar a automação se a pessoa comprar.
   - "Compradores": gatilho = compra (integração Hotmart → MailerLite, ou importar compradores) → 5 e-mails de `emails/buyers-sequence.md` (dias 0, 1, 3, 5, 10).
   - Trocar `{{checkout_url}}` pelo link de checkout e `{{playbook_url}}` pelo link de acesso da Hotmart.

## ETAPA 6 — Campanha no Meta (teste)
Seguir `ads/ads.md`. Resumo:
- **1 campanha** Objetivo **Vendas**, evento **Purchase**, orçamento **CBO US$ 50/dia**.
- Público: **Advantage+ amplo**, Estados Unidos, 35–65+, todos os gêneros. Posicionamentos Advantage+.
- **3 conjuntos**, cada um com o link certo (o `?s=` muda o topo da página para combinar com o anúncio):

| Conjunto | Criativos | Texto | URL de destino |
|---|---|---|---|
| Florida | `video/ad-video-01-florida-108k.mp4` + `ad-01-name.png` + `ad-06-billions.png` | Texto D + Texto A | `https://SEUSITE/?s=fl` |
| Colorado | `video/ad-video-02-colorado-30k.mp4` + `ad-03-moved.png` + `ad-04-ignore.png` | Texto C + Texto A | `https://SEUSITE/?s=co` |
| Heirs | `video/ad-video-03-heirs-ohio.mp4` + `ad-02-parents.png` + `ad-05-bonds.png` | Texto B | `https://SEUSITE/?s=oh` |

- Botão do anúncio: **Learn More**. Criar tudo **PAUSADO**, revisar, e só então ativar.
- **Não mexer por 3 dias.** Depois: conjunto que gastou US$ 30 sem venda → pausar. ROAS ≥ 1,8 por 3 dias → +20% de orçamento a cada 48h.


### Teste A/B das páginas (claro x escuro)
- **Versão A (clara):** `https://SEUSITE/?s=fl` (index.html)
- **Versão B (preta e dourada):** `https://SEUSITE/b.html?s=fl`
- Duplicar cada conjunto: um anúncio aponta para A, a cópia idêntica aponta para B (trocar só a URL). Mesmo orçamento.
- Depois de 3–5 dias, comparar **custo por compra** de A vs B. Ficar com a vencedora e pausar a outra.
- Os links de checkout, Pixel e e-mail precisam ser trocados nos DOIS arquivos (index.html e b.html).

## ETAPA 7 — Relatório
A cada 3 dias, exportar do Gerenciador de Anúncios (por anúncio): gasto, impressões, CTR, custo por clique, compras, custo por compra, ROAS. Mandar esses números para análise e decisão do que cortar e escalar.

---
## Checklist final (marcar)
- [ ] 4 produtos na Hotmart em USD + bump + funil
- [ ] Links trocados nos arquivos do site
- [ ] Site no ar e testado no celular (quiz → checkout)
- [ ] Pixel instalado no site e na Hotmart
- [ ] MailerLite com as 2 automações
- [ ] Campanha criada PAUSADA com os 3 conjuntos
- [ ] Campanha ativada
