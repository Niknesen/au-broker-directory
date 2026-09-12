"""
Master Site Builder and Static Site Generator for Best Brokers Australia.
Provides full, hub-only, and single-broker incremental compilation.
"""
import json
import shutil
import time
from pathlib import Path
from typing import Optional, List

from .config import SITE_DIR, DOCS_DIR
from .models import DirectoryData, load_all_data
from .templates.home import render_homepage
from .templates.category import render_category_page
from .templates.state import render_state_page
from .templates.city import render_city_page
from .templates.broker import render_broker_profile
from .templates.static import (
    render_about_page,
    render_methodology_page,
    render_editorial_policy_page,
    render_review_policy_page,
    render_claim_page,
    render_contact_page,
    render_privacy_page,
)
from .templates.not_found import render_404_page
from .seo.sitemaps import generate_sitemaps
from .seo.robots import generate_robots_txt
from .seo.redirects import generate_cloudflare_config


class SiteBuilder:
    def __init__(self, data: Optional[DirectoryData] = None, output_dir: Path = SITE_DIR):
        self.output_dir = output_dir
        self.data = data or load_all_data()

    def ensure_directories(self):
        """Ensures all necessary output base directories exist and cleans up legacy files."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        broker_dir = self.output_dir / "broker"
        broker_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove legacy flat .html files in broker/ so they don't duplicate with broker/:slug/index.html
        for legacy_html in broker_dir.glob("*.html"):
            try: legacy_html.unlink()
            except OSError: pass

        # Clean category dirs so stale hubs don't accumulate
        from .taxonomy import CATEGORIES
        for cat in CATEGORIES.values():
            cat_p = self.output_dir / cat["slug"]
            if cat_p.exists():
                try: shutil.rmtree(cat_p)
                except OSError: pass

        # Remove legacy root .html pages
        for root_legacy in ["about.html", "contact.html", "privacy.html", "methodology.html", "editorial-policy.html", "review-policy.html", "claim-profile.html"]:
            p = self.output_dir / root_legacy
            if p.exists():
                try: p.unlink()
                except OSError: pass

        # Ensure static assets are copied
        src_assets = SITE_DIR / "assets"
        dst_assets = self.output_dir / "assets"
        if src_assets.exists() and src_assets != dst_assets:
            if dst_assets.exists():
                shutil.rmtree(dst_assets)
            shutil.copytree(src_assets, dst_assets)

    def write_search_index(self):
        """Writes lightweight client-side search index consumed by homepage."""
        index_records = [
            {
                "slug": b.slug,
                "name": b.name,
                "category": b.category,
                "city": b.city or "",
                "suburb": b.suburb or "",
                "state": b.state or "",
                "phone": b.phone or "",
                "score": b.trust_score,
                "has_reviews": bool(b.google_reviews),
            }
            for b in self.data.brokers
        ]
        with open(self.output_dir / "data.json", "w", encoding="utf-8") as f:
            json.dump(index_records, f, ensure_ascii=False)

    def build_static_pages(self):
        """Builds all trust, governance, editorial, and legal pages."""
        pages = {
            "about": render_about_page(),
            "methodology": render_methodology_page(),
            "editorial-policy": render_editorial_policy_page(),
            "review-policy": render_review_policy_page(),
            "claim-profile": render_claim_page(),
            "contact": render_contact_page(),
            "privacy": render_privacy_page(),
        }
        for slug, html_content in pages.items():
            page_dir = self.output_dir / slug
            page_dir.mkdir(parents=True, exist_ok=True)
            with open(page_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(html_content)

        # 404 page
        with open(self.output_dir / "404.html", "w", encoding="utf-8") as f:
            f.write(render_404_page())

    def build_homepage(self):
        """Builds the homepage."""
        with open(self.output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(render_homepage(self.data))

    def build_category_hubs(self):
        """Builds all national category hubs."""
        for cat_slug, hub in self.data.category_hubs.items():
            cat_dir = self.output_dir / cat_slug
            cat_dir.mkdir(parents=True, exist_ok=True)
            with open(cat_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(render_category_page(hub, page=1))

    def build_state_hubs(self):
        """Builds all state category hubs."""
        for key, hub in self.data.state_hubs.items():
            cat_slug, state_slug = key.split("/")
            state_dir = self.output_dir / cat_slug / state_slug
            state_dir.mkdir(parents=True, exist_ok=True)
            with open(state_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(render_state_page(hub, page=1))

    def build_city_hubs(self):
        """Builds all city category hubs."""
        for key, hub in self.data.city_hubs.items():
            cat_slug, city_slug = key.split("/")
            city_dir = self.output_dir / cat_slug / city_slug
            city_dir.mkdir(parents=True, exist_ok=True)
            with open(city_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(render_city_page(hub, page=1))

    def build_seo_assets(self):
        """Builds sitemaps index, robots.txt, and Cloudflare config files."""
        generate_sitemaps(self.data, self.output_dir)
        generate_robots_txt(self.output_dir)
        generate_cloudflare_config(self.output_dir)

    def build_hubs_and_core(self):
        """Builds homepage, hubs, static pages, search index, and SEO files."""
        t0 = time.time()
        self.ensure_directories()
        self.write_search_index()
        self.build_homepage()
        self.build_static_pages()
        self.build_category_hubs()
        self.build_state_hubs()
        self.build_city_hubs()
        self.build_seo_assets()
        elapsed = time.time() - t0
        print(f"[Core & Hubs] Built homepage, 7 category hubs, {len(self.data.state_hubs)} state hubs, {len(self.data.city_hubs)} city hubs, trust pages & sitemaps in {elapsed:.2f}s")

    def build_single_broker(self, slug_or_id: str):
        """Instantly compiles a single broker profile without touching any other files."""
        broker = self.data.brokers_by_slug.get(slug_or_id) or self.data.brokers_by_id.get(slug_or_id)
        if not broker:
            raise ValueError(f"Broker with slug/id '{slug_or_id}' not found.")

        broker_dir = self.output_dir / "broker" / broker.slug
        broker_dir.mkdir(parents=True, exist_ok=True)
        with open(broker_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(render_broker_profile(broker))
        print(f"[Single Build] Generated broker profile: {broker.slug} -> {broker_dir / 'index.html'}")

    def build_all_brokers(self):
        """Builds all ~16,917 individual broker pages."""
        t0 = time.time()
        count = len(self.data.brokers)
        for i, b in enumerate(self.data.brokers, 1):
            broker_dir = self.output_dir / "broker" / b.slug
            broker_dir.mkdir(parents=True, exist_ok=True)
            with open(broker_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(render_broker_profile(b))
            
            if i % 2500 == 0 or i == count:
                print(f"[Broker Progress] Generated {i:,}/{count:,} broker pages...")

        elapsed = time.time() - t0
        print(f"[All Brokers] Generated {count:,} broker pages in {elapsed:.2f}s")

    def build_all(self, sync_to_docs: bool = True):
        """Runs the complete full-site build pipeline."""
        t_start = time.time()
        print(f"=== Starting Full Build for {self.data.total_brokers:,} brokers ===")
        self.build_hubs_and_core()
        self.build_all_brokers()
        
        if sync_to_docs and self.output_dir == SITE_DIR:
            t_sync = time.time()
            print(f"Syncing site/ to docs/ for Cloudflare Pages...")
            if DOCS_DIR.exists():
                shutil.rmtree(DOCS_DIR)
            shutil.copytree(SITE_DIR, DOCS_DIR)
            print(f"Synced site/ -> docs/ in {time.time() - t_sync:.2f}s")

        total_time = time.time() - t_start
        print(f"=== Full Build Completed in {total_time:.2f}s ===")
