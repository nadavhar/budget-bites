#!/usr/bin/env python3
"""Daily Wolt scanner — finds new restaurants with meals ≤35 NIS and adds them to the DB."""
import json, urllib.request, time, sys
from collections import defaultdict

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Accept-Encoding": "identity",
}

SEARCHES = ["פלאפל", "שווארמה", "חומוס", "פיצה", "סביח", "שניצל", "בורגר", "פיתה"]

CITIES = {
    "תל אביב":     ("tel-aviv",      "32.0853", "34.7818"),
    "ירושלים":     ("jerusalem",     "31.7683", "35.2137"),
    "חיפה":        ("haifa",         "32.7940", "35.5273"),
    "באר שבע":     ("beer-sheva",    "31.2530", "34.7915"),
    "ראשון לציון": ("rishon-lezion", "31.9730", "34.7925"),
    "נתניה":       ("netanya",       "32.3215", "34.8532"),
    "פתח תקווה":  ("petah-tikva",   "32.0840", "34.8878"),
    "אשדוד":       ("ashdod",        "31.8044", "34.6553"),
    "חולון":       ("holon",         "32.0107", "34.7794"),
    "בת ים":       ("bat-yam",       "32.0230", "34.7503"),
}

CITY_EN = {
    "תל אביב": "Tel Aviv", "ירושלים": "Jerusalem", "חיפה": "Haifa",
    "באר שבע": "Beer Sheva", "ראשון לציון": "Rishon LeZion", "נתניה": "Netanya",
    "פתח תקווה": "Petah Tikva", "אשדוד": "Ashdod", "חולון": "Holon", "בת ים": "Bat Yam",
}

REGION_MAP = {
    "תל אביב":     ("תל אביב", "Tel Aviv"),
    "ירושלים":     ("ירושלים", "Jerusalem"),
    "חיפה":        ("צפון", "North"),
    "באר שבע":     ("דרום", "South"),
    "ראשון לציון": ("מרכז", "Center"),
    "נתניה":       ("מרכז", "Center"),
    "פתח תקווה":  ("מרכז", "Center"),
    "אשדוד":       ("דרום", "South"),
    "חולון":       ("תל אביב", "Tel Aviv"),
    "בת ים":       ("תל אביב", "Tel Aviv"),
}

SKIP_VENUES = {"shufersal", "rami-levy", "7-bair", "mega", "victory", "yohananof", "wolt-market"}

SKIP_ITEM_WORDS = [
    'סכו"ם', 'מזלג', 'קוקה', 'קולה', 'ספרייט', 'פאנטה', 'מיץ', 'מים', 'סודה',
    'פחית', 'בקבוק', 'גרם', 'זכוכית', 'cutlery', 'cola', 'sprite', 'fanta',
    'water', 'mineral', 'fuze', 'nesher', 'kinley', 'prigat', 'coca', 'diet',
    'can', 'bottle', 'ביסלי', 'קופסה', 'שקית', 'אריזה', 'מארז', 'zero', 'זירו',
    'חד"פ', '250 מ', '330 מ', '500 מ',
]

MIN_PRICE, MAX_PRICE = 12, 35
DB_PATH = "data/restaurants_i18n.json"


def guess_category(item_name, venue_name):
    s = (item_name + " " + venue_name).lower()
    if "חומוס" in s or "hummus" in s: return {"he": "חומוס", "en": "Hummus"}
    if "פיצה" in s or "pizza" in s:   return {"he": "פיצה", "en": "Pizza"}
    if "בורגר" in s or "burger" in s: return {"he": "בורגר", "en": "Burger"}
    return {"he": "אוכל רחוב", "en": "Street Food"}


def scan_wolt():
    results = []
    seen = set()

    for city_he, (city_slug, lat, lon) in CITIES.items():
        for keyword in SEARCHES:
            payload = json.dumps({"q": keyword, "target": "items", "lat": lat, "lon": lon}).encode()
            req = urllib.request.Request(
                "https://restaurant-api.wolt.com/v1/pages/search",
                data=payload, headers=HEADERS, method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read())
            except Exception as e:
                print(f"  ⚠️  {city_he}/{keyword}: {e}", file=sys.stderr)
                continue

            for section in data.get("sections", []):
                for item in section.get("items", []):
                    link = item.get("link", {}).get("menu_item_details", {})
                    price = link.get("price")
                    if not price:
                        continue
                    price_nis = price / 100 if price > 500 else price
                    venue_slug = link.get("venue_slug", "")
                    venue_name = link.get("venue_name", "")
                    item_name  = link.get("name", "")

                    if any(s in venue_slug for s in SKIP_VENUES):
                        continue
                    if any(w.lower() in item_name.lower() for w in SKIP_ITEM_WORDS):
                        continue
                    if len(item_name) < 4:
                        continue

                    key = (venue_slug, item_name)
                    if key in seen:
                        continue
                    seen.add(key)

                    if MIN_PRICE <= price_nis <= MAX_PRICE:
                        results.append({
                            "city_he": city_he, "city_slug": city_slug,
                            "venue": venue_name, "venue_slug": venue_slug,
                            "item": item_name, "price_nis": price_nis,
                        })

            time.sleep(0.25)

    return results


def main():
    print("🔍 Scanning Wolt…")
    results = scan_wolt()
    print(f"   Found {len(results)} candidate items")

    with open(DB_PATH, encoding="utf-8") as f:
        db = json.load(f)

    existing_lower = set()
    existing_slugs = set()
    for e in db:
        existing_lower.add(e["name"]["he"].strip().lower())
        existing_lower.add(e["name"]["en"].strip().lower())
        if e.get("source_url"):
            # Extract slug from wolt URL
            parts = e["source_url"].rstrip("/").split("/")
            if parts:
                existing_slugs.add(parts[-1])

    # Best item per venue
    by_venue = defaultdict(list)
    for r in results:
        by_venue[(r["venue_slug"], r["city_he"])].append(r)

    max_id = max(int(e["id"]) for e in db)
    added = 0

    for (slug, city_he), items in by_venue.items():
        if slug in existing_slugs:
            continue
        best = min(items, key=lambda x: x["price_nis"])
        venue_lower = best["venue"].lower()
        if any(venue_lower in ex or ex in venue_lower for ex in existing_lower if len(ex) > 4):
            continue

        city_en = CITY_EN[city_he]
        region_he, region_en = REGION_MAP[city_he]
        max_id += 1
        db.append({
            "id": str(max_id),
            "name":      {"he": best["venue"], "en": best["venue"]},
            "dish_name": {"he": best["item"],  "en": best["item"]},
            "price":     int(best["price_nis"]),
            "category":  guess_category(best["item"], best["venue"]),
            "location": {
                "city":    {"he": city_he, "en": city_en},
                "address": {"he": city_he, "en": city_en},
                "region":  {"he": region_he, "en": region_en},
            },
            "kosher_status": {"he": "לא ידוע", "en": "Unknown"},
            "source_url": f"https://wolt.com/isr/{best['city_slug']}/restaurant/{slug}",
            "notes": {
                "he": f"נמצא ב-Wolt. מנה: {best['item']}",
                "en": f"Found on Wolt. Dish: {best['item']}",
            },
            "verified_date": "2026-03",
        })
        existing_slugs.add(slug)
        existing_lower.add(best["venue"].lower())
        added += 1
        print(f"  ✅ [{city_he}] {best['venue']} — {best['item']} {int(best['price_nis'])}₪")

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"\n✨ Added {added} new restaurants. Total: {len(db)}")
    return added


if __name__ == "__main__":
    added = main()
    sys.exit(0 if added >= 0 else 1)
