"""
City Hub Template for Best Brokers Australia.
Implements Blueprint Section 5.1 (City/category hub) — Top 9 verified specialists.
"""
from ..config import SITE_NAME, SITE_URL
from ..components.base import render_page
from ..components.breadcrumbs import render_breadcrumbs, breadcrumbs_jsonld
from ..components.broker_card import render_broker_card
from ..seo.schema import hub_collection_schema


def render_city_page(hub, page: int = 1) -> str:
    """Renders a city category hub page with local top 9 broker cards and nearby navigation."""
    total_brokers = len(hub.brokers)
    page_brokers = hub.brokers[:9]

    # Nearby cities chips
    nearby_chips_html = "".join(
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

    content = f"""
{render_breadcrumbs(hub.breadcrumbs)}

<div class="hero">
  <div class="container">
    <span class="hero-category-badge">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      Local City Hub &middot; {hub.city_name}, {hub.state_code}
    </span>
    <h1>{hub.h1}</h1>
    <p class="hero-lead">{hub.intro_text}</p>
    
    <div class="hero-stats">
      <div class="hero-stat-item">
        <strong>{total_brokers:,}</strong> Verified {hub.category_short}
      </div>
      <div class="hero-stat-item">
        Location: <strong>{hub.city_name}, {hub.state_code}</strong>
      </div>
      <div class="hero-stat-item">
        Updated: <strong>September 2026</strong>
      </div>
    </div>
  </div>
</div>

{f'''
<section class="section section-alt" style="padding:1.75rem 0;">
  <div class="container">
    <div style="font-size:0.875rem;font-weight:600;color:var(--text-muted);margin-bottom:0.75rem;text-transform:uppercase;letter-spacing:0.05em;">
      Nearby Locations in {hub.state_name or hub.state_code}:
    </div>
    <div class="location-chips">
      {nearby_chips_html}
    </div>
  </div>
</section>
''' if hub.sub_locations else ''}

<section class="section">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">Top 9 Verified {hub.category_short} in {hub.city_name}</h2>
        <p class="section-subtitle">Ranked by independent Trust Score (Google rating + review volume + licence disclosures)</p>
      </div>
    </div>
    
    <div class="broker-grid">
      {cards_html}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:840px;">
    <h2 class="section-title" style="margin-bottom:1.5rem;">{hub.city_name} Selection &amp; Advisory FAQs</h2>
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
