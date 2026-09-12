"""
JSON-LD Structured Data Generators for Best Brokers Australia.
Implements Blueprint Section 6 (Structured data map).
"""
from typing import Dict, Any, List, Optional
from ..config import SITE_NAME, SITE_URL, SITE_DESCRIPTION, OPERATOR_NAME, OPERATOR_URL
from ..taxonomy import get_category_info, url_for_broker, url_for_category


def organization_schema() -> dict:
    """Master Organization & WebSite structured data."""
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{SITE_URL}/#organization",
                "name": SITE_NAME,
                "url": SITE_URL,
                "logo": f"{SITE_URL}/assets/favicon-32.png",
                "description": SITE_DESCRIPTION,
                "parentOrganization": {
                    "@type": "Organization",
                    "name": OPERATOR_NAME,
                    "url": OPERATOR_URL,
                },
            },
            {
                "@type": "WebSite",
                "@id": f"{SITE_URL}/#website",
                "url": SITE_URL,
                "name": SITE_NAME,
                "publisher": {"@id": f"{SITE_URL}/#organization"},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{SITE_URL}/?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            },
        ],
    }


def hub_collection_schema(hub) -> dict:
    """Generates CollectionPage and ItemList schema for category, state, and city hubs."""
    items = []
    for i, b in enumerate(hub.brokers[:20], 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": b.canonical_url,
            "name": b.name,
        })

    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": hub.h1,
        "description": hub.meta_description,
        "url": hub.canonical_url,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(hub.brokers),
            "itemListElement": items,
        },
    }


def broker_local_business_schema(b) -> dict:
    """Generates LocalBusiness / FinancialService schema for individual broker profiles."""
    cat_info = get_category_info(b.sheet)
    schema_type = cat_info.get("schema_type", "LocalBusiness")

    schema: Dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": b.name,
        "url": b.canonical_url,
        "description": b.about or f"{b.name} is a verified {b.category.lower()} based in {b.display_location}.",
    }

    if b.phone:
        schema["telephone"] = b.phone
    if b.email:
        schema["email"] = b.email
    if b.website:
        schema["sameAs"] = [b.website]

    # Address
    address_obj = {
        "@type": "PostalAddress",
        "addressCountry": "AU",
    }
    if b.address:
        address_obj["streetAddress"] = b.address
    if b.suburb or b.city:
        address_obj["addressLocality"] = b.suburb or b.city
    if b.state:
        address_obj["addressRegion"] = b.state
    if b.postcode:
        address_obj["postalCode"] = b.postcode
    schema["address"] = address_obj

    # Aggregate Rating (only if verified rating exists)
    if b.rating > 0 and b.reviews_count > 0:
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": f"{b.rating:.1f}",
            "reviewCount": b.reviews_count,
            "bestRating": "5",
            "worstRating": "1",
        }

    return schema
