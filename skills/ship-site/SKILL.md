---
name: ship-site
description: "Build, verify and deploy the live sites (kai-sol.com on GitHub Pages, shaiyex.com on Cloudflare Pages). Use when asked to push, deploy, ship, publish or roll back either site, or when editing files in ~/web or ~/shaiyex. Carries the backup ritual, the verification checklist, the deploy targets and the rollback commands."
---

# ship-site

Two live sites, two different hosts, one discipline. Both are hand-written static
HTML/CSS/JS with **no framework, no build step and no runtime dependency** except Google
Fonts. That constraint is not negotiable: it is why they load fast, and the speed is part
of what kai-sol sells.

---

## The two targets

### kai-sol.com — the business site

| | |
| --- | --- |
| Local | `~/web` |
| Repo | `Shywera/web` |
| Host | **GitHub Pages**, via `.github/workflows/deploy.yml` |
| Trigger | push to `main` (or `workflow_dispatch`) |
| Uploads | the **whole repo root** (`path: '.'`) |
| Domain | `CNAME` file holds `kai-sol.com` |
| Observed deploy time | under 15 seconds |
| Design system | **`design.md` at the repo root is the source of truth.** Read it before touching any page. |
| CSS / JS | `assets/css/tokens.css` + `assets/css/kai.css`, `assets/js/kai.js` |
| Legacy, kept only for rollback | `base.css`, `home.css`, `usluge.css`, `iskustvo.css`, `kontakt.css`, `o-nama.css`, `assets/js/script.js` |
| Pages | `index`, `usluge`, `iskustvo`, `o-nama`, `kontakt`, `404`, `zasto-nas` |

**Because the workflow uploads the repo root, anything committed is public.** Keep
experiments and candidate pages **untracked** rather than committing them; that is how
four redesign candidates stayed local while the real pages shipped.

### shaiyex.com — the WoW personal site

| | |
| --- | --- |
| Local | `~/shaiyex` |
| Repo | `Shywera/Shaiyex` |
| Host | **Cloudflare Pages**, build command empty, output directory `public` |
| Root domain | one proxied CNAME to `shaiyex.pages.dev`; `www` has no record |
| `wrangler.toml` | a static-assets-only Worker config (`[assets] directory = "./public"`), left from an earlier Workers attempt |
| Routes | `/`, `about`, `anathema`, `beat`, `deplete`, `drift`, `kick`, `loud`, `miss`, `overdrive`, `pitch`, `raid`, `the-quiet-part`, `why` |
| Not static any more | `functions/api/scores.js` and `functions/api/vault.js` are **Cloudflare Pages Functions** |
| Binding required | both functions need one store bound to the Pages project as **`SCORES`** (Workers KV is the right choice). Without it they return 503 and the pages fall back to local scores / "the book is shut". |
| Toolchain | `tools/*.py` builds the `/beat/` rhythm-game charts (`osu2chart.py`, `build_beat.py`, `add_maps.py`, `verify.py` and friends). Charts live in `tools/charts/`. |

`/beat/` is a rhythm game with 10 "dungeons" and 3 difficulties, a KV leaderboard
(`/api/scores`) and a guestbook (`/api/vault`).

---

## Hard rules

1. **Never put WoW, gaming or personal content on kai-sol.com.** It was deliberately removed so the
   business domain stays clean. That content lives on the personal site.
2. **No blue anywhere on kai-sol.** The palette is a deliberate reaction against it: warm
   near-black paper, cream ink, one flare-orange accent. No blue in gradients, links,
   states, hover or charts.
3. **Headings are roman on kai-sol**, never italic. Emphasis is the accent colour plus a
   2px drawn underline (`.mark`). Zero eyebrow labels above sections. Both rules come from
   the `hallmark` skill's anti-pattern list and are recorded in `design.md`.
4. **No invented numbers.** Only three kinds of figure may appear: supplied by the client,
   measured live in the visitor's browser, or a promise the firm already publishes
   (the 24-hour response time). Otherwise the row hides itself.
5. **Do not commit or push unless asked.** When asked, follow the backup ritual first.
6. **Never delete the user's files to tidy up.** Leave superseded candidates on disk, untracked.

---

## Before any push: the backup ritual

Do all four. They cost seconds and they are the reason a bad deploy is boring.

```bash
cd ~/web
git status --short            # confirm a clean, understood tree
git tag -a backup-live-<YYYY-MM-DD> -m "Backup of live site before <change>"
git branch backup/<YYYY-MM-DD>-live
git archive --format=zip -o "$HOME/Desktop/SiteSpec/backup/<site>-live-<date>-<sha>.zip" HEAD
```

Then unzip that archive into a sibling folder so the old site can be opened in a browser
without git, and write or refresh a `RESTORE.md` beside it with the rollback commands
below. Tags and branches stay **local** unless asked; GitHub
already holds the same commit as `origin/main`.

## Verify before you ship

Run all of these; each one has caught a real bug.

```bash
# every link and anchor resolves (files exist, #ids exist in the target file)
# tag balance per page
for tag in div section span p a; do
  o=$(grep -o "<$tag[ >]" page.html | wc -l); c=$(grep -o "</$tag>" page.html | wc -l)
  [ "$o" != "$c" ] && echo "MISMATCH $tag $o/$c"
done
file page.html                       # must say UTF-8
grep -c "ž\|š\|č\|ć\|đ" page.html    # diacritics survived the edit
grep -l "base.css\|home.css" *.html  # no legacy stylesheet left behind
```

Then, after the deploy, curl the live domain rather than trusting the dashboard:

```bash
for u in "" usluge.html iskustvo.html o-nama.html kontakt.html 404.html assets/css/kai.css; do
  printf "  %-24s HTTP %s\n" "/$u" "$(curl -s -o /dev/null -w '%{http_code}' https://kai-sol.com/$u)"
done
```

Also confirm the things that must **not** be live (untracked candidates should return 404),
and say to hard-refresh, since GitHub Pages and the browser both cache.

## Rollback

Safest on a live site, because it keeps history honest and triggers a normal deploy:

```bash
cd ~/web
git revert --no-commit backup-live-<date>..HEAD
git commit -m "Vrati stranicu na stanje od <date>"
git push
```

Single file: `git checkout backup-live-<date> -- index.html`
Discard local commits: `git reset --hard backup-live-<date>` (destructive, only on request).

---

## Environment gotchas, learned the hard way

- **Quoted heredocs (`<< 'EOF'`) fail unpredictably in this Bash tool.** For anything
  longer than a couple of lines, write the file with the Write tool, or write a small
  Python generator script with Write and then run it. Do not fight the heredoc.
- **PowerShell `Get-Content -Raw` decodes as ANSI and mangles Croatian diacritics and
  dashes.** Read and write UTF-8 explicitly, or do the edit in Python / `perl -i` from
  Bash instead.
- `perl -i -pe 's/.../.../g'` is the reliable way to do a multi-file text rename; verify
  afterwards with `grep -ril` that nothing was missed and that diacritics survived.
- Python 3.14 is on PATH as `python`. There is **no `gh` CLI** on this machine, so GitHub
  cannot be queried from here; ask, or read the repo itself.
- Windows line endings: git will warn `LF will be replaced by CRLF`. Harmless. Check
  `git diff --stat` shows only the lines you meant to change, not the whole file.

## Local preview

```bash
cd ~/web && python -m http.server 8080 --bind 127.0.0.1
```

Serve over HTTP rather than opening `file://`: the Performance API will not report
transfer sizes from `file://`, so the measured-metrics block on the homepage hides two of
its four rows and looks broken when it is not.

For review on a phone, publish the pages as an Artifact (page plus its CSS/JS as
supporting files) and hand him the link, rather than pushing an unfinished design to the
live domain.
