---
name: site-brief
description: "Turn a request for a new site, landing page or page redesign into a filled brief and then a built page. Use when the user asks for a website, landing page, hero section or a recreation of a site the user has seen, or when he mentions the fill-in sheet, SITE-SPEC-TEMPLATE or a prompt-generator prompt. Carries the template path, the minimum fill, the asset fallbacks and the handoff to the hallmark design skill."
---

# site-brief

A request for "a site like this one" fails in one of two ways: too few facts, so the
result is a generic guess, or too many adjectives and no numbers, so the result looks
nothing like what was pictured. This skill closes that gap before any code is written.

---

## The artefact

**`~/Desktop/SiteSpec/SITE-SPEC-TEMPLATE.md`** — a 17-section fill-in sheet,
reusable for any subject. It exists because a soda-can landing-page prompt was reverse
engineered into fields: "flavour" became **variant**, "the can" became **centerpiece**,
"cherries and leaves" became **decor layers**, "bubbles" became **ambient particles**, and
the flavour-switch choreography became a **beat sheet** written like a shot list.

A worked example sits beside it: `kai-sol-brief.md`, filled from the live repo rather than
from guesses, with the eight judgment calls marked `[MY CALL]` so he can overrule them.

## How to run it

1. **Copy, do not edit the template.** `cp SITE-SPEC-TEMPLATE.md <project>-brief.md`.
   The blank stays reusable.
2. **Fill what can be read, ask only for what cannot.** If the site already exists, read
   the repo and fill the brief from it: tokens, fonts, copy, prices, interactions. Never
   ask for a value that is sitting in a CSS file.
3. **Two dials decide everything else**, and they are the only fields worth blocking on:
   - **Page behaviour** — locked single viewport / normal scroll / scroll-snap / horizontal
   - **Detail dial** — exact replica (follow every number literally) / tight spec (the user gives
     palette, copy, assets; you choose motion in a coherent style) / vibes (you compose)
4. **State the audience in one line** before handing anything over, so he can correct it.
5. **Mark every invented value.** Anything not from the user or the repo gets flagged, and
   collected in a short "open decisions" list at the end. He decides taste questions.

## Minimum fill

If the user has no time, these ten answers are enough to build a complete page:

```
1. Subject           6. Background: dark or light + base hue
2. Page name/title   7. Main headline, exact wording
3. One-sentence pitch 8. One CTA label
4. Mood, 3 adjectives 9. Scroll, or locked single screen
5. Accent colour hex 10. Centerpiece: what it is, URL if any
```

## Fidelity: weak versus strong

Push for the right column. It is the whole difference between a guess and a replica.

| Field | Weak | Strong |
| --- | --- | --- |
| Accent | "pink" | `#fbcfe8`, text on it `#011d17` |
| Background | "dark green" | radial, `#0b8a78` 0%, `#044e3b` 50%, `#011411` 100% |
| Hover | "make it move" | `translateY(-30px) rotate(-12deg) scale(1.15)` over `0.5s cubic-bezier(0.34,1.56,0.64,1)` |
| Transition | "cool spin" | 0→360deg with blur 0→15px over `0.6s power2.in`, swap texture at the peak, 360→720deg blur→0 over `1.5s back.out(0.7)` |

## Assets: never pretend

Binary assets cannot be invented. If the user has no 3D models, photos or textures, pick a
substitute strategy **and say which one you picked**:

- build the centerpiece in pure CSS/SVG (works well for cans, bottles, phones, cards)
- three.js primitives with materials instead of a real model
- free CDN sources, accepting they may change (Unsplash, Poly Haven, Khronos sample GLBs)
- visible placeholder boxes labelled with what goes there
- build against token names now, assets arrive later

**Never ship invented stock photos as if they were final.** And never hand-build fake
browser chrome, phone frames or IDE windows around a mockup: that is one of the strongest
"looks AI-generated" tells. Use a real screenshot in a `<figure>`, or let the content
stand alone.

## Handoff to design

Once the brief is filled, **load the `hallmark` skill** and follow its flow rather than
improvising visuals: pick a macrostructure, nav and footer archetype before writing code,
state the picks in plain text, then run its 58-gate slop test on the output and fix what
fails. On a repeat build, its diversification rule matters: do not ship the same
macrostructure or the same nav/footer shape twice in a row.

Hard rules that survive every brief:

- **Headings roman**, never an italicised emphasis word
- **Zero eyebrow labels** (`01 · FEATURES`) above section headings, and never an eyebrow
  in a column beside the heading
- **Animate `transform` and `opacity` only**; three motion primitives per site, maximum
- Every interactive element ships hover, `:focus-visible`, `:active` and disabled states
- `overflow-x: clip` on `html` and `body`; verified at 320 / 375 / 414 / 768px
- `prefers-reduced-motion` honoured
- Colours and fonts referenced by token name, never inlined mid-file

## Copy voice

State facts and stop. **No dares, no hype, no superlatives.** "Interactive, has sound, two
minutes" beats "click if you dare and turn the sound up". Confidence is stating the fact;
hype is asking to be believed. For Croatian sites: formal `vi`, short sentences, name the
customer's problem before the service, show prices rather than hiding them behind
"contact us".

## Delivery

1. Build as a **new candidate file** (`index-v4.html`), never overwriting a live page,
   unless the user has asked for the replacement outright.
2. Serve it locally over HTTP, not `file://`, and open it.
3. **Publish it as an Artifact** with its CSS/JS as supporting files, so it can be
   reviewed on a phone, and give the link.
4. Report what you invented, what you removed and why, and what is still open.
5. Promote to the live page only on request, and then follow the **`ship-site`**
   skill for the backup ritual and verification.
