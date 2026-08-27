# AU Broker Directory

A directory of Australian mortgage & finance brokers — search by name, suburb
or phone, see a computed Trust Score, and (with a running backend) submit
reviews or real client cases.

**Live demo (static, browsing/search only):** see the GitHub Pages link in
the repo's "About" sidebar.

## What's here

- `build.py` — static site generator. Reads `data/sample10.json`, writes the
  whole `site/` folder (homepage, one page per broker, search index,
  sitemap). No framework, no build step beyond `python3 build.py`.
- `server.py` — local dev server (Python stdlib only). Serves `site/` and
  adds two endpoints so the review/case forms actually work:
  `POST /api/reviews`, `POST /api/cases`. Submissions are appended to
  `data/submissions/*.jsonl` (git-ignored — not published).
- `docs/` — a static copy of `site/`, published via GitHub Pages. Since
  Pages only serves static files, the submission forms on the live demo
  will show a "could not reach the server" message — that's expected until
  the backend is deployed somewhere that runs Python (Render, Fly.io, Cloud
  Run, etc.), not just GitHub Pages.

## Running locally (with working forms)

```bash
python3 server.py
```

Then open `http://localhost:8941`.

## Regenerating the site after a data change

```bash
python3 build.py
cp -r site/* docs/
```

## Status

MVP with 10 sample brokers (one per major AU city), pulled from a larger
~11,600-row source spreadsheet spanning 7 broker categories. Scaling to the
full dataset is mechanical (same script, bigger input) — see the project's
build record in NickUltimateVault for the full history and next steps.
