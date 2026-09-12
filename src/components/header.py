"""
Centralized Header component for Best Brokers Australia.
Includes brand logo, live running ticker banner, and master navigation.
"""
from ..config import SITE_NAME
from ..taxonomy import CATEGORIES, url_for_home, url_for_category, url_for_page


def render_header(active_path: str = "") -> str:
    """Renders the single canonical source of truth for the site header with dynamic running text ticker."""
    top_categories = [
        ("Mortgage", "mortgage-brokers"),
        ("Insurance", "insurance-brokers"),
        ("Real Estate", "real-estate-agents"),
        ("Commercial", "business-brokers"),
        ("Wealth", "wealth-advisers"),
    ]

    nav_items_html = []
    for label, slug in top_categories:
        url = url_for_category(slug)
        is_active = "active" if active_path.startswith(url) else ""
        nav_items_html.append(f'<li><a href="{url}" class="{is_active}">{label}</a></li>')

    is_methodology_active = "active" if active_path == "/methodology/" else ""
    is_about_active = "active" if active_path == "/about/" else ""
    is_contact_active = "active" if active_path == "/contact/" else ""

    nav_items_html.append(f'<li><a href="/methodology/" class="{is_methodology_active}">Methodology</a></li>')
    nav_items_html.append(f'<li><a href="/about/" class="{is_about_active}">About</a></li>')
    nav_items_html.append(f'<li><a href="/contact/" class="{is_contact_active}">Contact</a></li>')

    ticker_content = """
    <span class="ticker-item">★ <strong>16,917 Verified Australian Brokers</strong></span>
    <span class="ticker-sep">&bull;</span>
    <span class="ticker-item">Independent 3-Factor Trust Scores</span>
    <span class="ticker-sep">&bull;</span>
    <span class="ticker-item"><strong>Sydney &middot; Melbourne &middot; Brisbane &middot; Perth &middot; Adelaide &middot; Canberra &middot; Gold Coast</strong></span>
    <span class="ticker-sep">&bull;</span>
    <span class="ticker-item">Zero Pay-To-Rank Guarantee</span>
    <span class="ticker-sep">&bull;</span>
    <span class="ticker-item">Real Google Maps Reviews Verified</span>
    <span class="ticker-sep">&bull;</span>
    <span class="ticker-item">Mortgage &middot; Insurance &middot; Real Estate &middot; Commercial &middot; Wealth</span>
    <span class="ticker-sep">&bull;</span>
    """

    return f"""
<div class="ticker-wrap" aria-label="Directory Live Data Stream">
  <div class="ticker-track">
    {ticker_content}
    {ticker_content}
  </div>
</div>

<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{url_for_home()}">
      <img class="brand-mark" src="/assets/favicon-32.png" alt="Best Brokers Australia Logo" width="32" height="32">
      <span>{SITE_NAME}</span>
    </a>
    <nav>
      <ul class="nav-links">
        {''.join(nav_items_html)}
      </ul>
    </nav>
    <a class="header-cta" href="/claim-profile/">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      Claim Profile
    </a>
  </div>
</header>
"""
