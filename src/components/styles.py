"""
Design tokens and unified CSS styles for Best Brokers Australia.
One single source of truth for all styles across the site.
"""

CSS_STYLES = """
:root {
  --bg: #f8fafc;
  --bg-surface: #ffffff;
  --bg-subtle: #f1f5f9;
  --bg-alt: #e2e8f0;
  --border: #e2e8f0;
  --border-focus: #3b82f6;
  --text: #0f172a;
  --text-muted: #64748b;
  --text-light: #94a3b8;
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-light: #eff6ff;
  --primary-border: #bfdbfe;
  --accent: #0284c7;
  --success: #16a34a;
  --success-bg: #dcfce7;
  --warning: #d97706;
  --warning-bg: #fef3c7;
  --danger: #dc2626;
  --danger-bg: #fee2e2;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.07);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.08), 0 4px 6px -4px rgb(0 0 0 / 0.08);
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-display: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif;
  --max-w: 1200px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-family: var(--font-sans); color: var(--text); background: var(--bg); line-height: 1.5; -webkit-text-size-adjust: 100%; }
body { min-height: 100vh; display: flex; flex-direction: column; }
a { color: inherit; text-decoration: none; }
img { max-width: 100%; height: auto; display: block; }
button, input, select, textarea { font: inherit; }

.container { width: 100%; max-width: var(--max-w); margin: 0 auto; padding: 0 1.5rem; }

/* Header & Nav */
.site-header { background: var(--bg-surface); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; }
.header-inner { display: flex; align-items: center; justify-content: space-between; height: 70px; }
.brand { display: flex; align-items: center; gap: 0.75rem; font-family: var(--font-display); font-weight: 700; font-size: 1.25rem; color: var(--text); letter-spacing: -0.02em; }
.brand-mark { width: 34px; height: 34px; border-radius: var(--radius-sm); }
.nav-links { display: flex; align-items: center; gap: 1.5rem; list-style: none; }
.nav-links a { font-size: 0.9375rem; font-weight: 500; color: var(--text-muted); transition: color 0.15s ease; }
.nav-links a:hover, .nav-links a.active { color: var(--primary); }
.header-cta { display: inline-flex; align-items: center; gap: 0.5rem; background: var(--primary-light); color: var(--primary); border: 1px solid var(--primary-border); padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 0.875rem; font-weight: 600; transition: all 0.15s ease; }
.header-cta:hover { background: var(--primary); color: #fff; }
.menu-toggle { display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; }

/* Breadcrumbs */
.breadcrumbs-bar { background: var(--bg-surface); border-bottom: 1px solid var(--border); padding: 0.75rem 0; font-size: 0.875rem; color: var(--text-muted); }
.breadcrumbs-list { display: flex; align-items: center; flex-wrap: wrap; gap: 0.5rem; list-style: none; }
.breadcrumbs-list a { color: var(--text-muted); transition: color 0.15s; }
.breadcrumbs-list a:hover { color: var(--primary); }
.breadcrumbs-list .sep { color: var(--text-light); }
.breadcrumbs-list .current { color: var(--text); font-weight: 500; }

/* Hero sections */
.hero { background: var(--bg-surface); border-bottom: 1px solid var(--border); padding: 3.5rem 0 3rem; }
.hero-grid { display: grid; grid-template-columns: 1fr 380px; gap: 3rem; align-items: center; }
.hero-category-badge { display: inline-flex; align-items: center; gap: 0.5rem; background: var(--primary-light); color: var(--primary); padding: 0.35rem 0.85rem; border-radius: var(--radius-full); font-size: 0.8125rem; font-weight: 600; margin-bottom: 1rem; }
.hero h1 { font-family: var(--font-display); font-size: 2.5rem; font-weight: 700; line-height: 1.15; letter-spacing: -0.03em; color: var(--text); margin-bottom: 1rem; }
.hero-lead { font-size: 1.125rem; color: var(--text-muted); max-width: 760px; line-height: 1.6; margin-bottom: 1.5rem; }
.hero-stats { display: flex; align-items: center; flex-wrap: wrap; gap: 1.5rem; font-size: 0.875rem; color: var(--text-muted); padding-top: 1rem; border-top: 1px solid var(--border); }
.hero-stat-item { display: flex; align-items: center; gap: 0.5rem; font-weight: 500; }
.hero-stat-item strong { color: var(--text); }

.hero-image-card { position: relative; display: flex; justify-content: center; }
.hero-portrait-img { width: 100%; max-width: 360px; height: auto; border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); border: 1px solid var(--border); object-fit: cover; }
.hero-image-badge { position: absolute; bottom: 1.25rem; left: 1rem; right: 1rem; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 0.75rem 1rem; display: flex; align-items: center; gap: 0.75rem; box-shadow: var(--shadow-md); color: var(--text); font-size: 0.8125rem; }
.hero-image-badge svg { color: var(--primary); flex-shrink: 0; }
.hero-image-badge strong { display: block; font-size: 0.875rem; color: var(--text); }
.hero-image-badge span { color: var(--text-muted); }

@media (max-width: 900px) {
  .hero-grid { grid-template-columns: 1fr; gap: 2rem; }
  .hero-image-card { display: none; }
}

/* Search Box */
.search-wrapper { position: relative; max-width: 640px; margin: 1.5rem 0 0.5rem; }
.search-input { width: 100%; padding: 0.9rem 1.25rem 0.9rem 3rem; font-size: 1rem; background: var(--bg); border: 2px solid var(--border); border-radius: var(--radius-md); color: var(--text); outline: none; transition: all 0.15s; }
.search-input:focus { border-color: var(--primary); background: #fff; box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
.search-icon { position: absolute; left: 1.1rem; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; color: var(--text-light); pointer-events: none; }
.search-results-box { margin-top: 0.75rem; background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-md); box-shadow: var(--shadow-lg); overflow: hidden; display: none; }
.search-result-item { display: flex; align-items: center; justify-content: space-between; padding: 0.875rem 1.25rem; border-bottom: 1px solid var(--border); transition: background 0.1s; }
.search-result-item:hover { background: var(--bg-subtle); }
.search-result-item:last-child { border-bottom: none; }

/* Grid Layouts */
.section { padding: 3rem 0; }
.section-alt { background: var(--bg-surface); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
.section-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 2rem; }
.section-title { font-family: var(--font-display); font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em; }
.section-subtitle { font-size: 0.9375rem; color: var(--text-muted); margin-top: 0.25rem; }

.broker-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.5rem; }
.category-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.25rem; }
.location-chips { display: flex; flex-wrap: wrap; gap: 0.625rem; }
.location-chip { display: inline-flex; align-items: center; gap: 0.5rem; background: var(--bg-surface); border: 1px solid var(--border); padding: 0.5rem 0.875rem; border-radius: var(--radius-md); font-size: 0.875rem; font-weight: 500; color: var(--text); transition: all 0.15s; }
.location-chip:hover { border-color: var(--primary); color: var(--primary); background: var(--primary-light); }
.location-chip .count { background: var(--bg-subtle); color: var(--text-muted); padding: 0.1rem 0.45rem; border-radius: var(--radius-full); font-size: 0.75rem; }

/* Broker Card */
.broker-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow-sm); transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s; position: relative; }
.broker-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); border-color: var(--primary-border); }
.broker-card-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 1rem; }
.broker-avatar { width: 46px; height: 46px; border-radius: var(--radius-md); background: var(--primary-light); color: var(--primary); font-family: var(--font-display); font-weight: 700; font-size: 1.25rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.broker-title-group { flex: 1; }
.broker-name { font-size: 1.125rem; font-weight: 700; color: var(--text); margin-bottom: 0.25rem; line-height: 1.3; }
.broker-meta { font-size: 0.8125rem; color: var(--text-muted); display: flex; align-items: center; flex-wrap: wrap; gap: 0.4rem; }
.broker-rating-badge { display: inline-flex; align-items: center; gap: 0.35rem; font-size: 0.8125rem; font-weight: 600; color: #b45309; background: #fffbeb; padding: 0.2rem 0.5rem; border-radius: var(--radius-sm); border: 1px solid #fef3c7; }
.trust-pill { display: inline-flex; align-items: center; gap: 0.35rem; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: var(--radius-full); letter-spacing: 0.02em; }
.trust-pill.high { background: var(--success-bg); color: var(--success); }
.trust-pill.mid { background: var(--warning-bg); color: var(--warning); }
.trust-pill.low { background: var(--bg-subtle); color: var(--text-muted); }

.trust-circle-wrap { display: inline-flex; flex-direction: column; align-items: center; gap: 0.2rem; flex-shrink: 0; }
.trust-circle-svg { display: block; overflow: visible; }
.trust-circle-label { font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; }
.broker-badges { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 1rem 0; }
.badge-item { font-size: 0.75rem; font-weight: 500; background: var(--bg-subtle); color: var(--text-muted); padding: 0.25rem 0.55rem; border-radius: var(--radius-sm); }
.broker-card-footer { display: flex; align-items: center; justify-content: space-between; padding-top: 1rem; border-top: 1px solid var(--border); margin-top: auto; }
.btn-card { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.875rem; font-weight: 600; color: var(--primary); }
.btn-card:hover { color: var(--primary-hover); text-decoration: underline; }

/* Broker Profile Page Layout */
.profile-header { background: var(--bg-surface); border-bottom: 1px solid var(--border); padding: 2.5rem 0; }
.profile-hero { display: grid; grid-template-columns: 1fr 340px; gap: 2.5rem; align-items: start; }
.profile-title-area h1 { font-family: var(--font-display); font-size: 2.25rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
.profile-badges { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0 1.25rem; }
.profile-grid { display: grid; grid-template-columns: 1fr 340px; gap: 2rem; margin-top: 2rem; }
.profile-main { display: flex; flex-direction: column; gap: 1.75rem; }
.profile-sidebar { display: flex; flex-direction: column; gap: 1.5rem; }

.card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.75rem; box-shadow: var(--shadow-sm); }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; }
.card-title { font-family: var(--font-display); font-size: 1.25rem; font-weight: 700; letter-spacing: -0.01em; }
.card-subtitle { font-size: 0.8125rem; color: var(--text-muted); }

/* Reveal Fields */
.reveal-box { background: var(--bg-subtle); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 0.875rem 1rem; margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: space-between; }
.reveal-label { font-size: 0.8125rem; color: var(--text-muted); font-weight: 500; display: flex; align-items: center; gap: 0.4rem; }
.reveal-value { font-size: 0.9375rem; font-weight: 600; color: var(--text); user-select: all; }
.reveal-btn { background: #fff; border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 0.3rem 0.75rem; font-size: 0.8125rem; font-weight: 600; color: var(--primary); cursor: pointer; transition: all 0.15s; }
.reveal-btn:hover { background: var(--primary-light); border-color: var(--primary-border); }

/* Reviews & Testimonials */
.review-item { padding: 1.25rem 0; border-bottom: 1px solid var(--border); }
.review-item:last-child { border-bottom: none; padding-bottom: 0; }
.review-meta { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; }
.reviewer-name { font-weight: 600; font-size: 0.9375rem; }
.review-date { font-size: 0.8125rem; color: var(--text-muted); }
.review-text { font-size: 0.9375rem; color: var(--text); line-height: 1.6; }

/* FAQ Accordion */
.faq-item { border-bottom: 1px solid var(--border); padding: 1.25rem 0; }
.faq-item:last-child { border-bottom: none; }
.faq-q { font-weight: 600; font-size: 1.0625rem; margin-bottom: 0.5rem; color: var(--text); }
.faq-a { font-size: 0.9375rem; color: var(--text-muted); line-height: 1.6; }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-top: 2.5rem; }
.page-link { display: inline-flex; align-items: center; justify-content: center; min-width: 40px; height: 40px; padding: 0 0.75rem; border: 1px solid var(--border); background: var(--bg-surface); border-radius: var(--radius-md); font-size: 0.875rem; font-weight: 600; color: var(--text); transition: all 0.15s; }
.page-link:hover { border-color: var(--primary); color: var(--primary); background: var(--primary-light); }
.page-link.active { background: var(--primary); border-color: var(--primary); color: #fff; }
.page-link.disabled { opacity: 0.5; pointer-events: none; }

/* Footer */
.site-footer { background: #0f172a; color: #94a3b8; border-top: 1px solid #1e293b; padding: 4rem 0 2rem; font-size: 0.875rem; margin-top: auto; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 3rem; margin-bottom: 3rem; }
.footer-brand h3 { font-family: var(--font-display); font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem; }
.footer-desc { font-size: 0.875rem; line-height: 1.6; color: #94a3b8; max-width: 320px; }
.footer-col h4 { font-family: var(--font-display); font-size: 0.9375rem; font-weight: 600; color: #fff; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; }
.footer-links { list-style: none; display: flex; flex-direction: column; gap: 0.625rem; }
.footer-links a { color: #94a3b8; transition: color 0.15s; }
.footer-links a:hover { color: #fff; }
.footer-bottom { padding-top: 2rem; border-top: 1px solid #1e293b; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; font-size: 0.8125rem; }
.footer-disclaimer { max-width: 600px; line-height: 1.5; color: #64748b; }

/* Responsive adjustments */
@media (max-width: 900px) {
  .hero h1 { font-size: 2rem; }
  .profile-hero, .profile-grid { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 2rem; }
}
@media (max-width: 640px) {
  .hero h1 { font-size: 1.75rem; }
  .nav-links { display: none; }
  .menu-toggle { display: block; }
  .broker-grid { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr; }
  .footer-bottom { flex-direction: column; align-items: flex-start; }
}
"""
