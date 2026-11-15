# Conversion Audit: Lost Money Playbook funnel (`site/index.html`)

Audited 2026-11-15. Rendered at 390x844 with Playwright (quiz → 6 answers → "Skip" → result + offer). Files read: `site/index.html`, `site/upsell.html`, `site/downsell.html`, `guide/guide.html`, `ads/ads.md`, `creatives/video/*.json`, `research/stories-unclaimed-money.md`, `SETUP.md`.

Nothing was edited except this file.

---

## 1. Overall score: **5.8 / 10**

| Framework | Raw score | /10 | One-line verdict |
|---|---|---|---|
| Landing Page Doctor (14 checkpoints) | 78/140 (56%, grade D) | 5.6 | Clean, honest, mobile-perfect quiz. Weak on trust, showing the product and getting to the CTA. |
| Hormozi Value Equation | 58/100 | 5.8 | Strong on speed (30 min, instant PDF). **Perceived Likelihood** is the weakest lever: the offer never shows *why this reader* should expect to find something. |
| RyMac paid-traffic gate (8 checks) | 4.5/8 passed | 5.5 | The quiz step is a good "one decision". The offer step breaks the rule: price and first CTA sit ~4 screens below the result. |
| Copy Thief (awareness / message match) | n/a | 6.5 | Right ladder for cold traffic (problem → proof → mechanism → offer). The page loses the specific story the ad told, and the mechanism comes too late and is too thin. |

**What's already good (keep it):** honest disclaimers everywhere ("many people find nothing", "$0 to claim officially", "not a government service"). Real, sourced news stories. A quiz as the first micro-commitment. One clear goal per step. Fast and self-contained (no web fonts, no images). Perfect mobile layout. A 60-day guarantee. For this niche, the compliance stance is a real conversion asset, so don't trade it away.

**Where the money is leaking, in one sentence:** the visitor finishes the quiz on a high and gets a generic "5/6". Then they scroll ~3,200px (≈4 phone screens) of education before they see what the product is, what it looks like, or a button. When they get there, nothing ties their quiz answers to the $9 purchase.

Measured positions in the offer state (390px wide, full page height 4,549px): result card at y≈376. Price at y=3,416. **First CTA at y=3,564.** Second CTA at y=4,207.

---

## 2. Framework scoring detail

### 2a. Landing Page Doctor: 78/140 (56%, D)
Page type C (consumer). Brand maturity: 🔴 Unknown (cold Meta traffic, new brand). Under that rule, trust (C) and CTA path (D) are "make or break".

| # | Checkpoint | Score | Why |
|---|---|---|---|
| 1 | Headline value prop | 6 | "you", 9 words, no jargon. No number, no verb. |
| 2 | 5-second clarity | 8 | Clear quiz. -2 reality check: "check" + "money in your name" can read as a name/records search, but it's a risk-factor quiz. |
| 3 | Audience anchoring | 6 | Good scenarios (parent's insurance, savings bonds as a kid). No who-it's-for line, no proof from people like them on the first screen. |
| 4 | First-screen density | 8 | Bar + kicker + H1/sub + quiz. A single target. |
| 5 | CTA visibility | 6 | The quiz options are the CTA. They start at y≈520 (lower half) and are white-on-white, not the most prominent element. |
| 6 | CTA copy | 6 | "Answer 6 quick questions" + "60-second" are good. Nothing near the quiz says "free / no sign-up to start". |
| 7 | Commitment reduction | 4 | "Free" never appears above the fold, and there's no "no sign-up" line. Only the time cue. |
| 8 | Trust anchors | 1 | Only the $70B stat on the first screen. The real news stories live ~2,000px down. |
| 9 | Trust authenticity | 2 | The stories are verifiable (named outlets), but invisible until late. |
| 10 | Product visualization | 1 | There is no image of the Playbook anywhere on the page, even though a real 12-page PDF exists. |
| 11 | Pricing visibility | 8 | $9 is clear and one-time, and free official claims are explained. It's hidden until after the quiz, which is acceptable for a quiz funnel. |
| 12 | CTA path consistency | 4 | The two CTAs use different words. "YES, SHOW ME WHERE TO LOOK" sounds like more content, not checkout. `#CHECKOUT_URL` is still a placeholder. Footer links go to `#`. The 2nd CTA doesn't fire InitiateCheckout. |
| 13 | Mobile | 10 | No overflow, 17px options, full-width buttons. |
| 14 | Readability | 8 | The subheadline runs 4 lines on mobile. |

Interpretation (🔴 Unknown brand): checkpoints 7, 8, 9, 10 and 12 are all under 5. ⚠️ High risk: cold traffic gives no second chance. The fixes for 8 and 10 cost nothing, because the assets already exist (the stories, the PDF).

### 2b. Hormozi Value Equation: 58/100
| Lever | Score | Reasoning |
|---|---|---|
| Dream Outcome | 14/25 | The desire ("money in my name / my parents left behind") is strong and well named. The offer itself is framed as a method ("complete 30-minute method to search every place"), not the outcome ("know for sure you've checked everywhere"). |
| Perceived Likelihood | **11/25 (weakest)** | Real stories prove the phenomenon, not that *this reader* will find something or that the *Playbook* helps. There's no buyer proof yet (new product, and none should be invented). The quiz result is generic. "Why pay if it's free?" is answered only in a collapsed FAQ. |
| Time Delay | 18/25 | Instant PDF and a "30-minute" search are excellent. Claims take weeks to months; that's honestly omitted and fine. |
| Effort & Sacrifice | 15/25 | DIY, but with templates and a tracker. The page *tells* you it's easy and never *shows* it (no preview of the tracker, templates or checklist). |

Grand Slam enhancement check:
- Scarcity: none. Correct, don't add any.
- Urgency: **"Launch price" is weak and unbacked.** It implies a price rise that isn't scheduled. Remove it, or make it true with a dated, enforced change.
- Bonuses: none are named on the offer. The lead magnet ("3 places to search first") and the Search Tracker could be framed as included tools. No dollar values may be invented.
- Guarantee: 60-day unconditional. Good, but it has no name and sits *below* the CTA instead of next to it.
- Naming (M.A.G.I.C.): "The Lost Money Playbook" has the Magnetic and Container parts. It's missing Goal and Timeframe, yet the PDF cover already has them: **"The 30-Minute Search Method"**. Use it as the subtitle.

### 2c. RyMac paid-traffic gate: 4.5/8
| Check | Result |
|---|---|
| H1 restates the ad promise | ½. Matches ad A / video 02's end card ("Is there money in your name?"). Doesn't match the story ads (FL $108k, CO $30k, OH heirs). |
| H1 ≤8 words, outcome-led | ½. 9 words, a curiosity question. |
| 5th–7th grade copy | ✅ |
| One decision, no other links | ✅ in the quiz state. ❌ footer has 3 dead `#` links. |
| H1 + sub + CTA + risk line in 390x844 | ½. Quiz options are visible, but there's no risk line ("free, no sign-up"). |
| Form ≤3 fields, right types | ½. 2 fields, `type=email`. Placeholder-only labels, no `autocomplete`. |
| One true trust element next to the CTA | ❌ none in the hero, and the guarantee isn't next to the checkout button. |
| Self-contained, no 3rd-party bloat | ✅ |

### 2d. Copy Thief: awareness and message match: 6.5/10
- **Awareness of the arriving traffic:** unaware → problem-aware ("I didn't know this existed"), primed by *one specific news story*. They need a short bridge from "that happened to her" to "could it be me?" to "how do I check properly?" to "$9". The quiz is the right bridge.
- **Sophistication:** stage 3. "Search MissingMoney.com, it's free" is common advice in news coverage, so a promise alone doesn't sell a paid product. The **mechanism** has to: "most people search wrong (one site, one name, one state, and the site hides the real amount)". The page has this mechanism, but it's 5 lines long and appears after the stories.
- **Message-match breaks:** (1) The story the visitor just watched isn't echoed at the top. (2) The Ohio heirs video (FOX 8 Cleveland) has **no matching story on the page**. (3) The Colorado video's best insight ("the site said *over $250*, it was nearly $30,000") is reduced to one line in the stories.
- **Ladder order:** H1 → quiz → email → result → why money is lost → stats → stories → mechanism → offer → guarantee → FAQ → CTA. The order is right for cold traffic. The *distance* between result and offer is the problem.

---

## 3. Top 10 fixes, ranked by expected impact

### Fix 1: Put the offer directly under the result (first CTA within one screen of the result)
**Why:** The quiz builds momentum and the page spends it on 4 screens of reading. The first CTA is at y=3,564. A quiz funnel converts on the *result* moment (RyMac: above-fold CTA, up to +304%; Doctor #12).

**Change:**
- On result, hide `<header>` (`header.classList.add('hidden')`) so the result card is at the top of the screen.
- Immediately after the result card, insert a short offer card (the existing one stays lower down as the full version, with the same CTA):

```html
<div class="card" id="next">
  <div class="kicker">Your next step</div>
  <p class="q" style="margin-top:4px">Search every place on your list in about 30 minutes</p>
  <p>The Lost Money Playbook gives you the exact order to search all the official sites (state and federal), the name tricks that surface hidden records, and the letters to send. Searching and claiming stay free. You only pay for the map.</p>
  <a class="btn" href="CHECKOUT_URL" data-ic>GET MY PLAYBOOK FOR $9 →</a>
  <p style="text-align:center;font-size:14px;color:var(--muted);margin:10px 0 0">Instant PDF · 60-day money-back guarantee · Official claims are always free</p>
</div>
```
- Keep the education sections below and end them with the same button.

### Fix 2: Make the result personal: turn each "yes" into a place to search (and fix the score-0 bug)
**Why:** This is the weakest lever (Perceived Likelihood). Right now everyone gets one of two generic messages. **Bug:** someone who scores 0/6 is told "You have some common risk factors", which is false. Mapping their own answers to specific Playbook chapters shows them the product is built for their situation, with no fabricated proof.

**Change:** store the answers (`ans[i]=k`). In `showResult()`, render a list under the score titled **"Where your answers say to look:"** using these lines (all taken from guide content):

| Answer | Line shown |
|---|---|
| Q1 2+ states | **More than one state.** Each state keeps its own list. Search every state you've lived, worked or banked in, not just today's. *(Playbook, Ch. 2, step 3)* |
| Q2 moved | **You moved.** Final checks and refunds often went to an old address. Search the states you moved *from*. *(Ch. 2)* |
| Q3 changed jobs | **Job changes.** Final paychecks, old retirement plans and group life insurance can go unclaimed. Check state lists, the PBGC pension search, and send Letter Template 1 to old employers. *(Ch. 2, 3 + Templates)* |
| Q4 loss in family | **A family member passed away.** Search their name too, plus the free NAIC Life Insurance Policy Locator. Heirs can claim. *(Ch. 4)* |
| Q5 other last name | **Another last name.** Records are filed under the name the company had. Search maiden, married and misspelled versions. *(Ch. 2, step 2)* |
| Q6 closed/forgotten account | **A closed or forgotten account.** Inactive balances are sent to the state after a few years. *(Ch. 1)* |

Score 0 message (replace the current fallback, which shouldn't claim risk factors):
> **You have few of the most common risk factors.** That's good news. A quick free search of your current state at unclaimed.org is still worth 5 minutes. Settlement and refund programs (Playbook, Ch. 5) don't depend on moving or changing jobs.

Score 1–2 message:
> **You have [N] common risk factor[s].** Even one move or one job change can leave a check behind. Here's where your answers say to look:

Score 3+ message: keep the current copy and add "Here's where your answers say to look:".

Also send `fields[quiz_answers]` with the lead so email 1 can repeat the same list.

### Fix 3: Match the ad's story at the top (one page, three openings)
**Why:** This is copy-thief's #1 cold-traffic leak (scent break). Someone who just watched "She thought it was a scam. It was $108,000" lands on a generic question. Matching the eyebrow and top bar to each ad angle is cheap and usually one of the highest-impact tests.

**Change:** read `?s=` from the URL and swap the top bar and the kicker only (the H1 and quiz stay the same). Tag each ad's URL accordingly.

| `?s=` | Top bar | Kicker |
|---|---|---|
| `fl` (Ad D / video 01) | An 88-year-old Florida woman thought the letters were a scam. It was about $108,000. (FOX 13 Tampa) | She checked. Could you have money waiting too? |
| `co` (video 02) | The state site said "over $250." It was nearly $30,000. (Fox News) | Most people see "over $100" and never claim it |
| `oh` (video 03 / Ad B) | A family's late parents' safe deposit box went to the state. Then a box of savings bonds came back. (FOX 8 Cleveland) | Lost a parent, grandparent or spouse? Heirs can claim. |
| default | U.S. states hold about $70 billion in unclaimed money. Some of it may be yours. | 60-second check |

**Also add the missing Ohio story** to `#stories` (real, from `research/stories-unclaimed-money.md` and the guide):
> **An Ohio family: hundreds of savings bonds from their late parents**<br>Their parents' safe deposit box had been turned over to the state. The claim stalled until a local news team asked questions. Then a box arrived with savings bonds, cash and collectibles.<br><small>FOX 8 Cleveland, 2025</small>

(Don't add a dollar amount: the source only says "tens of thousands", without a verified figure.)

### Fix 4: Show the product (cover + 3 inside pages from the real PDF)
**Why:** Doctor #10 scores 1/10. There is zero product visual for a product people can't touch. Seeing the tracker, a template and the federal-sources list lowers perceived effort and raises likelihood. It needs no new claims.

**Change:** export 4 images from `guide/The-Lost-Money-Playbook.pdf` (cover, Ch. 3 "Federal Money Most People Never Check", Template 1, Search Tracker). Show them as a stacked mockup at the top of the "Introducing" card with this caption:
> **12 pages · 7 short chapters · 3 ready-to-send letters · printable Search Tracker.** Read it tonight, search in about 30 minutes.

Rename the card's heading to use the PDF's own subtitle: **"The Lost Money Playbook: The 30-Minute Search Method"** (the M.A.G.I.C. naming fix).

### Fix 5: Answer "Why pay $9 if searching is free?" next to the price, not in a closed FAQ
**Why:** This is the #1 objection for this offer, and right now it hides in a collapsed `<details>`. Price justification belongs right before the price (copy-thief ref 05). Also, **"Launch price" implies a deadline that doesn't exist**. Remove it.

**Change:** replace the `Launch price` kicker with `One-time price`, and put this block right above the price:
> **Searching is free. Knowing where to search is the hard part.**
> One free site doesn't show every state, every name you've used, or federal money like old IRS refunds, savings bonds, pensions and back wages. The Playbook puts all of it in order, so one evening covers what most people never get to.
> Some "finder" companies offer to do this for a percentage of what they recover. With this guide you can almost always do it yourself, for free. *(from Playbook Ch. 7)*

Don't print a "$XX value" anchor or a "finders charge 30%" figure. Neither is sourced.

### Fix 6: One CTA wording, risk line under every button, named guarantee next to it, sticky mobile CTA
**Why:** The two buttons say different things. "SHOW ME WHERE TO LOOK" doesn't signal checkout (Doctor #12). The guarantee sits below the button instead of beside the decision. First-person CTA wording also tends to lift clicks.

**Change:**
- Every checkout button: **`GET MY PLAYBOOK FOR $9 →`**
- Under every checkout button: **`Instant PDF · 60-day money-back guarantee · Official claims are always free`**
- Name the guarantee and move the card to directly above the first checkout button:
> **The 60-Day "Worth It" Guarantee.** Use the Playbook for 60 days. If you don't feel it was worth far more than $9, email us and get every cent back. No questions asked. (Finding money isn't required; nobody can promise that.)
- After `#offer` is shown, add a fixed bottom bar on mobile (≤600px) with the same button. Hide it while either in-page checkout button is visible.
- Fire `fbq('track','InitiateCheckout')` on **all** checkout buttons (`[data-ic]`); right now only the first one fires it.

### Fix 7: Hero trust + commitment line (first screen)
**Why:** "Free", "no sign-up to start" and "not a government site" aren't on the first screen (Doctor #7 = 4, #8 = 1). People 35–70 who've been warned about unclaimed-money scams need the reassurance *before* tapping.

**Change:**
- Shorten the sub (4 lines → 2):
  > Old paychecks, forgotten accounts, a parent's life insurance. Answer 6 quick questions to see your risk factors.
- Directly under the quiz card, add:
  > ✓ Free · ✓ No sign-up to start · ✓ Independent guide, not a government site
- Below that, one real micro-proof line linked to the stories:
  > "She thought the letters were a scam. It was about $108,000 in unclaimed stock." (FOX 13 Tampa, Sept. 2025)
- H1 A/B alternates (same promise, sharper): **"Is the state holding money in your name?"** (8 words, ties to the mechanism) and, for `?s=fl`, **"She thought it was a scam. It was $108,000."** (verbatim ad headline).

### Fix 8: Move the mechanism up and make it concrete ("most people search wrong")
**Why:** This is a stage-3 market. The mechanism is what separates a $9 map from "just google it". Today it's 5 lines placed after the stories.

**Change:** move the "most people search wrong" section to right after the result/next-step card, and expand it into 4 scannable lines from the guide:
> **Why most people search once and find nothing**
> 1. **One state.** Money goes to the state of your *last known address*, which may not be where you live now.
> 2. **One name.** Records sit under maiden names, middle names and misspellings ("Jon/John", "Mc/Mac").
> 3. **Hidden amounts.** Many state sites only show "over $100" or "over $250". A Colorado listing that said "over $250" turned out to be nearly $30,000 (Fox News).
> 4. **Federal money isn't on state sites.** IRS refunds, savings bonds, pensions (PBGC), back wages (DOL), FHA refunds, failed-bank deposits (FDIC) and VA insurance each have their own search.

Then change the stories H2 from "Real people. Real money. Found by searching." to **"Real people. Real money. As reported by local news."** Not every story was found by the person searching (the Hammond man was surprised with a check, and a detective found Barbara's notice), so the current H2 overstates.

### Fix 9: Make the email step worth giving an email for
**Why:** "Skip, just show my result" sits right under the button. That's honest and should stay. But the reason to give an email is vague ("your result + checklist"), and fields are placeholder-only.

**Change:**
- Heading: **"Get your personal search list by email"**
- Sub: **"Your answers + the 3 free official sites to check first, so you can do it tonight."**
- Button: **`EMAIL ME MY SEARCH LIST →`**
- Add visible labels, `autocomplete="given-name"` / `autocomplete="email"` and `inputmode="email"`.
- Keep "Skip, just show my result" and the privacy line.
- Shorten the fake-processing loader from 2.9s to ~1s, and change its copy to **"Scoring your answers…"**. "Checking state-move patterns…" and "Comparing with the most common unclaimed property types" can read as if records were searched, which Meta reviewers and skeptical 60-year-olds will both distrust.

### Fix 10: Launch blockers and claim accuracy (do before any spend)
- Replace `#CHECKOUT_URL` (both buttons). Meta rejects non-functional landing pages.
- Footer: `Privacy Policy` → `privacy.html`, `Terms` → `terms.html`, `Contact` → a real `mailto:` support address. All 3 are dead `#` links now. Meta's landing-page review and Hotmart both expect working policy and contact links.
- Install the Pixel (placeholder comment still in `<head>`) and set `LEAD_ACTION`.
- **Stat accuracy:** "33 million Americans have unclaimed property (NAUPA)" doesn't appear in `research/stories-unclaimed-money.md`. The sourced NAUPA/unclaimed.org figure is **"about 1 in 7 Americans"**, which is also what the guide says. Change the stat tile to **"1 in 7 Americans have unclaimed property (NAUPA)"**, or verify 33M against a NAUPA source first. The same line is in video 02's end card.
- Label the Colorado story honestly: `Fox News (opinion column), June 2026`. In the source, the columnist searched for a cousin. "A Colorado man" is fine.

---

## 4. Anything that could hurt Meta ad approval (or the account)

**Landing page (`index.html`)**
1. **Non-functional CTA** (`#CHECKOUT_URL`) and **dead Privacy/Terms/Contact links**: likely rejection under the landing-page functionality policy. Fix 10.
2. **Unsourced stat** "33 million Americans": a misleading-claims risk. Use the sourced "1 in 7". Fix 10.
3. **"Launch price"** with no real price change: misleading pricing / false urgency. Fix 5.
4. **Score-0 user told they "have some common risk factors"**: a false personalized claim. Fix 2.
5. **Loader that looks like a records check**: could read as implying a search of their data. Fix 9.
6. **Stories H2 "Found by searching"** overstates 3 of 5 stories. Fix 8.
7. Already fine, keep it: independence disclaimer, "not part of Facebook", "results vary / many find nothing", no gov logos or seals. The colors and layout don't impersonate a .gov site.

**Ads (`ads/ads.md`, videos) touching the page**
8. **Text B opener "Did your mom, dad or grandparents pass away?"** asserts a personal circumstance about the viewer. Meta's personal-attributes rule is mostly about listed categories (health, finances, etc.), but direct "did your X die?" questions get flagged often. Safer: **"When a parent passes away, money they left can go unclaimed."** Same for video 03's end card "DID YOU LOSE A PARENT?" → **"HEIRS CAN CLAIM IT"**.
9. **"Moved in the last 10 years? Read this"** (extra headline) is low risk but follows the same pattern. Prefer **"Money often gets lost when people move."**
10. **AI-generated people shown while the narration tells a real person's story** (video 02 v2a–v2c, video 03 v3a–v3d): add a small on-screen label **"Illustration"**. That keeps the rule in `ads.md` (never present an AI photo as the person in the news), and Meta's AI-disclosure labeling applies to photorealistic generated people.
11. Video 02's "33 MILLION AMERICANS HAVE MONEY WAITING · Source: NAUPA": same sourcing issue as #2.

**Upsell (`upsell.html`), post-purchase. Meta rarely reviews it, but it affects refunds, chargebacks and Hotmart standing:**
12. **"⚠️ WAIT: your order is not complete. Do not close this page."** and `<title>Wait! Your order is not complete</title>` are false (the $9 order *is* complete) and the kind of pattern that drives chargebacks. Replace with: **"✓ Your Playbook is confirmed and on its way to your email. One optional add-on before you go:"**
13. **"Today only, on this page"**: a deadline claim. Keep "only on this page" (true if it's not sold elsewhere) and drop "Today only" unless it's enforced.
14. **"makes the search 3× faster"**: unsubstantiated. Use **"puts every state's official link and the 3-layer plan in one place, so you're not hunting for links."**
15. **"This is where 'nothing found' turns into 'found it'"** implies finding money. Use **"This is where people catch the states they forgot to search."**
16. The upsell's `<meta description>` was copied from the landing page. Minor; replace it.
17. On mobile, the upsell's price and button sit below the first screen. Add a one-line price + button under the subhead (same `YES, ADD THE SPEED KIT, $27 →`).

---

## 5. Suggested test order
1. Ship Fixes 10 + 1 + 2 + 6 together as the baseline (blockers + offer under the result + personal result + unified CTA). Don't spend on the current version.
2. A/B the `?s=` story openings (Fix 3) against the default, per ad set.
3. Then test the product mockup (Fix 4) and the price-justification block (Fix 5).
4. Watch: quiz start rate (first-option click / PageView), quiz completion, email opt-in %, result → InitiateCheckout %, InitiateCheckout → Purchase.
