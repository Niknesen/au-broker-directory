"""
404 Not Found Page Template for Best Brokers Australia.
"""
from ..config import SITE_NAME, SITE_URL
from ..taxonomy import CATEGORIES, url_for_category, url_for_home
from ..components.base import render_page


def render_404_page() -> str:
    """Renders a clean, user-friendly 404 page."""
    category_links = "".join(
        f'<a class="location-chip" href="{url_for_category(cat["slug"])}">{cat["short_name"]}</a>'
        for cat in CATEGORIES.values()
    )

    content = f"""
<div class="hero">
  <div class="container" style="text-align:center;padding:5rem 0;">
    <span class="hero-category-badge" style="background:var(--danger-bg);color:var(--danger);">Error 404</span>
    <h1 style="margin-bottom:1rem;">Page Not Found</h1>
    <p class="hero-lead" style="margin:0 auto 2rem;max-width:540px;">
      The broker listing, category hub, or page you were looking for does not exist or may have been moved.
    </p>

    <div style="display:flex;justify-content:center;gap:1rem;margin-bottom:3rem;">
      <a href="{url_for_home()}" class="header-cta" style="padding:0.75rem 1.5rem;font-size:1rem;">
        &larr; Return to Directory Home
      </a>
    </div>

    <div style="max-width:640px;margin:0 auto;text-align:left;">
      <h3 style="font-size:1rem;color:var(--text-muted);margin-bottom:1rem;text-align:center;">Or explore our main sectors:</h3>
      <div class="location-chips" style="justify-content:center;">
        {category_links}
      </div>
    </div>
  </div>
</div>
"""

    return render_page(
        title=f"Page Not Found (404) | {SITE_NAME}",
        meta_description="The requested page could not be found on Best Brokers Australia.",
        canonical_url=f"{SITE_URL}/404.html",
        content_html=content,
        active_nav="",
        is_indexable=False,
    )
