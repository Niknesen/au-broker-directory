"""
Taxonomy and routing definitions for Best Brokers Australia.
"""
import re

CATEGORIES = {
    "Mortgage & Finance": {
        "slug": "mortgage-brokers",
        "name": "Mortgage & Finance Brokers",
        "short_name": "Mortgage Brokers",
        "singular": "Mortgage Broker",
        "schema_type": "FinancialService",
        "description": "Compare verified Australian mortgage and finance brokers. Check independent trust scores, real client reviews, credit representative disclosures, and local loan specialties.",
        "icon": "home",
    },
    "Insurance": {
        "slug": "insurance-brokers",
        "name": "Insurance Brokers & Advisers",
        "short_name": "Insurance Brokers",
        "singular": "Insurance Broker",
        "schema_type": "InsuranceAgency",
        "description": "Find licensed Australian general, commercial, and professional insurance brokers. Compare independent reputation ratings, local service coverage, and direct contacts.",
        "icon": "shield",
    },
    "Real Estate & Buyers": {
        "slug": "real-estate-agents",
        "name": "Real Estate & Buyers Agents",
        "short_name": "Real Estate Agents",
        "singular": "Real Estate Agent",
        "schema_type": "RealEstateAgent",
        "description": "Discover top-rated Australian real estate agencies and independent buyers agents. Compare verified sales track records, suburb expertise, and client reviews.",
        "icon": "building",
    },
    "Business Sales & Franchise": {
        "slug": "business-brokers",
        "name": "Business & Franchise Brokers",
        "short_name": "Business Brokers",
        "singular": "Business Broker",
        "schema_type": "FinancialService",
        "description": "Connect with accredited Australian business brokers and franchise sales specialists for buying, selling, or valuing commercial operations across Australia.",
        "icon": "briefcase",
    },
    "Asset & Equipment Finance": {
        "slug": "asset-finance-brokers",
        "name": "Asset & Equipment Finance Brokers",
        "short_name": "Asset Finance Brokers",
        "singular": "Asset Finance Broker",
        "schema_type": "FinancialService",
        "description": "Compare specialized Australian vehicle, heavy machinery, and commercial equipment finance brokers with fast approval pathways and independent ratings.",
        "icon": "truck",
    },
    "Customs & Freight": {
        "slug": "customs-brokers",
        "name": "Customs & Freight Brokers",
        "short_name": "Customs Brokers",
        "singular": "Customs Broker",
        "schema_type": "LocalBusiness",
        "description": "Find licensed Australian customs brokers and international freight forwarding specialists for border clearance, import/export compliance, and supply chain logistics.",
        "icon": "globe",
    },
    "Wealth & Investment": {
        "slug": "wealth-advisers",
        "name": "Wealth & Financial Advisers",
        "short_name": "Wealth Advisers",
        "singular": "Wealth Adviser",
        "schema_type": "FinancialService",
        "description": "Browse qualified Australian financial planners, wealth advisers, and investment brokers. Compare verified credentials, advisory scopes, and client testimonials.",
        "icon": "trending-up",
    },
}

# Reverse lookup from category slug to sheet name
CATEGORY_SLUG_TO_SHEET = {v["slug"]: k for k, v in CATEGORIES.items()}

STATES = {
    "NSW": {"name": "New South Wales", "slug": "nsw", "capital": "Sydney"},
    "VIC": {"name": "Victoria", "slug": "vic", "capital": "Melbourne"},
    "QLD": {"name": "Queensland", "slug": "qld", "capital": "Brisbane"},
    "WA": {"name": "Western Australia", "slug": "wa", "capital": "Perth"},
    "SA": {"name": "South Australia", "slug": "sa", "capital": "Adelaide"},
    "ACT": {"name": "Australian Capital Territory", "slug": "act", "capital": "Canberra"},
    "TAS": {"name": "Tasmania", "slug": "tas", "capital": "Hobart"},
    "NT": {"name": "Northern Territory", "slug": "nt", "capital": "Darwin"},
}

STATE_SLUG_TO_CODE = {v["slug"]: k for k, v in STATES.items()}


def slugify(text: str) -> str:
    """Standardized slug generator."""
    if not text:
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def get_category_info(sheet_or_slug: str) -> dict:
    """Retrieve category definition by sheet name or slug."""
    if sheet_or_slug in CATEGORIES:
        return CATEGORIES[sheet_or_slug]
    if sheet_or_slug in CATEGORY_SLUG_TO_SHEET:
        sheet = CATEGORY_SLUG_TO_SHEET[sheet_or_slug]
        return CATEGORIES[sheet]
    # Fallback default
    return {
        "slug": slugify(sheet_or_slug),
        "name": sheet_or_slug or "Brokers",
        "short_name": sheet_or_slug or "Brokers",
        "singular": "Broker",
        "schema_type": "LocalBusiness",
        "description": f"Compare verified Australian {sheet_or_slug} brokers and advisers.",
        "icon": "briefcase",
    }


def get_state_info(state_code_or_slug: str) -> dict:
    """Retrieve state definition by code or slug."""
    if not state_code_or_slug:
        return {"name": "Australia", "slug": "au", "capital": "Canberra"}
    code = state_code_or_slug.upper()
    if code in STATES:
        return STATES[code]
    slug = state_code_or_slug.lower()
    if slug in STATE_SLUG_TO_CODE:
        return STATES[STATE_SLUG_TO_CODE[slug]]
    return {"name": state_code_or_slug, "slug": slugify(state_code_or_slug), "capital": ""}


def url_for_home() -> str:
    return "/"


def url_for_category(category_slug: str) -> str:
    return f"/{category_slug}/"


def url_for_state(category_slug: str, state_slug: str) -> str:
    return f"/{category_slug}/{state_slug}/"


def url_for_city(category_slug: str, city_slug: str) -> str:
    return f"/{category_slug}/{city_slug}/"


def url_for_broker(broker_slug: str) -> str:
    return f"/broker/{broker_slug}/"


def url_for_page(page_name: str) -> str:
    slug = slugify(page_name)
    return f"/{slug}/"
