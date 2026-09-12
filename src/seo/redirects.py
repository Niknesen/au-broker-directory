"""
Cloudflare Pages _redirects and _headers generator.
Implements Blueprint Section 3.1 (Canonical host and URL policy) and Phase 5.
"""
from pathlib import Path
from ..config import SITE_URL


def generate_cloudflare_config(output_dir: Path):
    """
    Generates Cloudflare Pages native _redirects and _headers files:
      - Enforces 301 redirects from legacy .html URLs to extensionless canonical URLs.
      - Sets edge caching and strict security headers.
    """
    # 1. _redirects
    redirects_content = """# Best Brokers Australia Cloudflare Pages Redirects
# 301 Permanent Redirects for legacy .html pages to canonical clean paths

/index.html                     /                           301
/about.html                     /about/                     301
/contact.html                   /contact/                   301
/privacy.html                   /privacy/                   301
/methodology.html               /methodology/               301
/editorial-policy.html          /editorial-policy/          301
/review-policy.html             /review-policy/             301
/claim-profile.html             /claim-profile/             301

# Wildcard pattern for legacy broker .html pages
/broker/:slug.html              /broker/:slug/              301

# Clean search redirect
/search/index.html              /                           301
/search                         /                           302
"""

    with open(output_dir / "_redirects", "w", encoding="utf-8") as f:
        f.write(redirects_content.strip() + "\n")

    # 2. _headers
    headers_content = """# Global Security and Edge Performance Headers
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()

# Cache static assets aggressively (immutable)
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# Cache search index with validation
/data.json
  Cache-Control: public, max-age=3600, must-revalidate

# HTML pages edge caching
/*.html
  Cache-Control: public, max-age=1800, stale-while-revalidate=86400
"""

    with open(output_dir / "_headers", "w", encoding="utf-8") as f:
        f.write(headers_content.strip() + "\n")
