"""
Base Document Shell and Layout for Best Brokers Australia.
Provides the single master HTML wrapper for all pages.
"""
import json
import html
from typing import Optional, List, Dict
from ..config import SITE_NAME, SITE_URL, SITE_DESCRIPTION
from .styles import CSS_STYLES
from .header import render_header
from .footer import render_footer


def render_page(
    title: str,
    meta_description: str,
    canonical_url: str,
    content_html: str,
    active_nav: str = "",
    is_indexable: bool = True,
    schema_jsonld: Optional[List[dict]] = None,
    extra_head: str = "",
) -> str:
    """
    Renders the complete HTML5 document.
    Ensures absolute canonicals, unified head tags, schema injection, and noindex control.
    """
    robots_meta = "index, follow" if is_indexable else "noindex, follow"
    escaped_title = html.escape(title)
    escaped_desc = html.escape(meta_description or SITE_DESCRIPTION)

    # Prepare JSON-LD script tags
    schema_scripts = []
    if schema_jsonld:
        for s in schema_jsonld:
            if s:
                schema_scripts.append(
                    f'<script type="application/ld+json">\n{json.dumps(s, indent=2, ensure_ascii=False)}\n</script>'
                )
    schemas_rendered = "\n".join(schema_scripts)

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-PNGJR452');</script>
  <!-- End Google Tag Manager -->

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-KVR945JRS2"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-KVR945JRS2');
  </script>
  <!-- End Google tag (gtag.js) -->

  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "yhkd62j0gn");
  </script>
  <!-- End Microsoft Clarity -->

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escaped_title}</title>
  <meta name="description" content="{escaped_desc}">
  <meta name="robots" content="{robots_meta}">
  <link rel="canonical" href="{canonical_url}">

  <!-- Open Graph / Social -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{escaped_title}">
  <meta property="og:description" content="{escaped_desc}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{SITE_URL}/assets/favicon-32.png">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{escaped_title}">
  <meta name="twitter:description" content="{escaped_desc}">

  <!-- Nick pixel -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '1256510258585870');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id=1256510258585870&ev=PageView&noscript=1"
  alt="" /></noscript>
  <!-- End Nick pixel -->

  <!-- Favicons -->
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">

  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">

  <style>
{CSS_STYLES}
  </style>
  
  {schemas_rendered}
  {extra_head}
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PNGJR452"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

  {render_header(active_nav)}
  
  <main id="main-content">
    {content_html}
  </main>

  {render_footer()}

  <script>
  // Reveal & Clipboard Interactions
  document.addEventListener('click', function(e) {{
    var revealBtn = e.target.closest('.reveal-btn');
    if (revealBtn) {{
      var box = revealBtn.closest('.reveal-box');
      if (!box) return;
      box.classList.add('is-revealed');
      revealBtn.style.display = 'none';
      var unfolded = box.querySelector('.reveal-unfolded');
      if (unfolded) {{
        unfolded.style.display = 'flex';
      }}
      return;
    }}

    var copyBtn = e.target.closest('.copy-action-btn');
    if (copyBtn) {{
      var box = copyBtn.closest('.reveal-box');
      var val = box ? box.dataset.value : '';
      if (val && navigator.clipboard) {{
        navigator.clipboard.writeText(val).then(function() {{
          var origHtml = copyBtn.innerHTML;
          copyBtn.innerHTML = '✓ Copied!';
          copyBtn.classList.add('copied');
          setTimeout(function() {{
            copyBtn.innerHTML = origHtml;
            copyBtn.classList.remove('copied');
          }}, 2000);
        }});
      }}
    }}
  }});

  // AJAX Form Handler
  document.addEventListener('submit', function(e) {{
    var form = e.target.closest('.ajax-form');
    if (!form) return;
    e.preventDefault();
    
    var endpoint = form.dataset.endpoint;
    var feedback = form.querySelector('.form-feedback');
    var submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

    var data = {{
      broker_slug: form.dataset.brokerSlug || '',
      broker_name: form.dataset.brokerName || '',
    }};
    var formData = new FormData(form);
    formData.forEach(function(value, key) {{
      data[key] = value;
    }});

    fetch(endpoint, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(data)
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(res) {{
      if (res.ok) {{
        if (feedback) {{
          feedback.style.display = 'block';
          feedback.style.background = 'var(--success-bg)';
          feedback.style.color = 'var(--success)';
          feedback.textContent = 'Thank you! Your submission has been received and queued for review.';
        }}
        form.reset();
      }} else {{
        if (feedback) {{
          feedback.style.display = 'block';
          feedback.style.background = 'var(--danger-bg)';
          feedback.style.color = 'var(--danger)';
          feedback.textContent = res.error || 'Submission failed. Please check your inputs.';
        }}
        if (submitBtn) submitBtn.disabled = false;
      }}
    }})
    .catch(function(err) {{
      if (feedback) {{
        feedback.style.display = 'block';
        feedback.style.background = 'var(--danger-bg)';
        feedback.style.color = 'var(--danger)';
        feedback.textContent = 'A network error occurred. Please try again.';
      }}
      if (submitBtn) submitBtn.disabled = false;
    }});
  }});
  </script>
</body>
</html>
"""
