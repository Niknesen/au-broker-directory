"""
State Hub Template for Best Brokers Australia.
"""
import math
from ..config import SITE_NAME, SITE_URL, BROKERS_PER_PAGE
from ..components.base import render_page
from ..components.breadcrumbs import render_breadcrumbs, breadcrumbs_jsonld
from ..components.broker_card import render_broker_card
from ..components.pagination import render_pagination
from ..seo.schema import hub_collection_schema


def render_state_page(hub, page: int = 1) -> str:
    """Renders a state category hub page with city navigation and broker cards."""
    total_brokers = len(hub.brokers)
    total_pages = max(1, math.ceil(total_brokers / BROKERS_PER_PAGE))
    start_idx = (page - 1) * BROKERS_PER_PAGE
    page_brokers = hub.brokers[start_idx : start_idx + BROKERS_PER_PAGE]

    # City chips
    city_chips_html = "".join(
        f'<a class="location-chip" href="{c["url"]}">{c["name"]} <span class="count">{c["count"]}</span></a>'
        for c in hub.sub_locations
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

    pagination_html = render_pagination(hub.canonical_url, page, total_pages)
    page_canonical = hub.canonical_url if page == 1 else f"{hub.canonical_url.rstrip('/')}/?page={page}"

    content = f"""
{render_breadcrumbs(hub.breadcrumbs)}

<div class="hero">
  <div class="container">
    <span class="hero-category-badge">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      State Hub &middot; {hub.state_name}
    </span>
    <h1>{hub.h1}</h1>
    <p class="hero-lead">{hub.intro_text}</p>
    
    <div class="hero-stats">
      <div class="hero-stat-item">
        <strong>{total_brokers:,}</strong> {hub.category_short} in {hub.state_code}
      </div>
      <div class="hero-stat-item">
        <strong>{len(hub.sub_locations)}</strong> Cities &amp; Regions
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
        <h2 class="section-title">Key Cities &amp; Regions in {hub.state_name}</h2>
        <p class="section-subtitle">Select a city to compare local specialists with active office locations</p>
      </div>
    </div>
    <div class="location-chips">
      {city_chips_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">Top-Rated {hub.category_short} in {hub.state_name}</h2>
        <p class="section-subtitle">Showing {len(page_brokers)} of {total_brokers:,} specialists ranked by Trust Score</p>
      </div>
    </div>
    
    <div class="broker-grid">
      {cards_html}
    </div>

    {pagination_html}
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:840px;">
    <h2 class="section-title" style="margin-bottom:1.5rem;">{hub.state_name} Lending &amp; Advisory FAQs</h2>
    <div class="card" style="padding:0.5rem 1.75rem;">
      {faqs_html}
    </div>
  </div>
</section>
"""

    return render_page(
        title=hub.title,
        meta_description=hub.meta_description,
        canonical_url=page_canonical,
        content_html=content,
        active_nav=hub.canonical_url,
        is_indexable=hub.is_indexable and (page == 1),
        schema_jsonld=[
            hub_collection_schema(hub),
            breadcrumbs_jsonld(hub.breadcrumbs),
        ],
    )
