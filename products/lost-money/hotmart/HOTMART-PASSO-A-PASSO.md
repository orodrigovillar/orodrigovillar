# Hotmart: cadastro dos 4 produtos (passo a passo)

Use a sua conta normal da Hotmart (a mesma conta serve para ser Produtor).
Os nomes de menus da Hotmart mudam às vezes; se algum estiver diferente, procure o equivalente.

## 0. Antes de tudo (uma vez só)
1. Entre em **app.hotmart.com**.
2. Confira se a conta está **verificada** (documento + dados bancários em *Minha Conta → Dados bancários*). Sem isso, a Hotmart não libera os saques.

---

## 1. Os 4 produtos

Para CADA produto: menu **Produtos → Cadastrar produto → E-book** e preencha:

| Campo | Produto 1 | Produto 2 | Produto 3 | Produto 4 |
|---|---|---|---|---|
| **Nome** | The Lost Money Playbook | Family Heir Search Kit | The 50-State Speed Kit | 50-State Speed Kit Lite |
| **Papel no funil** | Principal | Order bump | Upsell | Downsell |
| **Preço** | **US$ 9** | **US$ 7** | **US$ 27** | **US$ 17** |
| **Idioma** | Inglês | Inglês | Inglês | Inglês |
| **Categoria** | Finanças e Investimentos (ou Educacional) | igual | igual | igual |
| **Imagem** | cover-1-playbook.png | cover-2-heir-kit.png | cover-3-speed-kit.png | cover-4-speed-kit-lite.png |
| **Arquivo entregue** | The-Lost-Money-Playbook.pdf | Family-Heir-Search-Kit.pdf | 50-State-Speed-Kit.pdf **+** 50-State-Speed-Kit.xlsx | 50-State-Speed-Kit.xlsx |
| **Garantia** | o maior prazo que a Hotmart permitir | igual | igual | igual |

**Moeda (importante):** ao criar a **Oferta/Preço** de cada produto, escolha a moeda **USD (Dólar)** e deixe ativado **vender para outros países / vendas internacionais**.

**Página de vendas (campo "URL da página de vendas"):** deixe em branco por enquanto ou use `https://example.com`. Eu te passo o link do site assim que ele estiver no ar.

### Descrições (copie e cole)

**Produto 1: The Lost Money Playbook**
> The complete 30-minute method to search every official place where unclaimed money in your name or your family's could be: all 50 states, name variations, deceased relatives and 7 federal sources (IRS refunds, savings bonds, pensions, back wages, FHA refunds, failed banks, VA insurance). Includes 3 ready-to-send letter templates and a printable Search Tracker. Independent educational guide, not affiliated with any government agency. Official searches and claims are always free. Results vary.

**Produto 2: Family Heir Search Kit**
> How to find, and claim, money a parent, grandparent or spouse left behind: the relative profile, the paperwork clues that reveal hidden accounts, the heir search circuit, the documents heirs usually need, and 3 letter templates for banks, employers and state programs. Educational guide, not legal advice.

**Produto 3: The 50-State Speed Kit**
> Every state's official unclaimed property program (NAUPA directory) in one place, plus the 3-layer search plan, the claim document checklist, the re-check calendar and a ready-to-use tracking spreadsheet for all 50 states + D.C.

**Produto 4: 50-State Speed Kit Lite**
> The ready-to-use spreadsheet with every state's official unclaimed property program link (NAUPA directory) and columns to track searches, amounts, claim numbers and follow-ups. Federal sources and family search tabs included.

---

## 2. Order bump (Produto 2 dentro do checkout do Produto 1)
Menu **Ferramentas → Order Bump** (ou dentro do Produto 1 → *Checkout → Order Bump*):
- Produto principal: **The Lost Money Playbook**
- Produto do bump: **Family Heir Search Kit**, US$ 7
- Título do bump: **YES, add the Family Heir Search Kit for just $7**
- Descrição do bump: **Find and claim money a parent or grandparent left behind: documents, clues and letter templates.**

## 3. Funil: upsell e downsell de 1 clique
Menu **Ferramentas → Funil de vendas** (pode aparecer como "Upsell" ou "One Click Upsell"):
1. Produto inicial: **The Lost Money Playbook**
2. Depois da compra → **Upsell: The 50-State Speed Kit** (US$ 27). Página: `upsell.html` do nosso site.
3. Se recusar → **Downsell: 50-State Speed Kit Lite** (US$ 17). Página: `downsell.html`.
4. Final → página de obrigado: `thanks.html`.
5. A Hotmart gera um **código/widget** para colar nas páginas de upsell e downsell → **copie e me mande**.

## 4. O que me mandar depois
1. **Link do checkout** do The Lost Money Playbook (em *Produto → Links* ou *Ofertas*)
2. **Código do widget** do upsell e do downsell (do Funil de vendas)
3. O **prazo de garantia** que a Hotmart deixou escolher (eu ajusto a página)

Nunca me mande senha. Só esses links e códigos.

---

## Para o seu agente de IA (instrução direta)
> Log into the user's Hotmart producer account (user handles login/2FA). Create 4 e-book products exactly as in the table above (names, USD prices, English, descriptions, cover images, delivery files). Set each offer's currency to USD with international sales enabled. Configure an Order Bump on "The Lost Money Playbook" with "Family Heir Search Kit" ($7). Create a Sales Funnel: Playbook → upsell "The 50-State Speed Kit" ($27) → if declined, downsell "50-State Speed Kit Lite" ($17) → thank-you page. Return: the Playbook checkout URL, the funnel widget code(s), and the guarantee period set. Do not change account, bank or payout settings.
