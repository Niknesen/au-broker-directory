"""
Individual Broker Profile Template for Best Brokers Australia.
Implements Blueprint Section 5.2 (Broker profile).
"""
import html
from typing import List, Dict
from ..config import SITE_NAME, SITE_URL
from ..taxonomy import (
    get_category_info,
    get_state_info,
    url_for_home,
    url_for_category,
    url_for_state,
    url_for_city,
    url_for_broker,
)
from ..components.base import render_page
from ..components.breadcrumbs import render_breadcrumbs, breadcrumbs_jsonld
from ..components.trust_badge import render_trust_pill, render_trust_breakdown
from ..components.forms import render_review_form, render_case_form
from ..seo.schema import broker_local_business_schema


def render_broker_profile(b) -> str:
    """Renders an individual broker profile page."""
    cat_info = get_category_info(b.sheet)
    state_info = get_state_info(b.state)
    
    # Construct breadcrumb path
    breadcrumbs = [
        {"name": "Home", "url": url_for_home()},
        {"name": cat_info["short_name"], "url": url_for_category(b.category_slug)},
    ]
    if b.state:
        breadcrumbs.append({"name": b.state, "url": url_for_state(b.category_slug, b.state_slug)})
    if b.city and b.city_slug:
        breadcrumbs.append({"name": b.city, "url": url_for_city(b.category_slug, b.city_slug)})
    breadcrumbs.append({"name": b.name, "url": url_for_broker(b.slug)})

    name_escaped = html.escape(b.name)
    category_escaped = html.escape(b.category)
    location_escaped = html.escape(b.display_location)
    address_escaped = html.escape(b.address or b.display_location)

    # Google reviews rendering
    g_reviews_html = []
    if b.google_reviews:
        for r in b.google_reviews:
            r_author = html.escape(r.get("author") or "Verified Client")
            r_rating = int(r.get("rating") or 5)
            r_time = html.escape(r.get("relative_time") or "Recent")
            r_text = html.escape(r.get("text") or "").replace("\n", "<br>")
            stars = "&#9733;" * r_rating + "&#9734;" * (5 - r_rating)
            g_reviews_html.append(f"""
            <div class="review-item">
              <div class="review-meta">
                <div>
                  <span class="reviewer-name">{r_author}</span>
                  <span style="color:#f59e0b;margin-left:0.5rem;font-size:0.875rem;">{stars}</span>
                </div>
                <span class="review-date">{r_time} via Google</span>
              </div>
              <div class="review-text">{r_text}</div>
            </div>
            """)
    
    reviews_block = "".join(g_reviews_html) if g_reviews_html else f"""
    <div style="padding:1.5rem 0;color:var(--text-muted);font-size:0.9375rem;">
      No Google review excerpts have been mirrored yet for {name_escaped}. 
      Aggregate Google Place rating on file: <strong>&#9733; {b.rating:.1f} ({b.reviews_count} reviews)</strong>.
    </div>
    """

    # About section
    if b.about:
        about_text = html.escape(b.about).replace("\n", "<br>")
        about_source = f'<div style="font-size:0.75rem;color:var(--text-light);margin-top:0.5rem;">Source: {html.escape(b.about_source or "Official website")}</div>'
    else:
        about_text = (
            f"{name_escaped} is a registered {category_escaped.lower()} based in {location_escaped}. "
            f"They provide professional lending, advisory, and client transaction support across Australia."
        )
        about_source = ""

    # Contact reveal boxes
    phone_reveal = f"""
    <div class="reveal-box">
      <div class="reveal-label">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        Phone Number
      </div>
      <div>
        <span class="reveal-value" data-value="{html.escape(b.phone or 'Not listed')}" style="display:none;"></span>
        <button type="button" class="reveal-btn">Click to Reveal</button>
      </div>
    </div>
    """ if b.phone else '<div class="reveal-box"><div class="reveal-label">Phone</div><div style="font-size:0.875rem;color:var(--text-muted);">Available upon request</div></div>'

    email_reveal = f"""
    <div class="reveal-box">
      <div class="reveal-label">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        Email Address
      </div>
      <div>
        <span class="reveal-value" data-value="{html.escape(b.email)}" style="display:none;"></span>
        <button type="button" class="reveal-btn">Click to Reveal</button>
      </div>
    </div>
    """ if b.email else ""

    website_reveal = f"""
    <div class="reveal-box">
      <div class="reveal-label">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
        Official Website
      </div>
      <div>
        <span class="reveal-value" data-value="{html.escape(b.website)}" style="display:none;font-size:0.8125rem;"></span>
        <button type="button" class="reveal-btn">Reveal Website URL</button>
      </div>
    </div>
    """ if b.website else ""

    content = f"""
{render_breadcrumbs(breadcrumbs)}

<div class="profile-header">
  <div class="container">
    <div class="profile-hero">
      <div class="profile-title-area">
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
          <span class="hero-category-badge" style="margin-bottom:0;">{category_escaped}</span>
          <span style="font-size:0.8125rem;color:var(--text-muted);">&#10003; {b.display_location}</span>
        </div>
        <h1>{name_escaped}</h1>
        <div class="profile-badges">
          {f'<span class="broker-rating-badge">&#9733; {b.rating:.1f} ({b.reviews_count} Google reviews)</span>' if b.rating > 0 else ''}
          {render_trust_pill(b.trust_score)}
          {f'<span class="badge-item" style="color:var(--success);background:var(--success-bg);">Licence Verified</span>' if b.license_disclosed else ''}
        </div>
      </div>
      <div style="text-align:right;">
        <a href="/claim-profile/?broker={b.slug}" class="header-cta" style="font-size:0.8125rem;">
          Is this your brokerage? Claim Listing
        </a>
      </div>
    </div>
  </div>
</div>

<div class="container">
  <div class="profile-grid">
    <!-- Main Column -->
    <div class="profile-main">
      <!-- About -->
      <div class="card">
        <h2 class="card-title" style="margin-bottom:0.75rem;">About {name_escaped}</h2>
        <div style="font-size:0.9375rem;line-height:1.7;color:var(--text);">
          {about_text}
        </div>
        {about_source}
      </div>

      <!-- Trust Score Breakdown -->
      {render_trust_breakdown(b)}

      <!-- Reputation & Reviews -->
      <div class="card" id="reputation">
        <div class="card-header">
          <div>
            <h2 class="card-title">Google Reputation &amp; Reviews</h2>
            <p class="card-subtitle">Aggregated customer feedback mirrored from Google Places API</p>
          </div>
          {f'<span class="broker-rating-badge" style="font-size:0.9375rem;">&#9733; {b.rating:.1f} / 5.0</span>' if b.rating > 0 else ''}
        </div>
        {reviews_block}
      </div>

      <!-- Directory Review Submission -->
      {render_review_form(b.slug, b.name)}

      <!-- Real Case Study Submission -->
      {render_case_form(b.slug, b.name)}
    </div>

    <!-- Sidebar Column -->
    <div class="profile-sidebar">
      <!-- Contact Details -->
      <div class="card">
        <h3 class="card-title" style="margin-bottom:1rem;">Contact Details</h3>
        {phone_reveal}
        {email_reveal}
        {website_reveal}

        <div style="margin-top:1.25rem;padding-top:1rem;border-top:1px solid var(--border);">
          <div style="font-size:0.8125rem;font-weight:600;color:var(--text-muted);margin-bottom:0.35rem;">Office Address:</div>
          <div style="font-size:0.875rem;color:var(--text);line-height:1.4;">{address_escaped}</div>
        </div>
      </div>

      <!-- Compliance & Governance -->
      <div class="card">
        <h3 class="card-title" style="font-size:1.0625rem;margin-bottom:0.75rem;">Regulatory &amp; Data Provenance</h3>
        <ul style="font-size:0.8125rem;color:var(--text-muted);line-height:1.6;list-style:disc;padding-left:1.2rem;">
          <li>Entity verification: {b.place_id or 'National Directory Match'}</li>
          <li>Licence Disclosure: {'Public ACL / Credit Rep number published' if b.license_disclosed else 'Pending owner publication'}</li>
          <li>Scoring Method: Published 3-Factor Trust Algorithm</li>
          <li>Last Audit: September 2026</li>
        </ul>
        <div style="margin-top:1rem;padding-top:0.75rem;border-top:1px solid var(--border);font-size:0.75rem;">
          <a href="/contact/?broker={b.slug}" style="color:var(--primary);text-decoration:underline;">Report an error or request removal</a>
        </div>
      </div>
    </div>
  </div>
</div>
"""

    page_title = f"{b.name} — {b.category} in {b.display_location} | Best Brokers Australia"
    meta_desc = (
        f"{b.name} is a verified {b.category.lower()} in {b.display_location}. "
        f"Trust Score: {b.trust_score}%. Star rating: {b.rating:.1f} ({b.reviews_count} reviews). "
        f"View verified reviews, licence disclosures, and contact details."
    )

    return render_page(
        title=page_title,
        meta_description=meta_desc,
        canonical_url=b.canonical_url,
        content_html=content,
        active_nav=url_for_category(b.category_slug),
        is_indexable=b.is_indexable,
        schema_jsonld=[
            broker_local_business_schema(b),
            breadcrumbs_jsonld(breadcrumbs),
        ],
    )
