"""
Command-line interface for Best Brokers Australia site generator.
"""
import argparse
import sys
from pathlib import Path

from .config import SITE_DIR, DOCS_DIR
from .models import load_all_data
from .builder import SiteBuilder


def main():
    parser = argparse.ArgumentParser(description="Best Brokers Australia Site Generator")
    parser.add_argument("--all", action="store_true", help="Full site generation (hubs + all brokers)")
    parser.add_argument("--hubs-only", action="store_true", help="Generate only homepage, category/state/city hubs, static pages and SEO files")
    parser.add_argument("--brokers-only", action="store_true", help="Generate only broker profile pages")
    parser.add_argument("--slug", type=str, help="Generate a single broker profile by slug or ID")
    parser.add_argument("--output", type=str, default=str(SITE_DIR), help="Output directory (defaults to site/)")
    parser.add_argument("--no-sync", action="store_true", help="Do not sync output to docs/ folder")

    args = parser.parse_args()
    out_dir = Path(args.output)

    print("Loading directory datasets...")
    data = load_all_data()
    print(f"Loaded {data.total_brokers:,} total brokers ({data.total_indexable_brokers:,} indexable).")

    builder = SiteBuilder(data=data, output_dir=out_dir)

    if args.slug:
        builder.build_single_broker(args.slug)
    elif args.hubs_only:
        builder.build_hubs_and_core()
        if not args.no_sync and out_dir == SITE_DIR:
            import shutil
            print("Syncing hubs to docs/...")
            for item in out_dir.iterdir():
                if item.name != "broker":
                    dst = DOCS_DIR / item.name
                    if item.is_dir():
                        if dst.exists(): shutil.rmtree(dst)
                        shutil.copytree(item, dst)
                    else:
                        shutil.copy2(item, dst)
    elif args.brokers_only:
        builder.ensure_directories()
        builder.build_all_brokers()
    else:
        # Default is --all
        builder.build_all(sync_to_docs=not args.no_sync)


if __name__ == "__main__":
    main()
