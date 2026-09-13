"""
Trust, Governance, and Editorial Pages for Best Brokers Australia.
Implements Blueprint Section 7 (Trust, editorial and compliance) and Section 15.
"""
from ..config import SITE_NAME, SITE_URL, OPERATOR_NAME, OPERATOR_URL, CONTACT_EMAIL
from ..components.base import render_page
from ..components.breadcrumbs import render_breadcrumbs, breadcrumbs_jsonld


def render_about_page() -> str:
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "About", "url": "/about/"},
    ]
    content = f"""
{render_breadcrumbs(breadcrumbs)}
<div class="hero">
  <div class="container">
    <span class="hero-category-badge">About Best Brokers Australia</span>
    <h1>Independent Directory Engineering</h1>
    <p class="hero-lead">
      Best Brokers Australia is an independent discovery platform designed and operated by 
      the AIEX Forward Deployed Engineering team.
    </p>
  </div>
</div>

<section class="section">
  <div class="container" style="max-width:840px;">
    <div class="card" style="line-height:1.7;font-size:1rem;color:var(--text);">
      <h2 style="font-size:1.375rem;margin-bottom:1rem;color:var(--text);">Our Purpose</h2>
      <p style="margin-bottom:1.25rem;">
        Navigating the Australian financial and property advisory landscape is notoriously opaque. 
        Traditional directory websites operate on "pay-to-play" models where the highest paying broker 
        gets the top badge, regardless of track record or customer satisfaction.
      </p>
      <p style="margin-bottom:1.25rem;">
        Best Brokers Australia was built to provide an objective, algorithmically ranked index of Australian brokers. 
        We index over 16,000 businesses across seven regulated sectors: Mortgage &amp; Finance, Insurance, Real Estate, 
        Business Sales, Asset Finance, Customs &amp; Freight, and Wealth Advisers.
      </p>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;color:var(--text);">Who Operates the Site</h2>
      <p style="margin-bottom:1.25rem;">
        Best Brokers Australia is engineered by <a href="{OPERATOR_URL}" target="_blank" rel="noopener" style="color:var(--primary);text-decoration:underline;">{OPERATOR_NAME}</a> — 
        the applied engineering group at AIEX that builds production data systems and automation tools.
      </p>
      <p style="margin-bottom:1.25rem;">
        We do not offer credit activities, insurance advice, or financial planning directly. Our role is strictly 
        as an independent technology publisher providing clean data, transparent trust scoring, and direct contact access.
      </p>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;color:var(--text);">Core Commitments</h2>
      <ul style="list-style:disc;padding-left:1.5rem;margin-bottom:1.5rem;">
        <li><strong>Zero Pay-to-Rank:</strong> No business can pay to boost their Trust Score or jump organic ranking.</li>
        <li><strong>Real Customer Reviews:</strong> We mirror actual Google Maps Place reviews rather than hosting fake testimonial widgets.</li>
        <li><strong>Direct Access:</strong> We provide real contact information without forcing users through lead capture funnels.</li>
        <li><strong>Fast Corrections:</strong> Any broker can request an update or removal with a 24-48h turnaround SLA.</li>
      </ul>
    </div>
  </div>
</section>
"""
    return render_page(
        title="About Us | Best Brokers Australia",
        meta_description="Learn about Best Brokers Australia, our mission, our engineering team at AIEX, and our commitment to independent directory publishing.",
        canonical_url=f"{SITE_URL}/about/",
        content_html=content,
        active_nav="/about/",
        is_indexable=True,
        schema_jsonld=[breadcrumbs_jsonld(breadcrumbs)],
    )


def render_methodology_page() -> str:
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Trust Score Methodology", "url": "/methodology/"},
    ]
    content = f"""
{render_breadcrumbs(breadcrumbs)}
<div class="hero">
  <div class="container">
    <span class="hero-category-badge">Transparent Scoring Engine</span>
    <h1>Trust Score Methodology</h1>
    <p class="hero-lead">
      How we calculate objective Trust Scores for over 16,000 Australian brokers without commercial bias.
    </p>
  </div>
</div>

<section class="section">
  <div class="container" style="max-width:840px;">
    <div class="card" style="line-height:1.7;font-size:1rem;color:var(--text);">
      <h2 style="font-size:1.375rem;margin-bottom:1rem;color:var(--text);">The 3-Factor Formula</h2>
      <p style="margin-bottom:1.25rem;">
        Every broker on Best Brokers Australia receives an algorithmic score between 10% and 99%. 
        The score is derived entirely from public, verifiable data points across three core pillars:
      </p>

      <div style="display:grid;grid-template-columns:1fr;gap:1.5rem;margin:1.5rem 0;">
        <div style="background:var(--bg-subtle);padding:1.25rem;border-radius:var(--radius-md);border:1px solid var(--border);">
          <h3 style="font-size:1.125rem;font-weight:700;color:var(--primary);margin-bottom:0.35rem;">1. Google Place Rating (50% Weight)</h3>
          <p style="font-size:0.9375rem;color:var(--text-muted);">
            Derived from verified Google Maps review ratings. A 5.0/5.0 rating awards the maximum 50 points, 
            scaled proportionally down to 1.0/5.0. Businesses without public ratings receive a baseline score.
          </p>
        </div>

        <div style="background:var(--bg-subtle);padding:1.25rem;border-radius:var(--radius-md);border:1px solid var(--border);">
          <h3 style="font-size:1.125rem;font-weight:700;color:var(--primary);margin-bottom:0.35rem;">2. Review Volume &amp; Statistical Proof (30% Weight)</h3>
          <p style="font-size:0.9375rem;color:var(--text-muted);">
            A high rating is only statistically significant with sufficient volume. We award tiered points: 
            100+ reviews = 30 pts, 50+ reviews = 25 pts, 20+ reviews = 20 pts, 10+ reviews = 15 pts, 1+ reviews = 10 pts.
          </p>
        </div>

        <div style="background:var(--bg-subtle);padding:1.25rem;border-radius:var(--radius-md);border:1px solid var(--border);">
          <h3 style="font-size:1.125rem;font-weight:700;color:var(--primary);margin-bottom:0.35rem;">3. Public Licence &amp; Regulatory Disclosure (20% Weight)</h3>
          <p style="font-size:0.9375rem;color:var(--text-muted);">
            Australian financial legislation requires brokers to disclose their Australian Credit Licence (ACL) 
            or Authorised Credit Representative number. If a broker discloses this on their website, they receive 20 points.
          </p>
        </div>
      </div>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;color:var(--text);">Score Tiers &amp; Badges</h2>
      <ul style="list-style:disc;padding-left:1.5rem;margin-bottom:1.5rem;">
        <li><strong>High Trust (85% – 99%):</strong> Top-tier specialists with extensive verified review history (50+ reviews) and published regulatory disclosures.</li>
        <li><strong>Verified Trust (70% – 84%):</strong> Reliable operators with consistent positive feedback and verified business entity status.</li>
        <li><strong>Standard Listing (10% – 69%):</strong> Businesses with fewer public reviews or unverified web disclosures. Fully eligible for score upgrades upon submission of licence evidence.</li>
      </ul>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;color:var(--text);">Updating Your Score</h2>
      <p>
        If your brokerage has updated its website, added licence disclosures, or gained more customer reviews, 
        use our <a href="/claim-profile/" style="color:var(--primary);text-decoration:underline;">Claim Profile form</a> 
        to trigger an automated re-scan and score re-calculation.
      </p>
    </div>
  </div>
</section>
"""
    return render_page(
        title="Trust Score Methodology | Best Brokers Australia",
        meta_description="Read the complete scoring methodology behind Best Brokers Australia. Learn how Google ratings, review volume, and licence disclosures determine Trust Scores.",
        canonical_url=f"{SITE_URL}/methodology/",
        content_html=content,
        active_nav="/methodology/",
        is_indexable=True,
        schema_jsonld=[breadcrumbs_jsonld(breadcrumbs)],
    )


def render_editorial_policy_page() -> str:
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Editorial Policy", "url": "/editorial-policy/"},
    ]
    content = f"""
{render_breadcrumbs(breadcrumbs)}
<div class="hero">
  <div class="container">
    <span class="hero-category-badge">Standards &amp; Governance</span>
    <h1>Editorial &amp; Quality Policy</h1>
    <p class="hero-lead">Our standards for listing curation, ranking independence, and data integrity.</p>
  </div>
</div>
<section class="section">
  <div class="container" style="max-width:840px;">
    <div class="card" style="line-height:1.7;font-size:1rem;color:var(--text);">
      <h2 style="font-size:1.375rem;margin-bottom:1rem;">1. Absolute Commercial Independence</h2>
      <p style="margin-bottom:1.25rem;">
        Best Brokers Australia does not sell directory rank. Advertisers cannot purchase higher positioning, 
        manipulate Trust Scores, or suppress negative customer feedback. All directory orderings are programmatic.
      </p>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;">2. Data Ingestion &amp; Verification</h2>
      <p style="margin-bottom:1.25rem;">
        We curate listings from public registry sources, Google Places data, and business-owner submissions. 
        Each record is validated for active trading status, working phone numbers, and physical Australian office locations.
      </p>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;">3. Indexation Quality Gate</h2>
      <p style="margin-bottom:1.25rem;">
        To prevent thin or low-value pages in search results, only profiles with substantial verified data 
        (verified identity, complete NAP, review evidence, or licence proof) are permitted into search engine indexes. 
        All other records remain fully searchable by consumers on our platform.
      </p>
    </div>
  </div>
</section>
"""
    return render_page(
        title="Editorial Policy | Best Brokers Australia",
        meta_description="Our editorial policy details how Best Brokers Australia curates listings, verifies data, and enforces strict commercial independence.",
        canonical_url=f"{SITE_URL}/editorial-policy/",
        content_html=content,
        active_nav="/editorial-policy/",
        is_indexable=True,
        schema_jsonld=[breadcrumbs_jsonld(breadcrumbs)],
    )


def render_review_policy_page() -> str:
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Review Policy", "url": "/review-policy/"},
    ]
    content = f"""
{render_breadcrumbs(breadcrumbs)}
<div class="hero">
  <div class="container">
    <span class="hero-category-badge">Review Governance</span>
    <h1>Review &amp; Moderation Policy</h1>
    <p class="hero-lead">How third-party Google reviews and directory-native reviews are verified and moderated.</p>
  </div>
</div>
<section class="section">
  <div class="container" style="max-width:840px;">
    <div class="card" style="line-height:1.7;font-size:1rem;color:var(--text);">
      <h2 style="font-size:1.375rem;margin-bottom:1rem;">Third-Party Google Reviews</h2>
      <p style="margin-bottom:1.25rem;">
        Review counts and ratings displayed on broker profiles are synchronized directly from Google Place IDs. 
        We attribute these clearly as third-party reviews. We do not edit, rewrite, or filter Google review texts.
      </p>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;">First-Party Directory Submissions</h2>
      <p style="margin-bottom:1.25rem;">
        Reviews and real transaction cases submitted directly via our web forms undergo moderation before publication. 
        We require a valid email address and a client certification that the review stems from an actual commercial transaction.
      </p>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;">Disputes &amp; Fake Review Removal</h2>
      <p>
        If you are a broker and believe a first-party review is fraudulent, defamatory, or from a competitor, 
        contact <a href="mailto:{CONTACT_EMAIL}" style="color:var(--primary);text-decoration:underline;">{CONTACT_EMAIL}</a> 
        with your evidence. Our trust &amp; safety team reviews all dispute requests within 48 hours.
      </p>
    </div>
  </div>
</section>
"""
    return render_page(
        title="Review Policy | Best Brokers Australia",
        meta_description="Review moderation and authenticity policy for Best Brokers Australia. How we handle Google ratings, first-party reviews, and dispute resolutions.",
        canonical_url=f"{SITE_URL}/review-policy/",
        content_html=content,
        active_nav="/review-policy/",
        is_indexable=True,
        schema_jsonld=[breadcrumbs_jsonld(breadcrumbs)],
    )


def render_claim_page() -> str:
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Claim Listing", "url": "/claim-profile/"},
    ]
    content = f"""
{render_breadcrumbs(breadcrumbs)}
<div class="hero">
  <div class="container">
    <span class="hero-category-badge">Broker Verification</span>
    <h1>Claim &amp; Verify Your Profile</h1>
    <p class="hero-lead">Verify your brokerage profile to unlock custom descriptions, team photos, case studies, and score boosts.</p>
  </div>
</div>

<section class="section">
  <div class="container" style="max-width:840px;">
    <div class="card" style="margin-bottom:2rem;">
      <h2 style="font-size:1.25rem;margin-bottom:1rem;">Why Claim Your Profile?</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;font-size:0.9375rem;">
        <div><strong>&#10003; Boost Trust Score:</strong> Add your Australian Credit Licence (ACL) / Credit Rep number for an instant +20 pt boost.</div>
        <div><strong>&#10003; Custom Overview:</strong> Provide an authoritative description of your lending specialties and lender panel.</div>
        <div><strong>&#10003; Direct Client Inquiries:</strong> Ensure your phone number, email, and booking links are 100% accurate.</div>
      </div>
    </div>

    <div class="card">
      <h2 style="font-size:1.375rem;margin-bottom:1rem;">Claim Submission Form</h2>
      <form class="ajax-form" data-endpoint="/api/cases">
        <input type="hidden" name="role" value="broker">
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
          <div>
            <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;">Brokerage Business Name *</label>
            <input type="text" name="name" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="e.g. Acme Finance Pty Ltd">
          </div>
          <div>
            <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;">Contact Name &amp; Title *</label>
            <input type="text" name="contact_name" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="e.g. John Doe, Managing Director">
          </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
          <div>
            <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;">Work Email Address * (Matching your domain)</label>
            <input type="email" name="email" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="john@acmefinance.com.au">
          </div>
          <div>
            <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;">Phone Number *</label>
            <input type="tel" name="phone" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="1300 000 000">
          </div>
        </div>

        <div style="margin-bottom:1rem;">
          <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;">Current Best Brokers Australia Profile URL or Broker Slug</label>
          <input type="text" name="broker_slug" class="search-input" style="padding:0.6rem 0.85rem;" placeholder="https://bestbrokersaustralia.org/broker/your-slug/ or your-slug">
        </div>

        <div style="margin-bottom:1rem;">
          <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;">Licence &amp; Verification Details *</label>
          <textarea name="text" rows="4" required class="search-input" style="padding:0.75rem 0.85rem;min-height:100px;" placeholder="Provide your Australian Credit Licence (ACL) number or Credit Representative (CR) number, and any requested updates to your profile..."></textarea>
        </div>

        <div style="margin-bottom:1.25rem;">
          <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">
            📎 Verification Document / Licence Certificate (Optional &mdash; Max 10MB)
          </label>
          <div style="border:1px dashed var(--border);border-radius:var(--radius-md);padding:0.85rem 1rem;background:var(--bg-subtle);">
            <input type="file" name="attachment" accept="image/*,.pdf,.doc,.docx" style="font-size:0.8125rem;cursor:pointer;width:100%;">
            <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.35rem;">
              Upload ACL certificate, company letterhead, or ID verification (PDF, PNG, JPG up to 10MB)
            </div>
          </div>
        </div>

        <button type="submit" class="header-cta" style="border:none;cursor:pointer;padding:0.75rem 1.5rem;font-size:0.9375rem;">
          Submit Verification Request &rarr;
        </button>
        <div class="form-feedback" style="display:none;margin-top:1rem;padding:0.75rem;border-radius:var(--radius-md);"></div>
      </form>
    </div>
  </div>
</section>
"""
    return render_page(
        title="Claim & Verify Your Listing | Best Brokers Australia",
        meta_description="Are you a licensed Australian broker? Claim and verify your directory listing on Best Brokers Australia to manage your profile, add licence details, and boost your Trust Score.",
        canonical_url=f"{SITE_URL}/claim-profile/",
        content_html=content,
        active_nav="/claim-profile/",
        is_indexable=True,
        schema_jsonld=[breadcrumbs_jsonld(breadcrumbs)],
    )


def render_contact_page() -> str:
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Contact & Corrections", "url": "/contact/"},
    ]
    content = f"""
{render_breadcrumbs(breadcrumbs)}
<div class="hero">
  <div class="container">
    <span class="hero-category-badge">Support &amp; Inquiries</span>
    <h1>Contact &amp; Corrections</h1>
    <p class="hero-lead">Get in touch with our directory engineering team for general inquiries, corrections, or listing removal requests.</p>
  </div>
</div>

<section class="section">
  <div class="container" style="max-width:840px;">
    <div class="card" style="line-height:1.7;font-size:1rem;color:var(--text);">
      <h2 style="font-size:1.375rem;margin-bottom:1rem;">Direct Contact</h2>
      <p style="margin-bottom:1rem;">
        For general questions, technical inquiries, or partnership discussions, reach out directly via email:
      </p>
      <div style="background:var(--bg-subtle);padding:1rem;border-radius:var(--radius-md);margin-bottom:1.5rem;font-weight:600;color:var(--primary);font-size:1.125rem;">
        Email: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
      </div>

      <h2 style="font-size:1.375rem;margin-top:2rem;margin-bottom:1rem;">Data Corrections &amp; Removal Requests</h2>
      <p style="margin-bottom:1rem;">
        We take data accuracy and business privacy seriously. If your business profile contains outdated contact details, 
        an inaccurate address, or if you would like your listing removed from our directory:
      </p>
      <ol style="padding-left:1.5rem;margin-bottom:1.5rem;line-height:1.6;">
        <li>Email <strong>{CONTACT_EMAIL}</strong> with the subject line <em>"Directory Correction: [Business Name]"</em>.</li>
        <li>Include the direct URL to your profile on our platform.</li>
        <li>State the exact correction or state that you request full removal.</li>
      </ol>
      <p style="font-size:0.875rem;color:var(--text-muted);">
        <strong>Response SLA:</strong> All correction and removal requests are processed within 24 to 48 business hours.
      </p>
    </div>
  </div>
</section>
"""
    return render_page(
        title="Contact Us & Data Corrections | Best Brokers Australia",
        meta_description="Contact the Best Brokers Australia directory engineering team. Submit data corrections, profile updates, or listing removal requests.",
        canonical_url=f"{SITE_URL}/contact/",
        content_html=content,
        active_nav="/contact/",
        is_indexable=True,
        schema_jsonld=[breadcrumbs_jsonld(breadcrumbs)],
    )


def render_privacy_page() -> str:
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Privacy Policy", "url": "/privacy/"},
    ]
    content = f"""
{render_breadcrumbs(breadcrumbs)}
<div class="hero">
  <div class="container">
    <span class="hero-category-badge">Legal &amp; Compliance</span>
    <h1>Privacy Policy &amp; Terms</h1>
    <p class="hero-lead">How Best Brokers Australia collects, manages, and protects business and personal information under Australian Privacy Laws.</p>
  </div>
</div>

<section class="section">
  <div class="container" style="max-width:840px;">
    <div class="card" style="line-height:1.7;font-size:1rem;color:var(--text);">
      <h2 style="font-size:1.25rem;margin-bottom:0.75rem;">1. Compliance with the Privacy Act 1988 (Cth)</h2>
      <p style="margin-bottom:1.25rem;">
        Best Brokers Australia is committed to protecting your privacy in accordance with the Australian Privacy Principles (APPs) 
        contained in the Privacy Act 1988 (Cth).
      </p>

      <h2 style="font-size:1.25rem;margin-top:1.5rem;margin-bottom:0.75rem;">2. Information We Collect</h2>
      <p style="margin-bottom:1.25rem;">
        We collect business entity details (business name, public office address, published telephone numbers, website URLs, 
        and public regulatory licence disclosures) from public registries and official business websites. 
        When users submit reviews or claims, we collect their name and email address solely for verification and communication.
      </p>

      <h2 style="font-size:1.25rem;margin-top:1.5rem;margin-bottom:0.75rem;">3. Use of Information</h2>
      <p style="margin-bottom:1.25rem;">
        Business information is published in our directory to help consumers discover accredited broker services. 
        We do not sell user personal data or email addresses to third-party marketing brokers.
      </p>

      <h2 style="font-size:1.25rem;margin-top:1.5rem;margin-bottom:0.75rem;">4. Access, Correction, and Deletion Rights</h2>
      <p style="margin-bottom:1.25rem;">
        Under the APPs, you have the right to access the personal information we hold about you and request corrections. 
        You may request deletion of your information at any time by emailing <strong>{CONTACT_EMAIL}</strong>. 
        Australian residents may also lodge inquiries with the Office of the Australian Information Commissioner at <a href="https://oaic.gov.au" target="_blank" rel="noopener" style="color:var(--primary);text-decoration:underline;">oaic.gov.au</a>.
      </p>
    </div>
  </div>
</section>
"""
    return render_page(
        title="Privacy Policy | Best Brokers Australia",
        meta_description="Read the Privacy Policy and Terms of Use for Best Brokers Australia, compliant with the Australian Privacy Act 1988 and Australian Privacy Principles.",
        canonical_url=f"{SITE_URL}/privacy/",
        content_html=content,
        active_nav="/privacy/",
        is_indexable=True,
        schema_jsonld=[breadcrumbs_jsonld(breadcrumbs)],
    )
