"""
Submission and interaction forms for Best Brokers Australia:
- Review Submission
- Real Case Study Submission
- Claim & Verify Profile
- Dispute / Correction Request
"""
import html


def render_review_form(broker_slug: str, broker_name: str) -> str:
    """Renders the client review submission form."""
    b_slug = html.escape(broker_slug)
    b_name = html.escape(broker_name)

    return f"""
<div class="card" id="submit-review">
  <div class="card-header">
    <div>
      <h3 class="card-title">Write a Verified Review</h3>
      <p class="card-subtitle">Share your real experience with {b_name}</p>
    </div>
  </div>
  <form class="ajax-form" data-endpoint="/api/reviews" data-broker-slug="{b_slug}" data-broker-name="{b_name}">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
      <div>
        <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">Your Name *</label>
        <input type="text" name="name" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="e.g. Sarah Jenkins">
      </div>
      <div>
        <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">Your Email * (Kept private)</label>
        <input type="email" name="email" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="name@example.com.au">
      </div>
    </div>
    
    <div style="margin-bottom:1rem;">
      <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">Overall Rating *</label>
      <select name="rating" required class="search-input" style="padding:0.6rem 0.85rem;background:#fff;">
        <option value="5">&#9733;&#9733;&#9733;&#9733;&#9733; (5/5) — Outstanding Service</option>
        <option value="4">&#9733;&#9733;&#9733;&#9733;&#9734; (4/5) — Very Good</option>
        <option value="3">&#9733;&#9733;&#9733;&#9734;&#9734; (3/5) — Average / Satisfactory</option>
        <option value="2">&#9733;&#9733;&#9734;&#9734;&#9734; (2/5) — Below Expectations</option>
        <option value="1">&#9733;&#9734;&#9734;&#9734;&#9734; (1/5) — Poor Experience</option>
      </select>
    </div>

    <div style="margin-bottom:1rem;">
      <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">Your Review *</label>
      <textarea name="text" rows="4" required class="search-input" style="padding:0.75rem 0.85rem;min-height:100px;" placeholder="Describe your loan scenario, responsiveness, clarity, and overall outcome..."></textarea>
    </div>

    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
      <label style="font-size:0.75rem;color:var(--text-muted);display:flex;align-items:center;gap:0.4rem;">
        <input type="checkbox" required checked> I certify this review reflects a genuine client interaction.
      </label>
      <button type="submit" class="header-cta" style="border:none;cursor:pointer;padding:0.6rem 1.25rem;">
        Submit Review &rarr;
      </button>
    </div>
    <div class="form-feedback" style="display:none;margin-top:1rem;padding:0.75rem;border-radius:var(--radius-md);"></div>
  </form>
</div>
"""


def render_case_form(broker_slug: str, broker_name: str) -> str:
    """Renders the case study submission form."""
    b_slug = html.escape(broker_slug)
    b_name = html.escape(broker_name)

    return f"""
<div class="card" id="submit-case">
  <div class="card-header">
    <div>
      <h3 class="card-title">Share a Real Deal / Client Case</h3>
      <p class="card-subtitle">Clients or brokers can submit real transaction stories</p>
    </div>
  </div>
  <form class="ajax-form" data-endpoint="/api/cases" data-broker-slug="{b_slug}" data-broker-name="{b_name}">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem;">
      <div>
        <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">Your Name *</label>
        <input type="text" name="name" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="Your full name">
      </div>
      <div>
        <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">Your Email *</label>
        <input type="email" name="email" required class="search-input" style="padding:0.6rem 0.85rem;" placeholder="name@example.com.au">
      </div>
    </div>

    <div style="margin-bottom:1rem;">
      <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">I am submitting as *</label>
      <select name="role" required class="search-input" style="padding:0.6rem 0.85rem;background:#fff;">
        <option value="client">Client (Borrower / Buyer / Insured)</option>
        <option value="broker">Broker / Team Member</option>
      </select>
    </div>

    <div style="margin-bottom:1rem;">
      <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">Case Details / Scenario & Outcome *</label>
      <textarea name="text" rows="4" required class="search-input" style="padding:0.75rem 0.85rem;min-height:100px;" placeholder="Explain the initial challenge (e.g. self-employed refinance, tight deadline), lender negotiated, and final rate/savings outcome..."></textarea>
    </div>

    <div style="margin-bottom:1.25rem;">
      <label style="display:block;font-size:0.8125rem;font-weight:600;margin-bottom:0.35rem;color:var(--text);">
        📎 Attachment Proof (Optional photo, settlement doc, or short video &mdash; Max 10MB)
      </label>
      <div style="border:1px dashed var(--border);border-radius:var(--radius-md);padding:0.85rem 1rem;background:var(--bg-subtle);">
        <input type="file" name="attachment" accept="image/*,.pdf,.doc,.docx,video/mp4,video/quicktime" style="font-size:0.8125rem;cursor:pointer;width:100%;">
        <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.35rem;">
          Supported: PDF, JPG, PNG, WEBP, DOCX, MP4, MOV (Maximum file size: 10MB)
        </div>
      </div>
    </div>

    <button type="submit" class="header-cta" style="border:none;cursor:pointer;padding:0.6rem 1.25rem;">
      Submit Case Study &rarr;
    </button>
    <div class="form-feedback" style="display:none;margin-top:1rem;padding:0.75rem;border-radius:var(--radius-md);"></div>
  </form>
</div>
"""
