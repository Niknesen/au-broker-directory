"""
Category Hub Template for Best Brokers Australia.
Implements Blueprint Section 5.1 (City/category hub) — Top 9 verified specialists.
"""
from typing import List
from ..config import SITE_NAME, SITE_URL
from ..components.base import render_page
from ..components.breadcrumbs import render_breadcrumbs, breadcrumbs_jsonld
from ..components.broker_card import render_broker_card
from ..seo.schema import hub_collection_schema


def render_category_page(hub, page: int = 1) -> str:
    """Renders a national category hub page with state/city navigation and top 9 broker cards."""
    total_brokers = len(hub.brokers)
    page_brokers = hub.brokers[:9]

    # State chips
    state_chips_html = "".join(
        f'<a class="location-chip" href="{s["url"]}">{s["name"]} ({s["code"]}) <span class="count">{s["count"]}</span></a>'
        for s in hub.sub_locations
    )

    # Broker cards
    cards_html = "".join(render_broker_card(b) for b in page_brokers)

    # FAQs HTML
    faqs_html = "".join(f"""
    <div class="faq-item">
      <h3 class="faq-q">{faq['q']}</h3>
      <p class="faq-a">{faq['a']}</p>
    </div>
    """ for faq in hub.faqs)

    content = f"""
{render_breadcrumbs(hub.breadcrumbs)}

<div class="hero">
  <div class="dynamic-line-glow" aria-hidden="true"></div>
  <div class="dynamic-line-vertical" aria-hidden="true"></div>
  <div class="container">
    <span class="hero-category-badge">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      National Category Guide
    </span>
    <h1>{hub.h1}</h1>
    <p class="hero-lead">{hub.intro_text}</p>
    
    <div class="hero-stats">
      <div class="hero-stat-item">
        <strong>{total_brokers:,}</strong> Total {hub.category_short} on File
      </div>
      <div class="hero-stat-item">
        <strong>8</strong> States &amp; Territories
      </div>
      <div class="hero-stat-item">
        Updated: <strong>September 2026</strong>
      </div>
    </div>
  </div>
</div>

<section class="section section-alt">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">Browse by State &amp; Territory</h2>
        <p class="section-subtitle">Select your state to view local {hub.category_short.lower()} and regional specialists</p>
      </div>
    </div>
    <div class="location-chips">
      {state_chips_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">Top-Ranked {hub.category_short} in Australia</h2>
        <p class="section-subtitle">Showing the top 9 specialists ranked by Trust Score and client feedback</p>
      </div>
    </div>
    
    <div class="broker-grid">
      {cards_html}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:840px;">
    <h2 class="section-title" style="margin-bottom:1.5rem;">Frequently Asked Questions</h2>
    <div class="card" style="padding:0.5rem 1.75rem;">
      {faqs_html}
    </div>
  </div>
</section>
"""

    return render_page(
        title=hub.title,
        meta_description=hub.meta_description,
        canonical_url=hub.canonical_url,
        content_html=content,
        active_nav=hub.canonical_url,
        is_indexable=hub.is_indexable,
        schema_jsonld=[
            hub_collection_schema(hub),
            breadcrumbs_jsonld(hub.breadcrumbs),
        ],
    )
