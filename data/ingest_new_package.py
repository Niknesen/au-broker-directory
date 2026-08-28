#!/usr/bin/env python3
"""
One-off ingestion of the new, deduped broker package (16,771 unique
businesses, matched by Google Place ID - a hard dedup key the previous
~12,148-row dataset never had, which is why it turned out to be only ~5,620
truly unique records under the hood).

Replaces data/all_brokers_full.json entirely - this new file supersedes the
old one, it does not merge with it (merging would risk reintroducing the
duplicates this package was built to remove).

What this does NOT do, and why:
  - Does not import review text. Every row in the source workbook's Reviews
    sheet has Review Text/Original Text == "[object Object]" (a scraper bug
    that serialized a JS object instead of its string) or null - 100% of
    22,189 review rows are unusable. Only the aggregate Rating/Reviews count
    on the Brokers sheet is real and gets used (same as before).
  - Does not carry over the old `about` text. The old dataset had no stable
    join key (no Place ID) to match old rows to new ones reliably, and only
    a minority of old rows had `about` populated anyway. Every row here
    gets about=None, same fallback behaviour the site already handles.
  - Drops CLOSED_PERMANENTLY / CLOSED_TEMPORARILY rows and the ~59 rows
    (0.35%) whose Address doesn't parse as a real AU address (a few are
    literally overseas places from a bad geocode match).
"""
import json
import re
from collections import Counter
from pathlib import Path

import openpyxl

ROOT = Path(__file__).parent
SOURCE_XLSX = Path("/Users/nick/Downloads/ALL BROKERS/final-australian-broker-package.xlsx")
OUT = ROOT / "all_brokers_full.json"

ADDR_RE = re.compile(r"([A-Za-z0-9 '\.-]+?)\s+(NSW|VIC|QLD|WA|SA|TAS|ACT|NT)\s+(\d{4})")

# Our 7-bucket taxonomy the site already uses (category chips, page copy).
# Rows from the "original" 5,620 already carry one of these exact names in
# the Industry column. Rows from the "expansion" 11,151 only carry raw
# Google Places types (Category column, pipe-delimited) - map those.
BUCKETS = [
    "Mortgage & Finance",
    "Insurance",
    "Real Estate & Buyers",
    "Business Sales & Franchise",
    "Asset & Equipment Finance",
    "Customs & Freight",
    "Wealth & Investment",
]

FRIENDLY_TYPE = {
    "real_estate_agency": "Real estate agency",
    "insurance_agency": "Insurance agency",
    "accounting": "Accounting firm",
    "finance": "Finance broker",
    "consultant": "Finance broker",
}


def bucket_from_google_types(raw_category):
    tokens = {t.strip() for t in (raw_category or "").split("|")}
    if "real_estate_agency" in tokens:
        return "Real Estate & Buyers", "Real estate agency"
    if "insurance_agency" in tokens:
        return "Insurance", "Insurance agency"
    if "accounting" in tokens:
        return "Wealth & Investment", "Accounting firm"
    return "Mortgage & Finance", "Finance broker"


def parse_address(address):
    m = ADDR_RE.search(address or "")
    if not m:
        return None
    suburb, state, postcode = m.groups()
    suburb = suburb.split(",")[-1].strip(" ,")
    return suburb, state, postcode


def first_email(raw):
    if not raw:
        return None
    return raw.split(";")[0].strip() or None


def main():
    wb = openpyxl.load_workbook(SOURCE_XLSX, read_only=True, data_only=True)
    ws = wb["Brokers"]
    it = ws.iter_rows(values_only=True)
    header = list(next(it))
    idx = {name: i for i, name in enumerate(header)}

    dropped_closed = 0
    dropped_bad_address = 0
    bucket_counts = Counter()
    out = []

    for row in it:
        status = row[idx["Business Status"]]
        if status in ("CLOSED_PERMANENTLY", "CLOSED_TEMPORARILY"):
            dropped_closed += 1
            continue

        address = row[idx["Address"]]
        parsed = parse_address(address)
        if not parsed:
            dropped_bad_address += 1
            continue
        suburb, state, postcode = parsed

        industry = row[idx["Industry"]]
        raw_category = row[idx["Category"]]
        if industry in BUCKETS:
            sheet = industry
            category_label = raw_category or industry
        else:
            sheet, category_label = bucket_from_google_types(raw_category)

        bucket_counts[sheet] += 1
        n = bucket_counts[sheet]

        out.append({
            "id": f"{sheet}-{n}",
            "sheet": sheet,
            "name": row[idx["Business"]],
            "category": category_label,
            "phone": row[idx["Phone"]],
            "email": first_email(row[idx["Public Email"]]),
            "website": row[idx["Website URL"]],
            "address": address,
            "suburb": suburb,
            "city": suburb,
            "state": state,
            "postcode": postcode,
            "rating": row[idx["Rating"]],
            "reviews": row[idx["Reviews"]] or 0,
            "maps_url": row[idx["Google Maps URL"]],
            "about": None,
            "about_source": None,
            "team": [],
            "license_disclosed": False,
            "license_detail": None,
        })

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(out)} brokers to {OUT}")
    print(f"Dropped: {dropped_closed} closed, {dropped_bad_address} bad address")
    for name, count in bucket_counts.most_common():
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
