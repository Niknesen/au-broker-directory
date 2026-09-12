"""
Centralized Footer component for Best Brokers Australia.
"""
from ..config import SITE_NAME, OPERATOR_NAME, OPERATOR_URL, CONTACT_EMAIL
from ..taxonomy import CATEGORIES, url_for_category


def render_footer() -> str:
    """Renders the single canonical source of truth for the site footer."""
    category_links = "".join(
        f'<li><a href="{url_for_category(info["slug"])}">{info["short_name"]}</a></li>'
        for info in CATEGORIES.values()
    )

    major_city_links = """
      <li><a href="/mortgage-brokers/sydney/">Mortgage Brokers Sydney</a></li>
      <li><a href="/mortgage-brokers/melbourne/">Mortgage Brokers Melbourne</a></li>
      <li><a href="/mortgage-brokers/brisbane/">Mortgage Brokers Brisbane</a></li>
      <li><a href="/mortgage-brokers/perth/">Mortgage Brokers Perth</a></li>
      <li><a href="/mortgage-brokers/adelaide/">Mortgage Brokers Adelaide</a></li>
      <li><a href="/mortgage-brokers/canberra/">Mortgage Brokers Canberra</a></li>
      <li><a href="/mortgage-brokers/gold-coast/">Mortgage Brokers Gold Coast</a></li>
    """

    trust_links = """
      <li><a href="/methodology/">Trust Score Methodology</a></li>
      <li><a href="/editorial-policy/">Editorial & Quality Policy</a></li>
      <li><a href="/review-policy/">Review Moderation Policy</a></li>
      <li><a href="/claim-profile/">Claim & Verify Listing</a></li>
      <li><a href="/about/">About AIEX Engineering</a></li>
      <li><a href="/contact/">Contact & Corrections</a></li>
      <li><a href="/privacy/">Privacy & Terms</a></li>
    """

    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <h3>{SITE_NAME}</h3>
        <p class="footer-desc">
          Australia's independent directory of verified mortgage, finance, insurance, 
          real estate, and commercial brokers. Built for transparency and trust.
        </p>
      </div>
      <div class="footer-col">
        <h4>Broker Sectors</h4>
        <ul class="footer-links">
          {category_links}
        </ul>
      </div>
      <div class="footer-col">
        <h4>Key Metro Hubs</h4>
        <ul class="footer-links">
          {major_city_links}
        </ul>
      </div>
      <div class="footer-col">
        <h4>Trust & Governance</h4>
        <ul class="footer-links">
          {trust_links}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-disclaimer">
        Best Brokers Australia is an independent discovery platform designed and operated by 
        <a href="{OPERATOR_URL}" target="_blank" rel="noopener" style="color:#fff;text-decoration:underline;">{OPERATOR_NAME}</a>. 
        Rankings are determined objectively by our published Trust Score algorithm. We do not accept payment to alter organic rankings or scores.
      </div>
      <div class="footer-copy">
        &copy; {SITE_NAME}. All rights reserved.
      </div>
    </div>
  </div>
</footer>
"""
