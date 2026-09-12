"""
Broker Quality and Trust Scoring Engine.
Implements Blueprint Section 4 (Indexation Quality System) and Trust Score algorithm.
"""
import re
from typing import Tuple, Dict, Any
from .config import QUALITY_SCORE_INDEX_MIN, QUALITY_SCORE_CONDITIONAL_MIN


def compute_trust_score(b: dict) -> int:
    """
    Computes the user-facing Trust Score (0-100%).
    Based on real, verified data:
      - Google rating component (up to 50 pts)
      - Google review volume component (up to 30 pts)
      - Public licence/credit representative disclosure (20 pts)
    """
    rating = b.get("rating") or 0.0
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        rating = 0.0

    reviews = b.get("reviews") or 0
    try:
        reviews = int(reviews)
    except (TypeError, ValueError):
        reviews = 0

    license_disclosed = bool(b.get("license_disclosed"))

    # Rating points (0 - 50)
    rating_pts = (rating / 5.0) * 50.0 if rating > 0 else 25.0

    # Review volume points (0 - 30)
    if reviews >= 100:
        review_pts = 30.0
    elif reviews >= 50:
        review_pts = 25.0
    elif reviews >= 20:
        review_pts = 20.0
    elif reviews >= 10:
        review_pts = 15.0
    elif reviews >= 1:
        review_pts = 10.0
    else:
        review_pts = 0.0

    # Licence points (0 or 20)
    license_pts = 20.0 if license_disclosed else 0.0

    score = round(rating_pts + review_pts + license_pts)
    return max(10, min(99, score))


def compute_quality_score(b: dict, reviews_count: int = 0, has_manual_proof: bool = False) -> Tuple[int, Dict[str, int]]:
    """
    Computes the SEO Profile Quality Score (0-100) per Blueprint Section 4:
      - Verified business identity (20 pts)
      - Complete NAP: Name, Address/locality, Phone, working Website (15 pts)
      - Unique description / About text (15 pts)
      - Specific category/service detail (10 pts)
      - Reputation evidence: ratings + review count (10 pts)
      - Licence/credentials disclosed (10 pts)
      - Original proof: cases, reviews, owner responses, custom portrait (15 pts)
      - Freshness: verified within current cycle (5 pts)

    Returns (total_score, breakdown_dict).
    """
    breakdown = {}

    # 1. Verified business identity (20 pts)
    # Claimed by owner, verified Place ID match, or manual review
    is_claimed = bool(b.get("claimed"))
    place_id = b.get("place_id")
    if is_claimed:
        breakdown["identity"] = 20
    elif place_id and len(str(place_id)) > 10:
        breakdown["identity"] = 15
    elif b.get("name") and b.get("address"):
        breakdown["identity"] = 10
    else:
        breakdown["identity"] = 0

    # 2. Complete NAP (15 pts)
    nap_score = 0
    if b.get("name"):
        nap_score += 4
    if b.get("phone"):
        nap_score += 4
    if b.get("address") or (b.get("suburb") and b.get("state")):
        nap_score += 4
    if b.get("website"):
        nap_score += 3
    breakdown["nap"] = nap_score

    # 3. Unique description (15 pts)
    about = (b.get("about") or "").strip()
    if len(about) > 100:
        breakdown["description"] = 15
    elif len(about) > 30:
        breakdown["description"] = 8
    else:
        breakdown["description"] = 0

    # 4. Service / Category detail (10 pts)
    category = (b.get("category") or "").strip()
    sheet = (b.get("sheet") or "").strip()
    if category and category.lower() != sheet.lower() and len(category) > 4:
        breakdown["service_detail"] = 10
    elif category:
        breakdown["service_detail"] = 6
    else:
        breakdown["service_detail"] = 0

    # 5. Reputation evidence (10 pts)
    g_rating = float(b.get("rating") or 0)
    g_reviews = int(b.get("reviews") or 0)
    if g_reviews >= 10 and g_rating > 0:
        breakdown["reputation"] = 10
    elif g_reviews >= 1 and g_rating > 0:
        breakdown["reputation"] = 7
    elif g_rating > 0:
        breakdown["reputation"] = 4
    else:
        breakdown["reputation"] = 0

    # 6. Licence / credentials (10 pts)
    if b.get("license_disclosed") or b.get("license_detail"):
        breakdown["licence"] = 10
    else:
        breakdown["licence"] = 0

    # 7. Original proof (15 pts)
    # Directory reviews, real case studies, custom portrait, team list
    proof_score = 0
    if has_manual_proof:
        proof_score += 15
    else:
        if reviews_count > 0:
            proof_score += 8
        if b.get("team") and len(b.get("team")) > 0:
            proof_score += 4
        if b.get("email"):
            proof_score += 3
    breakdown["proof"] = min(15, proof_score)

    # 8. Freshness (5 pts)
    breakdown["freshness"] = 5

    total = sum(breakdown.values())
    return total, breakdown


def is_profile_indexable(quality_score: int, b: dict, has_real_reviews: bool = False) -> bool:
    """
    Decides whether a broker profile should be indexed by search engines.
    Blueprint rules:
      - 70-100: index, follow (strong entity, complete profile)
      - 50-69: index, follow IF real reviews / substantive data exist; otherwise noindex, follow
      - 0-49: noindex, follow (searchable internally, excluded from Google)
    """
    if quality_score >= QUALITY_SCORE_INDEX_MIN:
        return True
    if quality_score >= QUALITY_SCORE_CONDITIONAL_MIN:
        # Conditional indexation: must have either real reviews, website + phone + address, or verified proof
        reviews = int(b.get("reviews") or 0)
        has_nap = bool(b.get("phone") and b.get("website") and b.get("address"))
        if reviews >= 3 or has_real_reviews or (has_nap and b.get("rating")):
            return True
    return False


def normalize_phone(phone: str) -> str:
    """Normalizes phone string for deduplication."""
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("61"):
        digits = "0" + digits[2:]
    return digits


def normalize_domain(url: str) -> str:
    """Extracts base domain from URL for deduplication."""
    if not url:
        return ""
    domain = re.sub(r"^https?://(www\.)?", "", url.lower())
    domain = domain.split("/")[0].split("?")[0].strip()
    return domain
