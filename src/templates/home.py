"""
Homepage Template for Best Brokers Australia.
"""
from typing import List, Dict
import html
from ..config import SITE_NAME, SITE_TAGLINE, SITE_URL
from ..taxonomy import CATEGORIES, STATES, url_for_category, url_for_city, url_for_home
from ..components.base import render_page
from ..components.broker_card import render_broker_card
from ..seo.schema import organization_schema


def render_homepage(data) -> str:
    """Renders the national directory homepage."""
    # 1. Category cards
    cat_cards_html = []
    for sheet_name, cat in CATEGORIES.items():
        cat_slug = cat["slug"]
        broker_count = len(data.brokers_by_category.get(cat_slug, []))
        url = url_for_category(cat_slug)
        cat_cards_html.append(f"""
        <a class="card" href="{url}" style="transition:all 0.15s ease;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem;">
            <h3 style="font-size:1.125rem;font-weight:700;color:var(--text);">{cat['short_name']}</h3>
            <span class="trust-pill low" style="font-size:0.75rem;">{broker_count:,} Brokers</span>
          </div>
          <p style="font-size:0.875rem;color:var(--text-muted);line-height:1.5;">{cat['description'][:110]}...</p>
          <div style="margin-top:1rem;color:var(--primary);font-size:0.875rem;font-weight:600;">
            Browse {cat['short_name']} &rarr;
          </div>
        </a>
        """)

    # 2. Major metro hubs
    metro_cities = [
        ("Sydney", "NSW", "mortgage-brokers", "sydney"),
        ("Melbourne", "VIC", "mortgage-brokers", "melbourne"),
        ("Brisbane", "QLD", "mortgage-brokers", "brisbane-city"),
        ("Perth", "WA", "mortgage-brokers", "perth"),
        ("Adelaide", "SA", "mortgage-brokers", "adelaide"),
        ("Canberra", "ACT", "mortgage-brokers", "canberra"),
        ("Gold Coast", "QLD", "mortgage-brokers", "southport"),
        ("Newcastle", "NSW", "mortgage-brokers", "newcastle"),
        ("Hobart", "TAS", "mortgage-brokers", "hobart"),
        ("Darwin", "NT", "mortgage-brokers", "darwin-city"),
        ("Sunshine Coast", "QLD", "mortgage-brokers", "maroochydore"),
        ("Geelong", "VIC", "mortgage-brokers", "geelong"),
    ]

    city_chips_html = []
    for c_name, st, cat_slug, c_slug in metro_cities:
        url = url_for_city(cat_slug, c_slug)
        city_chips_html.append(f"""
        <a class="location-chip" href="{url}">
          <span>{c_name}, {st}</span>
          <span class="count">&rarr;</span>
        </a>
        """)

    # 3. Top Featured Brokers (highest trust score + real reviews, capped at 9)
    featured_brokers = [b for b in data.brokers if b.is_indexable and len(b.google_reviews) > 0][:9]
    featured_cards_html = "".join(render_broker_card(b) for b in featured_brokers)

    content = f"""
<div class="hero">
  <div class="dynamic-line-glow" aria-hidden="true"></div>
  <div class="dynamic-line-vertical" aria-hidden="true"></div>
  <div class="dynamic-line-vertical-2" aria-hidden="true"></div>
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="hero-category-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Independent Australian Directory
        </span>
        <h1>{SITE_TAGLINE}</h1>
        <p class="hero-lead">
          Compare {data.total_brokers:,} Australian brokers across 7 industry sectors. 
          Every listing features an independently computed Trust Score, verified client feedback, 
          and direct contact details.
        </p>

        <!-- Instant Search Bar -->
        <div class="search-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" id="site-search" class="search-input" placeholder="Search by broker name, suburb, city or phone..." autocomplete="off">
          <div id="search-results" class="search-results-box"></div>
        </div>

        <div class="hero-stats">
          <div class="hero-stat-item">
            <strong>{data.total_brokers:,}</strong> Verified Entities
          </div>
          <div class="hero-stat-item">
            <strong>7</strong> Sectors
          </div>
          <div class="hero-stat-item">
            <strong>100%</strong> Independent
          </div>
          <div class="hero-stat-item">
            <strong>Zero</strong> Pay-to-Rank
          </div>
        </div>
      </div>

      <div class="hero-image-card">
        <img src="/assets/broker-portrait.png" alt="Verified Australian Broker Specialist" class="hero-portrait-img" loading="eager" width="380" height="440">
        <div class="hero-image-badge">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <div>
            <strong>Independent Trust Scoring</strong>
            <span>Verified Australian Industry Profiles</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">Explore by Industry Sector</h2>
        <p class="section-subtitle">Find accredited specialists in lending, risk, property, and commercial transactions</p>
      </div>
    </div>
    <div class="category-grid">
      {''.join(cat_cards_html)}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">Key Metro Hubs</h2>
        <p class="section-subtitle">Browse verified local specialists in major Australian cities</p>
      </div>
    </div>
    <div class="location-chips">
      {''.join(city_chips_html)}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div>
        <h2 class="section-title">Highest Rated Verified Brokers</h2>
        <p class="section-subtitle">Ranked by our transparent Trust Score (Google rating + review volume + licence disclosure)</p>
      </div>
      <a href="/mortgage-brokers/" style="color:var(--primary);font-weight:600;font-size:0.9375rem;">View All Brokers &rarr;</a>
    </div>
    <div class="broker-grid">
      {featured_cards_html}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:860px;text-align:center;">
    <h2 class="section-title" style="margin-bottom:1rem;">How Best Brokers Australia Works</h2>
    <p style="color:var(--text-muted);line-height:1.7;font-size:1.0625rem;margin-bottom:2rem;">
      We built Best Brokers Australia to solve the lack of transparency in financial directory listings. 
      Traditional directories allow businesses to pay for top placement. Our rankings are purely algorithmic, 
      grounded in real Google reputation data and public regulatory filings.
    </p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem;text-align:left;">
      <div class="card">
        <h4 style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.5rem;">1. Real Google Reviews</h4>
        <p style="font-size:0.875rem;color:var(--text-muted);line-height:1.5;">We pull aggregate star ratings and review text directly from Google Place IDs, preventing review fraud.</p>
      </div>
      <div class="card">
        <h4 style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.5rem;">2. Licence Verification</h4>
        <p style="font-size:0.875rem;color:var(--text-muted);line-height:1.5;">We check if brokers disclose their Australian Credit Licence (ACL) or Credit Representative numbers.</p>
      </div>
      <div class="card">
        <h4 style="font-size:1rem;font-weight:700;color:var(--text);margin-bottom:0.5rem;">3. Direct Contact Reveal</h4>
        <p style="font-size:0.875rem;color:var(--text-muted);line-height:1.5;">Contact verified brokers directly via phone, email, or website without middleman lead markups.</p>
      </div>
    </div>
  </div>
</section>

<script>
// Live Search Handler on Homepage
(function() {{
  var searchInput = document.getElementById('site-search');
  var resultsBox = document.getElementById('search-results');
  if (!searchInput || !resultsBox) return;

  var indexData = null;

  function loadIndex() {{
    if (indexData) return Promise.resolve(indexData);
    return fetch('/data.json')
      .then(function(r) {{ return r.json(); }})
      .then(function(d) {{ indexData = d; return d; }});
  }}

  searchInput.addEventListener('input', function(e) {{
    var q = e.target.value.trim().toLowerCase();
    if (!q || q.length < 2) {{
      resultsBox.style.display = 'none';
      resultsBox.innerHTML = '';
      return;
    }}

    loadIndex().then(function(data) {{
      var matches = data.filter(function(b) {{
        return (b.name || '').toLowerCase().indexOf(q) !== -1 ||
               (b.city || '').toLowerCase().indexOf(q) !== -1 ||
               (b.suburb || '').toLowerCase().indexOf(q) !== -1 ||
               (b.phone || '').replace(/\\s/g,'').indexOf(q.replace(/\\s/g,'')) !== -1;
      }}).slice(0, 9);

      if (matches.length === 0) {{
        resultsBox.innerHTML = '<div style="padding:1rem;color:var(--text-muted);font-size:0.875rem;">No brokers found matching "' + q + '".</div>';
        resultsBox.style.display = 'block';
        return;
      }}

      resultsBox.innerHTML = matches.map(function(b) {{
        var loc = [b.suburb || b.city, b.state].filter(Boolean).join(', ');
        return '<a class="search-result-item" href="/broker/' + b.slug + '/">' +
                 '<div>' +
                   '<div style="font-weight:600;font-size:0.9375rem;color:var(--text);">' + b.name + '</div>' +
                   '<div style="font-size:0.8125rem;color:var(--text-muted);">' + b.category + ' &middot; ' + loc + '</div>' +
                 '</div>' +
                 '<span class="trust-pill ' + (b.score >= 85 ? 'high' : b.score >= 70 ? 'mid' : 'low') + '">' + b.score + '%</span>' +
               '</a>';
      }}).join('');
      resultsBox.style.display = 'block';
    }});
  }});

  document.addEventListener('click', function(e) {{
    if (!searchInput.contains(e.target) && !resultsBox.contains(e.target)) {{
      resultsBox.style.display = 'none';
    }}
  }});
}})();
</script>
"""

    return render_page(
        title=f"{SITE_NAME} — {SITE_TAGLINE}",
        meta_description=f"Compare {data.total_brokers:,} verified Australian brokers across mortgage, insurance, real estate, and finance. Independent trust scores and real Google reviews.",
        canonical_url=f"{SITE_URL}/",
        content_html=content,
        active_nav="/",
        is_indexable=True,
        schema_jsonld=[organization_schema()],
    )
