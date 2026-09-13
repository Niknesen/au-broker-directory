"""
City Hub Template for Best Brokers Australia.
Implements Blueprint Section 5.1 (City/category hub) — Top 9 verified specialists,
SEO Scenario Matcher Matrix, Interactive Repayment Estimator, and PAA FAQ Schema.
"""
import html
from ..config import SITE_NAME, SITE_URL
from ..components.base import render_page
from ..components.breadcrumbs import render_breadcrumbs, breadcrumbs_jsonld
from ..components.broker_card import render_broker_card
from ..seo.schema import hub_collection_schema


def render_city_page(hub, page: int = 1) -> str:
    """Renders a city category hub page with local top 9 broker cards, Scenario Matrix, Repayment Estimator, and nearby navigation."""
    total_brokers = len(hub.brokers)
    page_brokers = hub.brokers[:9]
    top_broker = page_brokers[0] if page_brokers else None

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
  <div class="dynamic-line-glow" aria-hidden="true"></div>
  <div class="dynamic-line-vertical" aria-hidden="true"></div>
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
        100% <strong>Free Borrower Service (BID)</strong>
      </div>
      <div class="hero-stat-item">
        Updated: <strong>September 2026</strong>
      </div>
    </div>
  </div>
</div>

<!-- SEO Feature 1: Lending Scenario Matcher Matrix -->
<section class="section" style="padding-top:2rem; padding-bottom:1rem;">
  <div class="container">
    <div class="scenario-section">
      <h2 class="scenario-title">{hub.city_name} Client Scenario Guide (2026 Matcher)</h2>
      <p class="scenario-subtitle">Compare key local lending parameters and broker specializations for {hub.city_name} residents:</p>
      <div class="scenario-table-wrap">
        <table class="scenario-table">
          <thead>
            <tr>
              <th>Borrowing Scenario</th>
              <th>Key {hub.state_code} Market Considerations</th>
              <th>Typical Lender Panel</th>
              <th>Top Suited Provider</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>First Home Buyer</strong></td>
              <td>{hub.state_code} Stamp Duty exemptions & Federal 5% Home Guarantee</td>
              <td><span class="scenario-badge">CBA, NAB, St George</span></td>
              <td><a href="#{top_broker.slug if top_broker else 'featured'}">{top_broker.name if top_broker else 'Top Rated Specialist'}</a></td>
            </tr>
            <tr>
              <td><strong>Refinancing & Equity</strong></td>
              <td>Discretionary rate discounts (0.20%-0.45% under branch rates)</td>
              <td><span class="scenario-badge">Macquarie, ANZ, Bankwest</span></td>
              <td><a href="#featured">Featured Local Specialist</a></td>
            </tr>
            <tr>
              <td><strong>Self-Employed / Low-Doc</strong></td>
              <td>12-month BAS statements, alt-doc income verification</td>
              <td><span class="scenario-badge">Pepper, Liberty, Resimac</span></td>
              <td><a href="#featured">Commercial & Alt-Doc Specialist</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<!-- SEO Feature 2: Interactive Repayment Calculator Slider -->
<section class="section" style="padding-top:0; padding-bottom:1.5rem;">
  <div class="container">
    <div class="calc-widget">
      <div>
        <h3 class="calc-title">Quick Loan Repayment Estimator</h3>
        <p class="calc-desc">Calculate estimated monthly repayments for {hub.city_name} properties based on current market rates:</p>
        <div class="calc-inputs">
          <div class="calc-row">
            <span>Loan Amount: <strong id="loan-display">$750,000</strong></span>
            <input type="range" class="calc-slider" id="loan-slider" min="200000" max="3000000" step="25000" value="750000" oninput="updateCityRepayment()">
          </div>
          <div class="calc-row">
            <span>Interest Rate: <strong id="rate-display">5.99%</strong></span>
            <input type="range" class="calc-slider" id="rate-slider" min="4.5" max="9.0" step="0.1" value="5.99" oninput="updateCityRepayment()">
          </div>
        </div>
      </div>
      <div class="calc-result-box">
        <div class="calc-result-lbl">Estimated Monthly Repayment</div>
        <div class="calc-result-val" id="repayment-display">$4,493</div>
        <div class="calc-result-lbl" style="margin-top:0.35rem;">30-year Principal & Interest</div>
      </div>
    </div>
  </div>
</section>

<!-- Top 9 Broker Cards -->
<section class="section" id="featured" style="padding-top:0;">
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

{f'''
<section class="section section-alt" style="padding:2rem 0;">
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

<!-- PAA FAQs -->
<section class="section section-alt">
  <div class="container" style="max-width:840px;">
    <h2 class="section-title" style="margin-bottom:1.5rem;">{hub.city_name} Selection &amp; Advisory FAQs</h2>
    <div class="card" style="padding:0.5rem 1.75rem;">
      {faqs_html}
    </div>
  </div>
</section>

<script>
function updateCityRepayment() {{
  const P = parseFloat(document.getElementById('loan-slider').value);
  const annualRate = parseFloat(document.getElementById('rate-slider').value);
  document.getElementById('loan-display').innerText = '$' + P.toLocaleString();
  document.getElementById('rate-display').innerText = annualRate.toFixed(2) + '%';
  const r = (annualRate / 100) / 12;
  const n = 30 * 12;
  const M = P * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
  document.getElementById('repayment-display').innerText = '$' + Math.round(M).toLocaleString();
}}
</script>
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
