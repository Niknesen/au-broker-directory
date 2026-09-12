"""
Reusable Broker Card component for category, state, city hubs and search.
The entire card is clickable to open the profile page directly.
"""
import html
from .trust_badge import render_trust_pill
from ..taxonomy import url_for_broker


def render_broker_card(b) -> str:
    """Renders a single broker comparison card where the entire card is clickable."""
    initial = html.escape((b.name or "B")[0].upper())
    name_escaped = html.escape(b.name or "Broker")
    category_escaped = html.escape(b.category or "Broker")
    location_escaped = html.escape(b.display_location or "Australia")
    profile_url = url_for_broker(b.slug)

    # Badges
    badges = []
    if b.rating > 0 and b.reviews_count > 0:
        badges.append(f'<span class="badge-item">&#9733; {b.rating:.1f} ({b.reviews_count} reviews)</span>')
    if b.phone:
        badges.append('<span class="badge-item">Direct Phone</span>')
    if b.license_disclosed:
        badges.append('<span class="badge-item" style="color:var(--success);background:var(--success-bg);">Licence on File</span>')
    if len(b.google_reviews) > 0:
        badges.append(f'<span class="badge-item" style="color:var(--primary);background:var(--primary-light);">{len(b.google_reviews)} Full Reviews</span>')

    return f"""
<a class="broker-card" href="{profile_url}" itemscope itemtype="https://schema.org/LocalBusiness">
  <meta itemprop="name" content="{name_escaped}">
  <meta itemprop="url" content="{profile_url}">
  
  <div class="broker-card-top">
    <div class="broker-avatar" aria-hidden="true">{initial}</div>
    <div class="broker-title-group">
      <h3 class="broker-name">{name_escaped}</h3>
      <div class="broker-meta">
        <span>{category_escaped}</span>
        <span class="sep">&middot;</span>
        <span itemprop="address">{location_escaped}</span>
      </div>
    </div>
    {render_trust_pill(b.trust_score)}
  </div>

  <div class="broker-badges">
    {''.join(badges)}
  </div>

  <div class="broker-card-footer">
    <span style="font-size:0.8125rem;color:var(--text-muted);">
      {'&#10003; Verified Entity' if b.place_id else 'Directory Listing'}
    </span>
    <span class="btn-card">
      View Profile &amp; Reviews &rarr;
    </span>
  </div>
</a>
"""
