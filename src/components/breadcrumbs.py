"""
Breadcrumbs UI component and schema generator.
"""
from typing import List, Dict
import json
from ..config import SITE_URL


def render_breadcrumbs(items: List[Dict[str, str]]) -> str:
    """
    Renders HTML breadcrumb bar with schema microdata and links.
    items: list of dicts with 'name' and 'url'
    """
    if not items:
        return ""

    links_html = []
    for i, item in enumerate(items):
        name = item["name"]
        url = item["url"]
        is_last = (i == len(items) - 1)

        if is_last:
            links_html.append(f'<span class="current" aria-current="page">{name}</span>')
        else:
            links_html.append(f'<a href="{url}">{name}</a>')
            links_html.append('<span class="sep" aria-hidden="true">&rsaquo;</span>')

    return f"""
<nav class="breadcrumbs-bar" aria-label="Breadcrumb">
  <div class="container">
    <ol class="breadcrumbs-list">
      {''.join(f'<li>{link}</li>' for link in links_html)}
    </ol>
  </div>
</nav>
"""


def breadcrumbs_jsonld(items: List[Dict[str, str]]) -> dict:
    """Generates schema.org BreadcrumbList structured data."""
    elements = []
    for i, item in enumerate(items, 1):
        url = item["url"]
        if not url.startswith("http"):
            url = f"{SITE_URL}{url}"
        elements.append({
            "@type": "ListItem",
            "position": i,
            "name": item["name"],
            "item": url,
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }
