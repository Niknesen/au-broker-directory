#!/usr/bin/env python3
"""
MVP build script for the broker directory.

Reads data/mortgage_finance_full.json (all 1,020 AU Mortgage & Finance
brokers from the master spreadsheet) and generates:
  site/index.html            - homepage with client-side search
  site/data.json             - search index consumed by index.html
  site/broker/<slug>.html    - one static page per broker (SEO)
  site/sitemap.xml           - sitemap for the generated pages

data/sample10.json is the original 10-broker demo fixture, kept for
reference. Scaling further (the other 6 categories, ~10,600 more rows) means
extracting them the same way and pointing SOURCE at the combined file - the
generation logic doesn't change. Purely mechanical string templating, no
LLM calls - generating all 1,020 pages takes well under a second.

Design system: light, blue, Apple-adjacent conservative style for a 30-40+
audience. No dark mode, no neon/glow - see build.py STYLE block for tokens.
"""
import json
import re
import html
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "data" / "mortgage_finance_full.json"
SITE = ROOT / "site"
SITE_URL = "https://brokers.example.com.au"  # placeholder domain

with open(SOURCE) as f:
    brokers = json.load(f)


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def first_email(email_field):
    if not email_field:
        return None
    return email_field.split(";")[0].strip()


def compute_trust_score(b):
    """Real, computed from data we hold: Google rating + review volume + licence
    disclosure. Never a fabricated finding - see the Trust score section for the
    full rationale. Shared between broker pages and the search index so ranking
    and the on-page score always agree."""
    rating_val = float(b["rating"]) if b.get("rating") else 0
    review_count = b.get("reviews") or 0
    score = (rating_val / 5) * 65
    score += min(review_count, 200) / 200 * 20
    score += 15 if b.get("license_disclosed") else 8
    return min(round(score), 97)


for b in brokers:
    # Record ID suffix guarantees uniqueness even when name+city collide
    # (e.g. two branches of the same franchise in one city).
    b["slug"] = f"{slugify(b['name'])}-{slugify(b['city'])}-{b['id']}"
    b["email_display"] = first_email(b["email"])
    b["initial"] = (b["name"][0] or "?").upper()
    b["trust_score"] = compute_trust_score(b)

# Full breadth of the master spreadsheet, shown as a "browse by category" row
# even though only Mortgage & Finance has generated pages so far.
CATEGORIES = [
    {"name": "Mortgage & Finance", "count": 1020, "active": True},
    {"name": "Insurance", "count": 811, "active": False},
    {"name": "Real Estate & Buyers", "count": 2300, "active": False},
    {"name": "Business Sales & Franchise", "count": 422, "active": False},
    {"name": "Asset & Equipment Finance", "count": 1193, "active": False},
    {"name": "Customs & Freight", "count": 2103, "active": False},
    {"name": "Wealth & Investment", "count": 3754, "active": False},
]

# ---------------------------------------------------------------------------
# Shared design system: light backgrounds, blue accent, restrained motion.
# ---------------------------------------------------------------------------
STYLE = """
:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --surface-alt: #f1f5f9;
  --border: #e2e8f0;
  --text: #0f172a;
  --text-muted: #475569;
  --accent: #0369a1;
  --accent-hover: #075985;
  --accent-soft: #e0f2fe;
  --radius-sm: 10px;
  --radius: 16px;
  --shadow-sm: 0 1px 2px rgba(15,23,42,.04), 0 1px 3px rgba(15,23,42,.06);
  --shadow-md: 0 4px 10px rgba(15,23,42,.06), 0 8px 24px rgba(15,23,42,.08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6; -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent-hover); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
img { max-width: 100%; display: block; }

header.site {
  position: sticky; top: 0; z-index: 30;
  background: rgba(248,250,252,.82); backdrop-filter: saturate(180%) blur(14px);
  -webkit-backdrop-filter: saturate(180%) blur(14px);
  border-bottom: 1px solid var(--border);
  padding: 16px 24px;
}
header.site .bar {
  max-width: 1040px; margin: 0 auto; display: flex; align-items: center;
  justify-content: space-between; gap: 16px;
}
.brand { display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 16px; color: var(--text); }
.brand .mark {
  width: 30px; height: 30px; border-radius: 8px; flex-shrink: 0; display: block;
}
.brand:hover { color: var(--text); }

main { max-width: 1040px; margin: 0 auto; padding: 0 24px 80px; }

/* Hero */
.hero { text-align: center; padding: 72px 0 40px; }
.hero h1 {
  font-size: clamp(30px, 4.5vw, 44px); font-weight: 700; letter-spacing: -0.02em;
  margin: 0 0 12px; color: var(--text);
}
.hero p.lede { color: var(--text-muted); font-size: 18px; max-width: 520px; margin: 0 auto 32px; }

.search-wrap { max-width: 560px; margin: 0 auto; position: relative; }
.search-wrap svg {
  position: absolute; left: 18px; top: 50%; transform: translateY(-50%);
  width: 20px; height: 20px; color: var(--text-muted); pointer-events: none;
}
#q {
  width: 100%; padding: 16px 18px 16px 48px; font-size: 16px; border-radius: 999px;
  border: 1px solid var(--border); background: var(--surface); color: var(--text);
  outline: none; box-shadow: var(--shadow-sm); transition: box-shadow 200ms ease, border-color 200ms ease;
}
#q:focus { border-color: var(--accent); box-shadow: 0 0 0 4px var(--accent-soft); }
#q::placeholder { color: #94a3b8; }

.policy-ribbon {
  display: inline-flex; align-items: center; gap: 8px; margin: 24px 0 0; padding: 8px 16px;
  border-radius: 999px; background: var(--surface-alt); border: 1px solid var(--border);
  color: var(--text-muted); font-size: 13px; font-weight: 500;
}
.policy-ribbon svg { color: var(--accent); flex-shrink: 0; }

/* Category chips */
.categories { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 32px 0 8px; }
.chip {
  display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px;
  border-radius: 999px; border: 1px solid var(--border); background: var(--surface);
  font-size: 14px; font-weight: 500; color: var(--text-muted);
  transition: border-color 200ms ease, color 200ms ease, background 200ms ease;
  min-height: 40px;
}
.chip .count { color: #94a3b8; font-weight: 400; }
.chip.active { background: var(--accent-soft); border-color: #bae6fd; color: var(--accent-hover); cursor: pointer; }
.chip.active:hover { border-color: var(--accent); }
.chip.disabled { opacity: .55; cursor: default; }

/* Results */
.results-head { display: flex; align-items: baseline; justify-content: space-between; margin: 40px 0 16px; flex-wrap: wrap; gap: 8px;}
.hint { color: var(--text-muted); font-size: 14px; }
.results-list { display: grid; gap: 12px; }

.result {
  display: flex; align-items: center; gap: 16px;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 18px 20px; box-shadow: var(--shadow-sm); color: var(--text);
  transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
  cursor: pointer;
}
.result:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); border-color: #bfdbfe; }
.result:hover .name { color: var(--accent-hover); }
.avatar {
  width: 44px; height: 44px; border-radius: 12px; background: var(--accent-soft);
  color: var(--accent-hover); display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 16px; flex-shrink: 0;
}
.result .body { min-width: 0; flex: 1; }
.name-row { display: flex; align-items: center; gap: 9px; }
.result .name { font-weight: 600; font-size: 16px; transition: color 200ms ease; }
.score-pill { font-size: 11.5px; font-weight: 700; padding: 2px 9px; border-radius: 999px; flex-shrink: 0; }
.result .meta { color: var(--text-muted); font-size: 13.5px; margin-top: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.phone-flag { display: inline-flex; align-items: center; gap: 4px; color: var(--text-muted); }
.phone-flag svg { width: 12px; height: 12px; flex-shrink: 0; }
.result .chev { color: #cbd5e1; flex-shrink: 0; width: 18px; height: 18px; }

.empty { text-align: center; color: var(--text-muted); padding: 56px 0; }

footer.site { text-align: center; padding: 40px 24px; color: #94a3b8; font-size: 13px; border-top: 1px solid var(--border); margin-top: 40px; }

/* Broker page */
.back-link { display: inline-flex; align-items: center; gap: 6px; font-size: 14px; color: var(--text-muted); margin: 28px 0 20px; }
.back-link:hover { color: var(--accent); }
.profile-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 20px;
  padding: 32px; box-shadow: var(--shadow-sm);
}
.profile-head { display: flex; align-items: center; gap: 18px; margin-bottom: 20px; }
.profile-head .avatar { width: 60px; height: 60px; border-radius: 16px; font-size: 22px; }
.profile-head h1 { font-size: 26px; margin: 0 0 6px; letter-spacing: -0.01em; }
.profile-head .addr { color: var(--text-muted); font-size: 14.5px; margin: 0; }
.badge {
  display: inline-block; font-size: 12.5px; font-weight: 600; padding: 4px 12px;
  border-radius: 999px; background: var(--accent-soft); color: var(--accent-hover);
  margin-bottom: 10px;
}
.fact-grid { display: grid; gap: 4px 32px; grid-template-columns: 1fr 1fr; margin: 24px 0 8px; padding-top: 24px; border-top: 1px solid var(--border); }
.fact-grid dt { font-size: 11.5px; text-transform: uppercase; letter-spacing: .06em; color: #94a3b8; margin: 14px 0 3px; }
.fact-grid dd { margin: 0; font-size: 15px; }
.reveal-btn {
  display: inline-flex; align-items: center; gap: 7px; padding: 7px 13px;
  border-radius: 8px; border: 1px solid var(--border); background: var(--surface);
  color: var(--accent); font-size: 13.5px; font-weight: 600; cursor: pointer;
  transition: border-color 150ms ease, background 150ms ease; font-family: inherit;
}
.reveal-btn:hover { border-color: var(--accent); background: var(--accent-soft); }
.reveal-btn.hidden { display: none; }
.reveal-value { display: none; }
.reveal-value.shown { display: inline; }
.reveal-text {
  color: var(--text); cursor: text; user-select: all; padding: 3px 8px;
  background: var(--surface-alt); border-radius: 6px; font-size: 13.5px;
}

/* Trust score */
.trust-policy {
  display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-muted);
  background: var(--surface-alt); border: 1px solid var(--border); border-radius: var(--radius-sm);
  padding: 10px 14px; margin: 0 0 18px;
}
.trust-policy svg { color: var(--accent); flex-shrink: 0; }
.trust-score-row { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; }
.score-ring {
  width: 96px; height: 96px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.score-ring-inner {
  width: 76px; height: 76px; border-radius: 50%; background: var(--surface);
  display: flex; align-items: center; justify-content: center;
}
.score-num { font-size: 21px; font-weight: 700; color: var(--text); letter-spacing: -0.01em; }
.trust-score-body { flex: 1; min-width: 200px; }
.score-word { font-size: 15px; font-weight: 700; margin-bottom: 10px; }
.factor-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.factor-list li { display: flex; align-items: flex-start; gap: 9px; font-size: 13.5px; color: var(--text); line-height: 1.5; }
.factor-list .factor-icon { width: 16px; height: 16px; flex-shrink: 0; margin-top: 2px; color: #16a34a; }

@media (max-width: 640px) {
  .trust-score-row { gap: 16px; }
}
.cta-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 28px; }
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 13px 22px; border-radius: 10px; font-weight: 600; font-size: 14.5px;
  transition: background 200ms ease, border-color 200ms ease, color 200ms ease; min-height: 44px;
}
.btn-primary { background: var(--accent); color: #fff; border: 1px solid var(--accent); }
.btn-primary:hover { background: var(--accent-hover); border-color: var(--accent-hover); color: #fff; }
.btn-ghost { background: var(--surface); color: var(--text); border: 1px solid var(--border); }
.btn-ghost:hover { border-color: #94a3b8; color: var(--text); }
.disclaimer { color: #94a3b8; font-size: 13px; margin-top: 24px; }

/* Trust sections below the profile card */
.section { margin-top: 28px; }
.section-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 28px 32px; box-shadow: var(--shadow-sm);
}
.section h2 { font-size: 18px; margin: 0 0 4px; letter-spacing: -0.01em; }
.section .source-note { font-size: 12.5px; color: #94a3b8; margin: 0 0 16px; }
.section p.body-text { font-size: 15px; color: var(--text); margin: 0; line-height: 1.7; }
.section p.muted { font-size: 14.5px; color: var(--text-muted); font-style: italic; margin: 0 0 12px; }
.team-list { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.team-pill {
  display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px;
  border-radius: 999px; background: var(--surface-alt); border: 1px solid var(--border);
  font-size: 13.5px; color: var(--text); font-weight: 500;
}
.team-pill .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent); flex-shrink: 0; }

.reputation { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }
.reputation .score { font-size: 36px; font-weight: 700; color: var(--text); line-height: 1; }
.reputation .stars { display: flex; gap: 2px; margin: 6px 0; }
.reputation .stars svg { width: 16px; height: 16px; color: #f59e0b; }
.reputation .stars svg.star-empty { color: #e2e8f0; }
.reputation .count { color: var(--text-muted); font-size: 13.5px; }

.empty-state {
  text-align: center; padding: 28px 20px; border: 1px dashed var(--border); border-radius: var(--radius-sm);
  background: var(--surface-alt);
}
.empty-state p { margin: 0 0 16px; color: var(--text-muted); font-size: 14.5px; }
.empty-state .cta-row { justify-content: center; margin-top: 0; }
.btn-sm { padding: 10px 18px; font-size: 13.5px; min-height: 40px; }

/* Reviews */
.review-card { padding: 16px 0; border-bottom: 1px solid var(--border); }
.review-card:last-child { border-bottom: none; }
.review-top { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; flex-wrap: wrap; }
.review-avatar {
  width: 34px; height: 34px; border-radius: 50%; background: var(--surface-alt); color: var(--text-muted);
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; flex-shrink: 0;
}
.review-name { font-weight: 600; font-size: 14px; }
.review-date { color: #94a3b8; font-size: 12.5px; }
.review-stars { display: flex; gap: 1px; }
.review-stars svg { width: 13px; height: 13px; color: #f59e0b; }
.review-stars svg.star-empty { color: #e2e8f0; }
.review-text { font-size: 14.5px; color: var(--text); margin: 6px 0 0 44px; line-height: 1.6; }

details.more-reviews { margin-top: 2px; }
details.more-reviews summary {
  cursor: pointer; font-size: 14px; color: var(--accent); font-weight: 600; padding: 14px 0 4px; list-style: none;
}
details.more-reviews summary::-webkit-details-marker { display: none; }
details.more-reviews summary .label-closed { display: inline; }
details.more-reviews summary .label-open { display: none; }
details.more-reviews[open] summary .label-closed { display: none; }
details.more-reviews[open] summary .label-open { display: inline; }

details.form-disclosure { margin-top: 22px; }
details.form-disclosure summary {
  cursor: pointer; font-weight: 600; color: var(--accent); list-style: none; padding: 8px 0; font-size: 14.5px;
}
details.form-disclosure summary::-webkit-details-marker { display: none; }
.form-box { margin-top: 14px; padding: 22px; border: 1px solid var(--border); border-radius: var(--radius-sm); background: var(--surface-alt); }
.form-row { margin-bottom: 14px; }
.form-row label { display: block; font-size: 13px; font-weight: 600; color: var(--text-muted); margin-bottom: 6px; }
.form-row input[type=text], .form-row input[type=email], .form-row textarea, .form-row input[type=file] {
  width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 14px;
  font-family: inherit; background: var(--surface); color: var(--text);
}
.form-row input:focus, .form-row textarea:focus { border-color: var(--accent); outline: none; box-shadow: 0 0 0 3px var(--accent-soft); }
.form-row textarea { min-height: 90px; resize: vertical; }
.radio-row { display: flex; gap: 18px; flex-wrap: wrap; }
.radio-row label { display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 500; color: var(--text); }
.star-picker { display: flex; gap: 4px; }
.star-picker svg { width: 24px; height: 24px; color: #e2e8f0; cursor: pointer; transition: color 150ms ease; }
.star-picker svg.active { color: #f59e0b; }
.form-note { font-size: 12.5px; color: #94a3b8; margin-top: 12px; }
.form-error { font-size: 13px; color: #dc2626; margin: 10px 0 0; min-height: 1em; }
.thank-you { display: none; text-align: center; padding: 12px; }
.thank-you.show { display: block; }
.thank-you p { margin: 0 0 12px; color: var(--text); font-weight: 500; font-size: 14.5px; }

/* Cases */
.case-card { padding: 22px 0; border-bottom: 1px solid var(--border); }
.case-card:last-child { border-bottom: none; }
.case-badge {
  display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 600;
  padding: 4px 10px; border-radius: 999px; margin-bottom: 10px;
}
.case-badge.client { background: var(--accent-soft); color: var(--accent-hover); }
.case-badge.broker { background: var(--surface-alt); color: var(--text-muted); border: 1px solid var(--border); }
.case-title { font-size: 16.5px; font-weight: 600; margin: 0 0 8px; letter-spacing: -0.005em; }
.case-text { font-size: 14.5px; color: var(--text); line-height: 1.7; margin: 0 0 16px; }
.media-row { display: flex; gap: 10px; flex-wrap: wrap; }
.media-tile {
  width: 88px; height: 88px; border-radius: 10px; background: var(--surface);
  border: 1px dashed var(--border); display: flex; flex-direction: column;
  align-items: center; justify-content: center; color: #94a3b8; gap: 4px; font-size: 10.5px;
}
.media-tile svg { width: 20px; height: 20px; }

@media (prefers-reduced-motion: no-preference) {
  .results-list .result { animation: fadeUp 320ms ease both; }
  .results-list .result:nth-child(1) { animation-delay: 0ms; }
  .results-list .result:nth-child(2) { animation-delay: 30ms; }
  .results-list .result:nth-child(3) { animation-delay: 60ms; }
  .results-list .result:nth-child(4) { animation-delay: 90ms; }
  .results-list .result:nth-child(5) { animation-delay: 120ms; }
  .results-list .result:nth-child(n+6) { animation-delay: 150ms; }
  @keyframes fadeUp { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
}

@media (max-width: 640px) {
  .hero { padding: 48px 0 28px; }
  .fact-grid { grid-template-columns: 1fr; }
  .profile-card { padding: 24px; }
  .result .meta { white-space: normal; }
}
"""

SEARCH_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>"""
CHEVRON_ICON = """<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>"""
PHONE_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.7a2 2 0 0 1-.5 2.1L8 9.7a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.5 2.7.6a2 2 0 0 1 1.7 2z"/></svg>"""
BACK_ICON = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>"""
EYE_ICON = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>"""
CHECK_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="8 12.5 11 15.5 16 9"/></svg>"""
ALERT_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4"/><path d="M10.3 3.9 1.9 18a1.7 1.7 0 0 0 1.5 2.6h17.2a1.7 1.7 0 0 0 1.5-2.6L13.7 3.9a1.7 1.7 0 0 0-3.4 0Z"/><circle cx="12" cy="16.5" r="0.3" fill="currentColor"/></svg>"""
CLOCK_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 14"/></svg>"""
SHIELD_ICON = """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 4 5v6c0 5 3.4 8.4 8 11 4.6-2.6 8-6 8-11V5z"/></svg>"""
STAR_FILLED = """<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.63 22 9.24 16.5 14.14 18.18 21 12 17.27 5.82 21 7.5 14.14 2 9.24 8.91 8.63"/></svg>"""
STAR_EMPTY = """<svg class="star-empty" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.63 22 9.24 16.5 14.14 18.18 21 12 17.27 5.82 21 7.5 14.14 2 9.24 8.91 8.63"/></svg>"""
PHOTO_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="1.8"/><path d="m21 16-5.5-5.5L4 21"/></svg>"""
PLAY_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polygon points="10 8 16 12 10 16" fill="currentColor" stroke="none"/></svg>"""
STAR_PICKER_ICON = """<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.63 22 9.24 16.5 14.14 18.18 21 12 17.27 5.82 21 7.5 14.14 2 9.24 8.91 8.63"/></svg>"""

PAGE_HEAD = """<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="color-scheme" content="light">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../assets/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="../assets/apple-touch-icon.png">
<style>{style}</style>
</head>
<body>
<header class="site">
  <div class="bar">
    <a class="brand" href="{home}"><img class="mark" src="../assets/favicon-32.png" alt="" width="30" height="30">Broker Directory</a>
  </div>
</header>
<main>
"""

FORM_SCRIPT = """
document.querySelectorAll('.reveal-btn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var value = document.getElementById(btn.dataset.target);
    value.classList.add('shown');
    btn.classList.add('hidden');
  });
});

document.querySelectorAll('.star-picker').forEach(function (picker) {
  var stars = picker.querySelectorAll('svg');
  var ratingInput = picker.parentElement.querySelector('input[type=hidden]');
  stars.forEach(function (star, idx) {
    star.addEventListener('click', function () {
      stars.forEach(function (s, i) { s.classList.toggle('active', i <= idx); });
      if (ratingInput) ratingInput.value = idx + 1;
    });
  });
});

document.querySelectorAll('.live-form').forEach(function (form) {
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var box = form.closest('.form-box');
    var errorEl = box.querySelector('.form-error');
    var submitBtn = form.querySelector('button[type=submit]');

    var payload = { broker_slug: form.dataset.brokerSlug, broker_name: form.dataset.brokerName };
    form.querySelectorAll('[name]').forEach(function (field) {
      if (field.type === 'file' || field.disabled) return;
      if (field.type === 'radio') { if (field.checked) payload[field.name] = field.value; }
      else { payload[field.name] = field.value; }
    });
    if (payload.rating !== undefined) payload.rating = parseInt(payload.rating, 10);

    errorEl.textContent = '';
    submitBtn.disabled = true;

    fetch(form.dataset.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
      .then(function (result) {
        submitBtn.disabled = false;
        if (!result.ok) {
          errorEl.textContent = (result.data && result.data.error) || 'Something went wrong — please try again.';
          return;
        }
        box.querySelector('.form-fields').style.display = 'none';
        box.querySelector('.thank-you').classList.add('show');
      })
      .catch(function () {
        submitBtn.disabled = false;
        errorEl.textContent = 'Could not reach the server — please try again.';
      });
  });
});

document.querySelectorAll('.submit-another').forEach(function (link) {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    var box = link.closest('.form-box');
    box.querySelector('.thank-you').classList.remove('show');
    box.querySelector('.form-fields').style.display = '';
    var form = box.querySelector('form');
    if (form) form.reset();
    box.querySelectorAll('.star-picker svg').forEach(function (s) { s.classList.remove('active'); });
  });
});
"""

PAGE_FOOT = """
</main>
<footer class="site">AU Broker Directory &mdash; independent directory, not affiliated with any listed business.</footer>
</body>
</html>
"""


def broker_page(b):
    title = f"{b['name']} — {b['category']} in {b['city']}, {b['state']} | AU Broker Directory"
    desc = f"Contact details for {b['name']}, a {b['category'].lower()} based in {b['suburb'] or b['city']}, {b['state']}."
    canonical = f"{SITE_URL}/broker/{b['slug']}.html"

    jsonld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": b["name"],
        "telephone": b["phone"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": b["address"],
            "addressLocality": b["suburb"] or b["city"],
            "addressRegion": b["state"],
            "postalCode": b["postcode"],
            "addressCountry": "AU",
        },
    }
    if b["email_display"]:
        jsonld["email"] = b["email_display"]
    if b["website"]:
        jsonld["url"] = b["website"]
    if b["rating"]:
        jsonld["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": b["rating"],
            "reviewCount": b["reviews"] or 0,
        }

    def reveal_field(kind, value, label, href_prefix=None):
        if not value:
            return "—"
        field_id = f"{kind}-{b['slug']}"
        value_esc = html.escape(value)
        if href_prefix:
            # tel: / mailto: - fine to click, opens the phone/mail app rather than navigating away.
            value_html = f'<a href="{href_prefix}{value_esc}" id="{field_id}" class="reveal-value">{value_esc}</a>'
        else:
            # Plain, non-clickable text - copy/paste only, so revealing it doesn't send
            # people straight to the broker's own site from ours.
            value_html = f'<span id="{field_id}" class="reveal-value reveal-text">{value_esc}</span>'
        return (
            f'<span class="reveal-field">'
            f'<button type="button" class="reveal-btn" data-target="{field_id}">{EYE_ICON}Reveal {label}</button>'
            f'{value_html}'
            f'</span>'
        )

    rows = [
        ("Category", html.escape(b["category"])),
        ("Suburb", html.escape(b["suburb"] or "—")),
        ("State", html.escape(b["state"] or "—")),
        ("Postcode", html.escape(b["postcode"] or "—")),
        ("Phone", reveal_field("phone", b["phone"], "phone", href_prefix="tel:")),
        ("Email", reveal_field("email", b["email_display"], "email", href_prefix="mailto:")),
        ("Website", reveal_field("website", b["website"], "website")),
        ("Rating", f'{b["rating"]} / 5 &nbsp;·&nbsp; {b["reviews"]} reviews' if b["rating"] else "—"),
    ]
    grid_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)

    home_rel = "../index.html"
    name_esc = html.escape(b["name"])
    claim_mailto = f'mailto:hello@aubrokerdirectory.com.au?subject=Claim%20your%20listing%20-%20{name_esc}'

    # --- Trust score: a real, computed aggregate from data we actually hold
    # (Google rating + review volume + licence disclosure). Every input shown
    # is either real or an honest neutral - we never expose our own gaps
    # (e.g. "we haven't checked X yet") as if that were a finding about them.
    review_count = b.get("reviews") or 0
    score = b["trust_score"]

    if score >= 85:
        score_color, score_word = "#16a34a", "Trustworthy"
    elif score >= 70:
        score_color, score_word = "#d97706", "Generally positive"
    else:
        score_color, score_word = "#dc2626", "Needs a closer look"

    factors = []
    if b.get("rating"):
        factors.append((CHECK_ICON, "#16a34a", f"{b['rating']}/5 from {review_count} Google reviews"))
    if b.get("license_disclosed"):
        factors.append((CHECK_ICON, "#16a34a", f"Licence publicly disclosed — {html.escape(b['license_detail'])}"))
    else:
        factors.append((ALERT_ICON, "#d97706", "Licence number not disclosed on their website"))
    factors_html = "".join(
        f"<li>{icon.replace('<svg ', f'<svg class=\"factor-icon\" style=\"color:{color}\" ')}<span>{text}</span></li>"
        for icon, color, text in factors
    )

    trust_html = f"""
<div class="section">
  <div class="section-card">
    <h2>Trust score</h2>
    <p class="source-note">Calculated from their Google reputation and what they publicly disclose. Updates as more signals come in — reviews, cases and complaints all move it.</p>
    <div class="trust-score-row">
      <div class="score-ring" style="background: conic-gradient({score_color} {score}%, var(--surface-alt) 0);">
        <div class="score-ring-inner">
          <span class="score-num">{score}%</span>
        </div>
      </div>
      <div class="trust-score-body">
        <div class="score-word" style="color:{score_color};">{score_word}</div>
        <ul class="factor-list">{factors_html}</ul>
      </div>
    </div>
  </div>
</div>"""

    # --- About section ---
    if b.get("about"):
        about_html = f"""
<div class="section">
  <div class="section-card">
    <h2>About {name_esc}</h2>
    <p class="source-note">Summarised from {html.escape(b.get('about_source') or 'their website')}.</p>
    <p class="body-text">{html.escape(b['about'])}</p>
    {'<div class="team-list">' + ''.join(f'<span class="team-pill"><span class="dot"></span>{html.escape(t)}</span>' for t in b.get('team', [])) + '</div>' if b.get('team') else ''}
  </div>
</div>"""
    else:
        about_html = f"""
<div class="section">
  <div class="section-card">
    <h2>About {name_esc}</h2>
    <div class="empty-state">
      <p>This business hasn't shared their story yet — we couldn't pull a public description automatically either.</p>
      <div class="cta-row empty-state-cta">
        <a class="btn btn-primary btn-sm" href="{claim_mailto}">Is this your business? Add your story</a>
      </div>
    </div>
  </div>
</div>"""

    # --- Reputation section: real aggregate score + a real submission form.
    # No sample/mock reviews - honest empty state until real ones exist.
    if b.get("rating"):
        rating = float(b["rating"])
        full_stars = round(rating)
        summary_stars = "".join(STAR_FILLED if i < full_stars else STAR_EMPTY for i in range(5))

        reputation_html = f"""
<div class="section">
  <div class="section-card">
    <h2>Reputation</h2>
    <p class="source-note">Overall score is real, from their Google Business listing.</p>
    <div class="reputation">
      <div>
        <div class="score">{b['rating']}</div>
        <div class="stars">{summary_stars}</div>
        <div class="count">{b.get('reviews') or 0} reviews on Google</div>
      </div>
    </div>
    <div class="empty-state" style="margin-top:20px;">
      <p>No reviews published on our site yet for {name_esc}. Be the first to share yours.</p>
    </div>
    <details class="form-disclosure">
      <summary>+ Write a review</summary>
      <div class="form-box">
        <div class="form-fields">
          <form class="live-form" data-endpoint="/api/reviews" data-broker-slug="{b['slug']}" data-broker-name="{name_esc}">
            <div class="form-row">
              <label for="rev-name-{b['slug']}">Your name</label>
              <input type="text" name="name" id="rev-name-{b['slug']}" placeholder="e.g. Sam W." required>
            </div>
            <div class="form-row">
              <label for="rev-email-{b['slug']}">Your email</label>
              <input type="email" name="email" id="rev-email-{b['slug']}" placeholder="you@example.com" required>
            </div>
            <div class="form-row">
              <label>Your rating</label>
              <div class="star-picker" role="radiogroup" aria-label="Star rating">
                {STAR_PICKER_ICON}{STAR_PICKER_ICON}{STAR_PICKER_ICON}{STAR_PICKER_ICON}{STAR_PICKER_ICON}
              </div>
              <input type="hidden" name="rating" value="0">
            </div>
            <div class="form-row">
              <label for="rev-text-{b['slug']}">Your review</label>
              <textarea name="text" id="rev-text-{b['slug']}" placeholder="What was your experience working with {name_esc}?" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-sm">Submit review</button>
            <p class="form-error" role="alert"></p>
          </form>
          <p class="form-note">Your email is only for us to follow up on this submission — it won't be published. Reviews are checked by our team before publishing, so yours won't appear immediately.</p>
        </div>
        <div class="thank-you">
          <p>Thanks — your review has been submitted and will appear once we've checked it.</p>
          <a href="#" class="submit-another btn btn-ghost btn-sm">Submit another</a>
        </div>
      </div>
    </details>
  </div>
</div>"""
    else:
        reputation_html = ""

    # --- Real cases section: honest empty state + submission form for both sides.
    # Photos/video stay as a described-but-not-yet-built upload path - the
    # placeholder the case format was designed around, not fabricated content.
    stories_html = f"""
<div class="section">
  <div class="section-card">
    <h2>Real cases</h2>
    <p class="source-note">Real examples of how {name_esc} has helped people — shared by clients or the brokerage itself.</p>
    <div class="empty-state">
      <p>No real cases shared yet for {name_esc}. A case is a short story of what happened, plus photos or a video once uploads are live — be the first to add one.</p>
      <div class="media-row" style="justify-content:center;">
        <div class="media-tile">{PHOTO_ICON}<span>Photo</span></div>
        <div class="media-tile">{PHOTO_ICON}<span>Photo</span></div>
        <div class="media-tile">{PHOTO_ICON}<span>Photo</span></div>
        <div class="media-tile video">{PLAY_ICON}<span>Video</span></div>
      </div>
    </div>
    <details class="form-disclosure">
      <summary>+ Share a real case</summary>
      <div class="form-box">
        <div class="form-fields">
          <form class="live-form" data-endpoint="/api/cases" data-broker-slug="{b['slug']}" data-broker-name="{name_esc}">
            <div class="form-row">
              <label>I'm submitting as</label>
              <div class="radio-row">
                <label><input type="radio" name="role" value="client" checked> A client</label>
                <label><input type="radio" name="role" value="broker"> This brokerage</label>
              </div>
            </div>
            <div class="form-row">
              <label for="case-name-{b['slug']}">Your name</label>
              <input type="text" name="name" id="case-name-{b['slug']}" placeholder="e.g. Sam W." required>
            </div>
            <div class="form-row">
              <label for="case-email-{b['slug']}">Your email</label>
              <input type="email" name="email" id="case-email-{b['slug']}" placeholder="you@example.com" required>
            </div>
            <div class="form-row">
              <label for="case-text-{b['slug']}">What happened?</label>
              <textarea name="text" id="case-text-{b['slug']}" placeholder="What was the situation, what did they do, and how did it turn out?" required></textarea>
            </div>
            <div class="form-row">
              <label for="case-photos-{b['slug']}">Photos (optional)</label>
              <input type="file" id="case-photos-{b['slug']}" multiple accept="image/*" disabled>
              <p class="form-note" style="margin-top:6px;">Photo upload is coming soon — for now, submit your story and we'll follow up for photos by email.</p>
            </div>
            <button type="submit" class="btn btn-primary btn-sm">Submit case</button>
            <p class="form-error" role="alert"></p>
          </form>
          <p class="form-note">Your email is only for us to follow up on this submission — it won't be published. Submissions are checked by our team before publishing, so nothing appears immediately.</p>
        </div>
        <div class="thank-you">
          <p>Thanks — this has been submitted and will appear once we've checked it.</p>
          <a href="#" class="submit-another btn btn-ghost btn-sm">Submit another</a>
        </div>
      </div>
    </details>
  </div>
</div>"""

    body = f"""
<a class="back-link" href="{home_rel}">{BACK_ICON} Back to directory</a>
<div class="profile-card">
  <div class="profile-head">
    <div class="avatar">{html.escape(b['initial'])}</div>
    <div>
      <span class="badge">{html.escape(b['category'])}</span>
      <h1>{name_esc}</h1>
      <p class="addr">{html.escape(b['address'] or '')}</p>
    </div>
  </div>
  <dl class="fact-grid">{grid_html}</dl>
  <p class="disclaimer">Listing sourced from public business records. Contact us to verify, update or remove your details.</p>
</div>
{trust_html}
{about_html}
{reputation_html}
{stories_html}
<script type="application/ld+json">{json.dumps(jsonld)}</script>
<script>{FORM_SCRIPT}</script>
"""
    return (
        PAGE_HEAD.format(title=title, description=desc, canonical=canonical, home=home_rel, style=STYLE)
        + body
        + PAGE_FOOT
    )


def category_chips_html():
    out = []
    for c in CATEGORIES:
        cls = "chip active" if c["active"] else "chip disabled"
        label = f'{html.escape(c["name"])} <span class="count">{c["count"]:,}</span>'
        out.append(f'<span class="{cls}">{label}</span>')
    return "".join(out)


INDEX_HTML = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AU Broker Directory — Find a broker near you</title>
<meta name="description" content="Search Australian mortgage, finance and insurance brokers by name, phone or city.">
<meta name="color-scheme" content="light">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<style>{STYLE}</style>
</head>
<body>
<header class="site">
  <div class="bar">
    <a class="brand" href="index.html"><img class="mark" src="assets/favicon-32.png" alt="" width="30" height="30">Broker Directory</a>
  </div>
</header>
<main>
  <section class="hero">
    <h1>Find a broker you can trust</h1>
    <p class="lede">Search Australian mortgage &amp; finance brokers by name, suburb or phone number.</p>
    <div class="search-wrap">
      {SEARCH_ICON}
      <input id="q" type="text" placeholder="Try “Sydney”, a broker's name, or a phone number…" autocomplete="off" aria-label="Search brokers">
    </div>
    <div class="categories">
      {category_chips_html()}
    </div>
    <p class="policy-ribbon">{SHIELD_ICON} Independent listings — brokers can't pay for a better rank or to remove a review.</p>
  </section>

  <div class="results-head">
    <span class="hint" id="hint"></span>
  </div>
  <div class="results-list" id="results"></div>
</main>
<footer class="site">AU Broker Directory &mdash; independent directory, not affiliated with any listed business.</footer>
<script>
const LIMIT = 9;
let data = [];

fetch('data.json').then(r => r.json()).then(d => {{ data = d; renderEmpty(); }});

function renderEmpty() {{
  document.getElementById('hint').textContent =
    `Start typing a suburb, name or phone number to search ${{data.length}} mortgage brokers.`;
  document.getElementById('results').innerHTML = '';
}}

function scoreTier(score) {{
  if (score >= 85) return {{ bg: '#dcfce7', fg: '#16a34a' }};
  if (score >= 70) return {{ bg: '#fef3c7', fg: '#d97706' }};
  return {{ bg: '#fee2e2', fg: '#dc2626' }};
}}

function render(query) {{
  const q = query.trim().toLowerCase();
  const hint = document.getElementById('hint');
  const results = document.getElementById('results');

  if (!q) {{ renderEmpty(); return; }}

  let matches = data.filter(b =>
    b.name.toLowerCase().includes(q) ||
    b.city.toLowerCase().includes(q) ||
    (b.suburb || '').toLowerCase().includes(q) ||
    b.state.toLowerCase().includes(q) ||
    (b.phone || '').replace(/\\s/g,'').includes(q.replace(/\\s/g,''))
  );
  matches.sort((a, b) => b.score - a.score);

  const shown = matches.slice(0, LIMIT);
  hint.textContent = matches.length > LIMIT
    ? `Top ${{LIMIT}} of ${{matches.length}} matches, ranked by trust score — search a full name for an exact match`
    : `${{shown.length}} match${{shown.length===1?'':'es'}} found`;

  if (shown.length === 0) {{
    results.innerHTML = '<div class="empty">No brokers found. Try a different city or name.</div>';
    return;
  }}

  results.innerHTML = shown.map(b => {{
    const tier = scoreTier(b.score);
    const phoneFlag = b.phone
      ? `<span class="phone-flag">{PHONE_ICON} Phone on file</span>`
      : '';
    return `
    <a class="result" href="broker/${{b.slug}}.html">
      <div class="avatar">${{b.name.charAt(0).toUpperCase()}}</div>
      <div class="body">
        <div class="name-row">
          <span class="name">${{b.name}}</span>
          <span class="score-pill" style="background:${{tier.bg}};color:${{tier.fg}};">${{b.score}}%</span>
        </div>
        <div class="meta">${{b.category}} · ${{b.suburb || b.city}}, ${{b.state}}${{phoneFlag ? ' · ' + phoneFlag : ''}}</div>
      </div>
      {CHEVRON_ICON}
    </a>
  `;
  }}).join('');
}}

document.getElementById('q').addEventListener('input', e => render(e.target.value));
</script>
</body>
</html>
"""

# --- write output ---
SITE.mkdir(exist_ok=True)
(SITE / "broker").mkdir(exist_ok=True)

with open(SITE / "index.html", "w") as f:
    f.write(INDEX_HTML)

search_index = [
    {
        "slug": b["slug"], "name": b["name"], "category": b["category"],
        "city": b["city"], "suburb": b["suburb"], "state": b["state"], "phone": b["phone"],
        "score": b["trust_score"],
    }
    for b in brokers
]
with open(SITE / "data.json", "w") as f:
    json.dump(search_index, f, indent=2, ensure_ascii=False)

for b in brokers:
    with open(SITE / "broker" / f"{b['slug']}.html", "w") as f:
        f.write(broker_page(b))

urls = [f"{SITE_URL}/index.html"] + [f"{SITE_URL}/broker/{b['slug']}.html" for b in brokers]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
sitemap += "</urlset>\n"
with open(SITE / "sitemap.xml", "w") as f:
    f.write(sitemap)

print(f"Built {len(brokers)} broker pages + index + sitemap into {SITE}")
