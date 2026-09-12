"""
Site configuration and constants for Best Brokers Australia.
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
SITE_DIR = ROOT / "site"
DOCS_DIR = ROOT / "docs"
SUBMISSIONS_DIR = DATA_DIR / "submissions"
ASSETS_SRC_DIR = ROOT / "assets_src"

# Canonical URL configuration
SITE_URL = "https://bestbrokersaustralia.org"
SITE_NAME = "Best Brokers Australia"
SITE_TAGLINE = "Find & Compare Verified Australian Brokers"
SITE_DESCRIPTION = (
    "Australia's independent directory of verified mortgage, finance, insurance, "
    "real estate, business sales, asset finance, customs, and wealth brokers."
)
OPERATOR_NAME = "AIEX Forward Deployed Engineering"
OPERATOR_URL = "https://aiex.team"
CONTACT_EMAIL = "nick@aiex.team"

# Local dev server
PORT = 8941

# Quality score thresholds for indexation (Blueprint Section 4)
QUALITY_SCORE_INDEX_MIN = 70
QUALITY_SCORE_CONDITIONAL_MIN = 50

# Minimum brokers required to generate an indexable city hub page (Blueprint Section 2)
MIN_BROKERS_FOR_CITY_HUB = 5
MIN_BROKERS_FOR_SUBURB_HUB = 3

# Hub pagination size (maximum 9 results per view/industry)
BROKERS_PER_PAGE = 9

# Data sources
BROKERS_SOURCE = DATA_DIR / "all_brokers_full.json"
REVIEWS_SOURCE = DATA_DIR / "reviews_by_place.json"
MANUAL_REVIEWS_SOURCE = DATA_DIR / "manual_reviews.json"
