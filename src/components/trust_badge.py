"""
Trust Score badge and visual circular indicators for Best Brokers Australia.
Renders SVG circular progress rings with color-coded score tiers.
"""

def get_tier_color(score: int) -> dict:
    """Returns color definitions based on score tier."""
    if score >= 80:
        return {
            "stroke": "#16a34a",
            "bg": "#dcfce7",
            "text": "#16a34a",
            "label": "High Trust",
            "tier": "high",
        }
    elif score >= 70:
        return {
            "stroke": "#d97706",
            "bg": "#fef3c7",
            "text": "#b45309",
            "label": "Verified Trust",
            "tier": "mid",
        }
    else:
        return {
            "stroke": "#dc2626",
            "bg": "#fee2e2",
            "text": "#dc2626",
            "label": "Standard",
            "tier": "low",
        }


def render_trust_circle(score: int, size: int = 44) -> str:
    """
    Renders a compact circular SVG progress ring for broker cards and lists.
    """
    tier = get_tier_color(score)
    r = (size - 6) / 2
    cx = size / 2
    cy = size / 2
    c = 2 * 3.14159265 * r
    offset = c * (1.0 - (score / 100.0))

    return f"""
<div class="trust-circle-wrap" title="Trust Score: {score}% ({tier['label']})">
  <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" class="trust-circle-svg">
    <!-- Track -->
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e2e8f0" stroke-width="3.5" />
    <!-- Progress Arc -->
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{tier['stroke']}" stroke-width="3.5"
            stroke-dasharray="{c:.1f}" stroke-dashoffset="{offset:.1f}"
            stroke-linecap="round"
            transform="rotate(-90 {cx} {cy})" />
    <!-- Center Text -->
    <text x="{cx}" y="{cy + 4}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="{tier['text']}">{score}%</text>
  </svg>
  <span class="trust-circle-label" style="color:{tier['text']};">{tier['label']}</span>
</div>
"""


def render_trust_pill(score: int) -> str:
    """Renders a color-coded trust score pill with circular indicator."""
    return render_trust_circle(score, size=40)


def render_trust_breakdown(broker) -> str:
    """Renders the transparent 3-factor score breakdown with a large circular gauge for broker profile."""
    score = broker.trust_score
    tier = get_tier_color(score)
    rating_val = broker.rating or 0.0
    review_cnt = broker.reviews_count or 0
    licence_ok = broker.license_disclosed

    # 90px Large Gauge
    size = 90
    r = 38
    cx = 45
    cy = 45
    c = 2 * 3.14159265 * r
    offset = c * (1.0 - (score / 100.0))

    gauge_svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="flex-shrink:0;">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e2e8f0" stroke-width="6" />
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{tier['stroke']}" stroke-width="6"
              stroke-dasharray="{c:.1f}" stroke-dashoffset="{offset:.1f}"
              stroke-linecap="round"
              transform="rotate(-90 {cx} {cy})" />
      <text x="{cx}" y="{cy + 7}" text-anchor="middle" font-family="'Space Grotesk', -apple-system, sans-serif" font-size="22" font-weight="700" fill="{tier['text']}">{score}%</text>
    </svg>
    """

    return f"""
<div class="card" id="trust-score-breakdown">
  <div class="card-header" style="display:flex;align-items:center;gap:1.5rem;">
    {gauge_svg}
    <div>
      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
        <h2 class="card-title" style="margin-bottom:0;">Independent Trust Score</h2>
        <span class="trust-pill {tier['tier']}" style="padding:0.2rem 0.6rem;font-size:0.75rem;">{tier['label']}</span>
      </div>
      <p class="card-subtitle">Transparent 3-factor algorithm based on publicly verifiable data points</p>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-top:1.25rem;">
    <div style="background:var(--bg-subtle);padding:1rem;border-radius:var(--radius-md);border:1px solid var(--border);">
      <div style="font-size:0.8125rem;color:var(--text-muted);font-weight:600;">Google Rating (50%)</div>
      <div style="font-size:1.25rem;font-weight:700;margin-top:0.25rem;color:var(--text);">&#9733; {rating_val:.1f} / 5.0</div>
      <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.25rem;">Aggregate customer satisfaction</div>
    </div>
    <div style="background:var(--bg-subtle);padding:1rem;border-radius:var(--radius-md);border:1px solid var(--border);">
      <div style="font-size:0.8125rem;color:var(--text-muted);font-weight:600;">Review Volume (30%)</div>
      <div style="font-size:1.25rem;font-weight:700;margin-top:0.25rem;color:var(--text);">{review_cnt:,} Reviews</div>
      <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.25rem;">Statistical proof of market activity</div>
    </div>
    <div style="background:var(--bg-subtle);padding:1rem;border-radius:var(--radius-md);border:1px solid var(--border);">
      <div style="font-size:0.8125rem;color:var(--text-muted);font-weight:600;">Licence Disclosure (20%)</div>
      <div style="font-size:1.25rem;font-weight:700;margin-top:0.25rem;color:{'var(--success)' if licence_ok else 'var(--text-muted)'};">
        {'Disclosed' if licence_ok else 'Not Published'}
      </div>
      <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.25rem;">
        {'Public ACL / Credit Rep verified' if licence_ok else 'No licence number on website'}
      </div>
    </div>
  </div>
</div>
"""
