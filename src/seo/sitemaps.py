"""
Segmented XML Sitemap Index and Sitemaps Generator.
Implements Blueprint Section 3.2 (robots, sitemaps and index controls) and Phase 11.
"""
from typing import List
from datetime import datetime, timezone
from pathlib import Path
from ..config import SITE_URL, SITE_DIR


def generate_sitemaps(data, output_dir: Path):
    """
    Generates a clean, segmented XML sitemap index:
      - sitemap.xml (Index)
      - sitemap-hubs.xml (Categories, States, Cities)
      - sitemap-pages.xml (Editorial and Trust pages)
      - sitemap-brokers-*.xml (Only indexable quality-score brokers)
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1. Hub URLs (Home, Category, State, City)
    hub_urls = [f"{SITE_URL}/"]
    for cat_slug, hub in data.category_hubs.items():
        if hub.is_indexable:
            hub_urls.append(hub.canonical_url)
    for key, hub in data.state_hubs.items():
        if hub.is_indexable:
            hub_urls.append(hub.canonical_url)
    for key, hub in data.city_hubs.items():
        if hub.is_indexable:
            hub_urls.append(hub.canonical_url)

    _write_urlset(output_dir / "sitemap-hubs.xml", hub_urls, today, changefreq="weekly", priority="0.9")

    # 2. Static / Trust Pages
    static_pages = [
        f"{SITE_URL}/about/",
        f"{SITE_URL}/methodology/",
        f"{SITE_URL}/editorial-policy/",
        f"{SITE_URL}/review-policy/",
        f"{SITE_URL}/claim-profile/",
        f"{SITE_URL}/contact/",
        f"{SITE_URL}/privacy/",
    ]
    _write_urlset(output_dir / "sitemap-pages.xml", static_pages, today, changefreq="monthly", priority="0.6")

    # 3. Indexable Broker Profiles
    indexable_brokers = [b for b in data.brokers if b.is_indexable]
    broker_urls = [b.canonical_url for b in indexable_brokers]

    # Chunk into files of max 10,000 URLs
    chunk_size = 10000
    broker_sitemap_names = []
    for i in range(0, len(broker_urls), chunk_size):
        chunk = broker_urls[i : i + chunk_size]
        file_idx = (i // chunk_size) + 1
        filename = f"sitemap-brokers-{file_idx}.xml"
        _write_urlset(output_dir / filename, chunk, today, changefreq="monthly", priority="0.7")
        broker_sitemap_names.append(filename)

    # 4. Master Sitemap Index
    index_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    
    # Hubs sitemap
    index_xml.append(f'  <sitemap>\n    <loc>{SITE_URL}/sitemap-hubs.xml</loc>\n    <lastmod>{today}</lastmod>\n  </sitemap>')
    # Pages sitemap
    index_xml.append(f'  <sitemap>\n    <loc>{SITE_URL}/sitemap-pages.xml</loc>\n    <lastmod>{today}</lastmod>\n  </sitemap>')
    # Broker sitemaps
    for s_name in broker_sitemap_names:
        index_xml.append(f'  <sitemap>\n    <loc>{SITE_URL}/{s_name}</loc>\n    <lastmod>{today}</lastmod>\n  </sitemap>')

    index_xml.append('</sitemapindex>\n')

    with open(output_dir / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(index_xml))


def _write_urlset(file_path: Path, urls: List[str], lastmod: str, changefreq: str = "monthly", priority: str = "0.7"):
    """Helper to write a single XML urlset."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in sorted(set(urls)):
        lines.append(
            f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>'
        )
    lines.append('</urlset>\n')
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
