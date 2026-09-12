"""
Trust Score badge and visual indicators for Best Brokers Australia.
"""

def render_trust_pill(score: int) -> str:
    """Renders a color-coded trust score pill."""
    if score >= 85:
        tier_class = "high"
        label = "High Trust"
    elif score >= 70:
        tier_class = "mid"
        label = "Verified Trust"
    else:
        tier_class = "low"
        label = "Standard"

    return f'<span class="trust-pill {tier_class}" title="Computed Trust Score: {score}% ({label})">{score}% Trust Score</span>'


def render_trust_breakdown(broker) -> str:
    """Renders the transparent 3-factor score breakdown for broker profile."""
    rating_val = broker.rating or 0.0
    review_cnt = broker.reviews_count or 0
    licence_ok = broker.license_disclosed

    return f"""
<div class="card" id="trust-score-breakdown">
  <div class="card-header">
    <div>
      <h2 class="card-title">Independent Trust Score: {broker.trust_score}%</h2>
      <p class="card-subtitle">Transparent algorithm based on publicly verifiable data points</p>
    </div>
    {render_trust_pill(broker.trust_score)}
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-top:1rem;">
    <div style="background:var(--bg-subtle);padding:1rem;border-radius:var(--radius-md);border:1px solid var(--border);">
      <div style="font-size:0.8125rem;color:var(--text-muted);font-weight:600;">Google Rating (50%)</div>
      <div style="font-size:1.25rem;font-weight:700;margin-top:0.25rem;color:var(--text);">&#9733; {rating_val:.1f} / 5.0</div>
      <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.25rem;">Based on aggregate customer satisfaction</div>
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
