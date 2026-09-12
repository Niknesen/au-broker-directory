"""
Data models and ingestion for Best Brokers Australia.
"""
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from collections import defaultdict
from pathlib import Path

from .config import (
    BROKERS_SOURCE,
    REVIEWS_SOURCE,
    MANUAL_REVIEWS_SOURCE,
    MIN_BROKERS_FOR_CITY_HUB,
    MIN_BROKERS_FOR_SUBURB_HUB,
    SITE_URL,
)
from .taxonomy import (
    CATEGORIES,
    STATES,
    STATE_SLUG_TO_CODE,
    slugify,
    get_category_info,
    get_state_info,
    url_for_home,
    url_for_category,
    url_for_state,
    url_for_city,
    url_for_broker,
)
from .quality import compute_trust_score, compute_quality_score, is_profile_indexable


@dataclass
class Broker:
    id: str
    sheet: str
    name: str
    category: str
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    address: Optional[str]
    suburb: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postcode: Optional[str]
    rating: float
    reviews_count: int
    maps_url: Optional[str]
    place_id: Optional[str]
    about: Optional[str]
    about_source: Optional[str]
    team: List[Any]
    license_disclosed: bool
    license_detail: Optional[str]
    slug: str
    trust_score: int
    quality_score: int
    is_indexable: bool
    category_slug: str
    state_slug: str
    city_slug: str
    suburb_slug: str
    canonical_url: str
    google_reviews: List[dict] = field(default_factory=list)
    manual_reviews: List[dict] = field(default_factory=list)
    case_studies: List[dict] = field(default_factory=list)
    raw_data: dict = field(default_factory=dict)

    @property
    def display_location(self) -> str:
        parts = [self.suburb or self.city, self.state]
        return ", ".join(p for p in parts if p)

    @property
    def display_phone(self) -> str:
        return self.phone or "Available upon request"


@dataclass
class Hub:
    hub_type: str  # 'category', 'state', 'city', 'suburb'
    title: str
    h1: str
    meta_description: str
    canonical_url: str
    category_slug: str
    category_name: str
    category_short: str
    state_code: Optional[str]
    state_name: Optional[str]
    city_name: Optional[str]
    city_slug: Optional[str]
    brokers: List[Broker]
    breadcrumbs: List[dict]
    intro_text: str
    faqs: List[dict]
    sub_locations: List[dict] = field(default_factory=list)
    is_indexable: bool = True


class DirectoryData:
    def __init__(self):
        self.brokers: List[Broker] = []
        self.brokers_by_id: Dict[str, Broker] = {}
        self.brokers_by_slug: Dict[str, Broker] = {}
        
        # Hub collections
        self.category_hubs: Dict[str, Hub] = {}
        self.state_hubs: Dict[str, Hub] = {}  # key: f"{category_slug}/{state_slug}"
        self.city_hubs: Dict[str, Hub] = {}   # key: f"{category_slug}/{city_slug}"
        
        # Index grouping
        self.brokers_by_category: Dict[str, List[Broker]] = defaultdict(list)
        self.brokers_by_category_state: Dict[tuple, List[Broker]] = defaultdict(list)
        self.brokers_by_category_city: Dict[tuple, List[Broker]] = defaultdict(list)
        
        # Stats
        self.total_brokers: int = 0
        self.total_indexable_brokers: int = 0


def load_all_data() -> DirectoryData:
    """Loads all data sources and constructs rich broker and hub models."""
    data = DirectoryData()

    with open(BROKERS_SOURCE, "r", encoding="utf-8") as f:
        raw_brokers = json.load(f)

    reviews_by_place = {}
    if REVIEWS_SOURCE.exists():
        with open(REVIEWS_SOURCE, "r", encoding="utf-8") as f:
            reviews_by_place = json.load(f)

    manual_reviews = {}
    if MANUAL_REVIEWS_SOURCE.exists():
        with open(MANUAL_REVIEWS_SOURCE, "r", encoding="utf-8") as f:
            manual_reviews = json.load(f)

    # Process individual brokers
    for b in raw_brokers:
        b_id = str(b.get("id"))
        name = b.get("name") or "Unnamed Broker"
        sheet = b.get("sheet") or "Mortgage & Finance"
        cat_info = get_category_info(sheet)
        category_slug = cat_info["slug"]
        
        state_code = (b.get("state") or "").upper().strip()
        state_info = get_state_info(state_code)
        state_slug = state_info["slug"]
        
        city = (b.get("city") or b.get("suburb") or "").strip()
        suburb = (b.get("suburb") or "").strip()
        city_slug = slugify(city)
        suburb_slug = slugify(suburb)

        # Build stable slug
        slug = f"{slugify(name)}-{slugify(city or state_code)}-{slugify(b_id)}"
        canonical_url = f"{SITE_URL}{url_for_broker(slug)}"

        # Reviews & Cases
        place_id = b.get("place_id")
        g_reviews = reviews_by_place.get(place_id, []) if place_id else []
        m_reviews = manual_reviews.get(b_id, [])

        # Scores
        trust_score = compute_trust_score(b)
        has_manual_proof = len(m_reviews) > 0 or b.get("case_study") is not None
        quality_score, _ = compute_quality_score(b, len(g_reviews) + len(m_reviews), has_manual_proof)
        indexable = is_profile_indexable(quality_score, b, len(g_reviews) > 0)

        broker_obj = Broker(
            id=b_id,
            sheet=sheet,
            name=name,
            category=b.get("category") or cat_info["singular"],
            phone=b.get("phone"),
            email=b.get("email"),
            website=b.get("website"),
            address=b.get("address"),
            suburb=suburb or None,
            city=city or None,
            state=state_code or None,
            postcode=b.get("postcode"),
            rating=float(b.get("rating") or 0.0),
            reviews_count=int(b.get("reviews") or 0),
            maps_url=b.get("maps_url"),
            place_id=place_id,
            about=b.get("about"),
            about_source=b.get("about_source"),
            team=b.get("team") or [],
            license_disclosed=bool(b.get("license_disclosed")),
            license_detail=b.get("license_detail"),
            slug=slug,
            trust_score=trust_score,
            quality_score=quality_score,
            is_indexable=indexable,
            category_slug=category_slug,
            state_slug=state_slug,
            city_slug=city_slug,
            suburb_slug=suburb_slug,
            canonical_url=canonical_url,
            google_reviews=g_reviews,
            manual_reviews=m_reviews,
            raw_data=b,
        )

        data.brokers.append(broker_obj)
        data.brokers_by_id[b_id] = broker_obj
        data.brokers_by_slug[slug] = broker_obj
        data.brokers_by_category[category_slug].append(broker_obj)
        if state_code:
            data.brokers_by_category_state[(category_slug, state_slug)].append(broker_obj)
        if city_slug:
            data.brokers_by_category_city[(category_slug, city_slug)].append(broker_obj)

    data.total_brokers = len(data.brokers)
    data.total_indexable_brokers = sum(1 for b in data.brokers if b.is_indexable)

    # Sort all broker lists by review count + trust score descending
    for cat_slug in data.brokers_by_category:
        data.brokers_by_category[cat_slug].sort(
            key=lambda b: (len(b.google_reviews) > 0, b.reviews_count, b.trust_score),
            reverse=True,
        )
    for key in data.brokers_by_category_state:
        data.brokers_by_category_state[key].sort(
            key=lambda b: (len(b.google_reviews) > 0, b.reviews_count, b.trust_score),
            reverse=True,
        )
    for key in data.brokers_by_category_city:
        data.brokers_by_category_city[key].sort(
            key=lambda b: (len(b.google_reviews) > 0, b.reviews_count, b.trust_score),
            reverse=True,
        )

    # Construct Hubs
    _build_hubs(data)
    return data


def _build_hubs(data: DirectoryData):
    """Builds category, state, and city hub models."""
    # 1. Category Hubs
    for sheet_name, cat_info in CATEGORIES.items():
        cat_slug = cat_info["slug"]
        cat_brokers = data.brokers_by_category.get(cat_slug, [])
        if not cat_brokers:
            continue

        # Sub-locations: available states
        state_links = []
        for state_code, state_info in STATES.items():
            state_slug = state_info["slug"]
            count = len(data.brokers_by_category_state.get((cat_slug, state_slug), []))
            if count > 0:
                state_links.append({
                    "name": state_info["name"],
                    "code": state_code,
                    "url": url_for_state(cat_slug, state_slug),
                    "count": count,
                })

        # Top city links
        top_cities = []
        city_counts = {}
        for b in cat_brokers:
            if b.city and b.city_slug:
                city_counts[b.city_slug] = (b.city, b.state or "", city_counts.get(b.city_slug, (b.city, b.state, 0))[2] + 1)
        
        for c_slug, (c_name, c_state, count) in sorted(city_counts.items(), key=lambda x: x[1][2], reverse=True)[:18]:
            if count >= MIN_BROKERS_FOR_CITY_HUB:
                top_cities.append({
                    "name": f"{c_name}, {c_state}" if c_state else c_name,
                    "url": url_for_city(cat_slug, c_slug),
                    "count": count,
                })

        title = f"{cat_info['name']} Across Australia | Compare Verified Brokers"
        h1 = f"Compare {cat_info['name']} in Australia"
        meta_desc = (
            f"Browse {len(cat_brokers):,} verified {cat_info['short_name'].lower()} across Australia. "
            f"Compare independent trust scores, real Google reviews, and verified credentials."
        )
        canonical = f"{SITE_URL}{url_for_category(cat_slug)}"

        breadcrumbs = [
            {"name": "Home", "url": url_for_home()},
            {"name": cat_info["short_name"], "url": url_for_category(cat_slug)},
        ]

        faqs = [
            {
                "q": f"How are {cat_info['short_name'].lower()} evaluated on Best Brokers Australia?",
                "a": (
                    f"Every broker profile is independently evaluated using our 3-factor Trust Score methodology: "
                    f"aggregate Google review rating (50%), verified review volume (30%), and public regulatory / "
                    f"licence disclosure on their official site (20%). We do not accept payment to alter rankings."
                ),
            },
            {
                "q": f"How much does it cost to use an Australian {cat_info['singular'].lower()}?",
                "a": (
                    f"Most mortgage and finance brokers in Australia do not charge upfront borrower fees, as they are "
                    f"remunerated by the lender upon loan settlement. For insurance and commercial services, fee "
                    f"structures vary and must be disclosed upfront in a Financial Services Guide (FSG)."
                ),
            },
            {
                "q": f"How do I verify if a {cat_info['singular'].lower()} is licensed in Australia?",
                "a": (
                    f"All credit representatives and Australian Credit License (ACL) or Australian Financial Services "
                    f"License (AFSL) holders are registered on ASIC's professional registers. Look for their licence "
                    f"number on their profile card or official website."
                ),
            },
        ]

        hub = Hub(
            hub_type="category",
            title=title,
            h1=h1,
            meta_description=meta_desc,
            canonical_url=canonical,
            category_slug=cat_slug,
            category_name=cat_info["name"],
            category_short=cat_info["short_name"],
            state_code=None,
            state_name=None,
            city_name=None,
            city_slug=None,
            brokers=cat_brokers,
            breadcrumbs=breadcrumbs,
            intro_text=cat_info["description"],
            faqs=faqs,
            sub_locations=state_links,
            is_indexable=True,
        )
        data.category_hubs[cat_slug] = hub

    # 2. State Hubs
    for (cat_slug, state_slug), st_brokers in data.brokers_by_category_state.items():
        if not st_brokers:
            continue
        cat_info = get_category_info(cat_slug)
        state_code = STATE_SLUG_TO_CODE.get(state_slug, state_slug.upper())
        state_info = STATES.get(state_code, {"name": state_code, "capital": ""})

        # Top city links in this state
        city_counts = {}
        for b in st_brokers:
            if b.city and b.city_slug:
                city_counts[b.city_slug] = (b.city, city_counts.get(b.city_slug, (b.city, 0))[1] + 1)

        city_links = []
        for c_slug, (c_name, count) in sorted(city_counts.items(), key=lambda x: x[1][1], reverse=True):
            if count >= MIN_BROKERS_FOR_CITY_HUB:
                city_links.append({
                    "name": c_name,
                    "url": url_for_city(cat_slug, c_slug),
                    "count": count,
                })

        title = f"{cat_info['name']} in {state_info['name']} ({state_code}) | Best Brokers Australia"
        h1 = f"{cat_info['short_name']} in {state_info['name']}"
        meta_desc = (
            f"Find & compare {len(st_brokers):,} top-rated {cat_info['short_name'].lower()} across "
            f"{state_info['name']}. Verified trust scores, local client reviews, and direct contact details."
        )
        canonical = f"{SITE_URL}{url_for_state(cat_slug, state_slug)}"

        breadcrumbs = [
            {"name": "Home", "url": url_for_home()},
            {"name": cat_info["short_name"], "url": url_for_category(cat_slug)},
            {"name": state_code, "url": url_for_state(cat_slug, state_slug)},
        ]

        faqs = [
            {
                "q": f"How many {cat_info['short_name'].lower()} are reviewed in {state_info['name']}?",
                "a": f"We currently track and score {len(st_brokers):,} independent {cat_info['short_name'].lower()} operating across {state_info['name']}.",
            },
            {
                "q": f"What should I look for when hiring a {cat_info['singular'].lower()} in {state_info['name']}?",
                "a": f"Verify their ASIC licence or Credit Representative status, check their independent Trust Score, read local client feedback, and ensure they have experience with property and lending conditions in {state_info['name']}.",
            },
        ]

        hub = Hub(
            hub_type="state",
            title=title,
            h1=h1,
            meta_description=meta_desc,
            canonical_url=canonical,
            category_slug=cat_slug,
            category_name=cat_info["name"],
            category_short=cat_info["short_name"],
            state_code=state_code,
            state_name=state_info["name"],
            city_name=None,
            city_slug=None,
            brokers=st_brokers,
            breadcrumbs=breadcrumbs,
            intro_text=f"Explore verified {cat_info['name'].lower()} serving clients across {state_info['name']}. Compare local ratings, client reviews, and independent trust scores.",
            faqs=faqs,
            sub_locations=city_links,
            is_indexable=len(st_brokers) >= 5,
        )
        data.state_hubs[f"{cat_slug}/{state_slug}"] = hub

    # 3. City Hubs
    for (cat_slug, city_slug), c_brokers in data.brokers_by_category_city.items():
        if len(c_brokers) < MIN_BROKERS_FOR_CITY_HUB:
            continue
        cat_info = get_category_info(cat_slug)
        sample_b = c_brokers[0]
        city_name = sample_b.city or city_slug.replace("-", " ").title()
        state_code = sample_b.state or ""
        state_slug = sample_b.state_slug or "nsw"
        state_name = STATES.get(state_code, {}).get("name", state_code)

        title = f"{cat_info['short_name']} in {city_name}, {state_code} | Compare Local Brokers"
        h1 = f"{cat_info['short_name']} in {city_name}"
        meta_desc = (
            f"Compare {len(c_brokers):,} verified {cat_info['short_name'].lower()} in {city_name}, {state_code}. "
            f"Independent trust scores, genuine client reviews, and local market expertise."
        )
        canonical = f"{SITE_URL}{url_for_city(cat_slug, city_slug)}"

        breadcrumbs = [
            {"name": "Home", "url": url_for_home()},
            {"name": cat_info["short_name"], "url": url_for_category(cat_slug)},
        ]
        if state_code:
            breadcrumbs.append({"name": state_code, "url": url_for_state(cat_slug, state_slug)})
        breadcrumbs.append({"name": city_name, "url": url_for_city(cat_slug, city_slug)})

        # Nearby cities in the same state
        nearby_cities = []
        if state_code:
            st_key = (cat_slug, state_slug)
            st_all = data.brokers_by_category_state.get(st_key, [])
            st_city_counts = defaultdict(int)
            st_city_names = {}
            for b in st_all:
                if b.city_slug and b.city_slug != city_slug:
                    st_city_counts[b.city_slug] += 1
                    st_city_names[b.city_slug] = b.city

            for n_slug, count in sorted(st_city_counts.items(), key=lambda x: x[1], reverse=True)[:8]:
                if count >= MIN_BROKERS_FOR_CITY_HUB:
                    nearby_cities.append({
                        "name": st_city_names.get(n_slug, n_slug.replace("-", " ").title()),
                        "url": url_for_city(cat_slug, n_slug),
                        "count": count,
                    })

        faqs = [
            {
                "q": f"How many {cat_info['short_name'].lower()} are located in {city_name}?",
                "a": f"There are currently {len(c_brokers):,} verified {cat_info['short_name'].lower()} profiled in {city_name}, {state_code} on Best Brokers Australia.",
            },
            {
                "q": f"Who is the highest rated {cat_info['singular'].lower()} in {city_name}?",
                "a": (
                    f"Rankings in {city_name} are determined objectively by our Trust Score, which combines verified Google "
                    f"review volume, average rating, and public regulatory disclosures. Check the comparison cards above to "
                    f"view the top-ranked local specialists."
                ),
            },
            {
                "q": f"Do {city_name} brokers assist with local property & market requirements?",
                "a": (
                    f"Yes, local {city_name} brokers have specialized knowledge of lending policies, local council requirements, "
                    f"and regional property valuation trends across {city_name} and surrounding areas."
                ),
            },
        ]

        # Quality gate: only index city hubs with at least MIN_BROKERS_FOR_CITY_HUB (5) brokers
        is_index = len(c_brokers) >= MIN_BROKERS_FOR_CITY_HUB

        hub = Hub(
            hub_type="city",
            title=title,
            h1=h1,
            meta_description=meta_desc,
            canonical_url=canonical,
            category_slug=cat_slug,
            category_name=cat_info["name"],
            category_short=cat_info["short_name"],
            state_code=state_code,
            state_name=state_name,
            city_name=city_name,
            city_slug=city_slug,
            brokers=c_brokers,
            breadcrumbs=breadcrumbs,
            intro_text=(
                f"Compare {len(c_brokers):,} top-rated {cat_info['short_name'].lower()} in {city_name}, {state_code}. "
                f"Every profile features an independently computed Trust Score, real client reviews, and direct contact details."
            ),
            faqs=faqs,
            sub_locations=nearby_cities,
            is_indexable=is_index,
        )
        data.city_hubs[f"{cat_slug}/{city_slug}"] = hub
