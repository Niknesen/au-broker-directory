"""
Robots.txt generator for Best Brokers Australia.
Implements Blueprint Section 3.2.
"""
from pathlib import Path
from ..config import SITE_URL


def generate_robots_txt(output_dir: Path):
    """Generates a clean robots.txt referencing the sitemap index and blocking parameters."""
    content = f"""# Best Brokers Australia robots.txt
User-agent: *
Allow: /

# Disallow internal search & API submission endpoints
Disallow: /search/
Disallow: /api/

# Disallow parameter combinations that create duplicate crawl traps
Disallow: /*?q=*
Disallow: /*?rating=*
Disallow: /*?sort=*

# Sitemap Index
Sitemap: {SITE_URL}/sitemap.xml
"""
    with open(output_dir / "robots.txt", "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
