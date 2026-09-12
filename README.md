# Best Brokers Australia (AU Broker Directory)

A national directory platform indexing 16,900+ Australian mortgage, finance, insurance, real estate, business-sales, asset-finance, customs/freight, and wealth advisers.

**Live site:** https://bestbrokersaustralia.org (Cloudflare Pages project `best-brokers-australia`).

---

## 🏛️ Architecture & Module Structure

The project has been rebuilt into a modular, component-based static generator architecture:

```
src/
├── config.py              # Central site configuration, URLs, paths, thresholds
├── taxonomy.py            # Category, state, city taxonomies & URL builders
├── quality.py             # Trust Score (0-100%) & SEO Quality Score (0-100) algorithms
├── models.py              # Broker & Hub data models, relationship graph
├── components/            # Reusable UI components (Single Source of Truth)
│   ├── base.py            # Document shell, metadata, schema injection, scripts
│   ├── header.py          # Master header & navigation
│   ├── footer.py          # Master footer with taxonomy & governance links
│   ├── breadcrumbs.py     # Hierarchical breadcrumb navigation & BreadcrumbList JSON-LD
│   ├── broker_card.py     # Broker comparison card for lists, hubs, comparisons
│   ├── trust_badge.py     # Trust score pill, tiers, and transparent 3-factor breakdown
│   ├── pagination.py      # Crawlable HTML pagination
│   ├── forms.py           # Review, Case Study, Claim, and Correction submission forms
│   └── styles.py          # Unified design system tokens & CSS stylesheet
├── templates/             # Page templates
│   ├── home.py            # Homepage with instant live search & sector grid
│   ├── category.py        # National category hubs (e.g. /mortgage-brokers/)
│   ├── state.py           # State category hubs (e.g. /mortgage-brokers/nsw/)
│   ├── city.py            # Local city hubs (e.g. /mortgage-brokers/sydney/)
│   ├── broker.py          # Individual broker profile (/broker/:slug/)
│   ├── static.py          # Trust & governance pages (/about/, /methodology/, etc.)
│   └── not_found.py       # Custom 404 page
├── seo/                   # Technical SEO generators
│   ├── schema.py          # JSON-LD schemas (Organization, CollectionPage, LocalBusiness)
│   ├── sitemaps.py        # Segmented XML sitemaps index
│   ├── robots.py          # robots.txt generator
│   └── redirects.py       # Cloudflare Pages _redirects and _headers
├── builder.py             # Static site generator orchestration & incremental build
└── cli.py                 # CLI interface
```

---

## 🚀 Fast Incremental & Targeted Builds

No need to rebuild all 16,900+ pages for routine template or single-record updates:

```bash
# 1. Fast Hubs & Core Rebuild (< 2 seconds)
# Rebuilds homepage, 7 category hubs, 56 state hubs, 4,014 city hubs, trust pages & sitemaps
python3 build.py --hubs-only

# 2. Single Broker Instant Rebuild (< 50 milliseconds)
# Updates just one broker profile without touching any other files
python3 build.py --slug dominion-finance-canberra-mortgage-finance-287

# 3. Full Site Regeneration & Cloudflare Pages Sync (~40 seconds)
python3 build.py --all
```

---

## 🌐 SEO Information Architecture

- **Homepage:** `/` (National discovery, instant search, sector grid)
- **Category Hubs:** `/{category}/` (e.g. `/mortgage-brokers/`, `/insurance-brokers/`)
- **State Hubs:** `/{category}/{state}/` (e.g. `/mortgage-brokers/nsw/`, `/mortgage-brokers/vic/`)
- **City Hubs:** `/{category}/{city}/` (e.g. `/mortgage-brokers/sydney/`, `/mortgage-brokers/parramatta/`)
- **Broker Entity Profiles:** `/broker/{canonical-slug}/`
- **Trust & Governance Hubs:**
  - `/about/` — AIEX engineering background & directory mission
  - `/methodology/` — 3-Factor Trust Score formula & scoring engine
  - `/editorial-policy/` — Quality standards & zero pay-to-rank guarantee
  - `/review-policy/` — Review moderation & dispute policy
  - `/claim-profile/` — Broker verification & claim workflow
  - `/contact/` — Direct support & 24-48h correction SLA
  - `/privacy/` — Australian Privacy Principles (APP) compliance

---

## 🔒 Indexation Quality Gate

Profiles are scored on a 0–100 Quality Score (verified identity, NAP completeness, description, ratings, licence disclosure, original proof).
- **Indexable (`index, follow`):** Included in segmented sitemaps and search engine indexes.
- **Thin / Incomplete (`noindex, follow`):** Searchable internally by users, but excluded from sitemaps and search engines to protect site authority.

---

## 💻 Local Development Server

```bash
python3 server.py
```
Serves `site/` at `http://localhost:8941` with extensionless routing support and active endpoints for `POST /api/reviews` and `POST /api/cases`.

---

## 🚢 Deploying to Cloudflare Pages

```bash
git add -A
git commit -m "..."
git push origin main
npx wrangler pages deploy docs --project-name=best-brokers-australia --commit-dirty=true
```
