# Best Brokers Australia (AU Broker Directory)

A directory of Australian mortgage, finance, insurance, real estate,
business-sales, asset-finance, customs/freight and wealth/investment
brokers — search by name, suburb or phone, see a computed Trust Score and
real Google reviews, and (with a running backend) submit reviews or real
client cases.

**Live site:** https://bestbrokersaustralia.org (Cloudflare Pages).

## What's here

- `build.py` — static site generator. Reads `data/all_brokers_full.json`
  and `data/reviews_by_place.json`, writes the whole `site/` folder
  (homepage, About/Contact/Privacy, one page per broker, search index,
  sitemap). No framework, no build step beyond `python3 build.py`.
- `data/all_brokers_full.json` — the current dataset, ~16,917 unique
  businesses. Built by `data/ingest_new_package.py` from a Google
  Places-sourced Excel export (deduped by Place ID) plus ~210 businesses
  that only ever existed in an older one-off AIEX outreach-list merge
  (kept so they don't get silently dropped again — see that script's
  docstring for the full history).
- `data/reviews_by_place.json` — real Google review text (rating,
  reviewer, relative time), grouped by Place ID, capped at 12/business.
  Rendered on broker pages under "Reputation". Businesses with real
  reviews are ranked above those without in search results.
- `data/ingest_new_package.py` — re-run this whenever a new broker
  package spreadsheet arrives. Reads the source xlsx path hardcoded near
  the top of the file (update it to point at the new file first).
- `server.py` — local dev server (Python stdlib only). Serves `site/` and
  adds two endpoints so the review/case forms work end to end:
  `POST /api/reviews`, `POST /api/cases`. Submissions are appended to
  `data/submissions/*.jsonl` (git-ignored). Sends `Cache-Control: no-store`
  on every response so local testing never shows a stale cached page.
- `docs/` — a byte-for-byte copy of `site/`, deployed to Cloudflare Pages.
  Always `rm -rf docs && cp -r site docs` after a rebuild, never edit
  `docs/` directly.
- `assets_src/` — untracked-by-purpose source images (old portrait
  crops, raw exports) kept for reference; not read by the build.

## Running locally (with working forms)

```bash
python3 server.py
```

Then open `http://localhost:8941`.

## Regenerating the site after a data or template change

```bash
python3 build.py
rm -rf docs && cp -r site docs
```

`build.py` wipes `site/broker/` before regenerating, so a broker that
dropped out of the dataset (or whose slug changed) won't leave a stale
orphaned page behind.

## Deploying

```bash
git add -A
git commit -m "..."
git push origin main   # github.com/Niknesen/au-broker-directory
npx wrangler pages deploy docs --project-name=best-brokers-australia --commit-dirty=true
```

**Important:** any change to the shared header/footer/branding touches
every one of the ~16,900 generated broker pages, which means the deploy
step re-uploads nearly the whole site (10-15+ minutes, and Cloudflare
Pages occasionally drops the upload partway through with a generic
"Failed to upload files" error — just retry the same command, it resumes
from wherever it left off since already-uploaded files are skipped).
**Confirm with Nick before running a full-site deploy** — this has been a
recurring friction point; small/scoped changes are lower-stakes but a
heads-up is still appreciated.

## Known follow-ups / not yet done

- A `wrangler pages deploy` for the "Best Brokers Australia" rebrand
  (new logo, new name, Space Grotesk wordmark font — see commit
  `0ba330360`) was attempted and failed partway through the upload
  (transient Cloudflare error, only ~850 of 16,930 files uploaded). The
  code is committed and pushed to `main`; the live site has **not** been
  updated yet. Re-run the deploy command above when authorized.
- Review text only exists for ~4,820 of ~16,917 businesses (28.5%) — the
  rest simply weren't in the source Reviews sheet's coverage.
- Category assignment for the "expansion" businesses (no explicit
  Industry column value) is a keyword heuristic on Google Place types,
  not manually verified — see `bucket_from_google_types()` in
  `ingest_new_package.py`.
- ACY Securities and similar businesses outside the 7 broker categories
  (e.g. FX/CFD trading firms) are not covered by any current scrape and
  won't appear in search unless manually added the same way the old
  outreach batch was.
