#!/usr/bin/env python3
"""Transform flat restaurant data into bilingual schema."""
import json
import re

# Category translations
CATEGORIES = {
    "Street Food": "אוכל רחוב",
    "Burger": "המבורגר",
    "Pizza": "פיצה",
    "Italian": "איטלקי",
    "Bakery": "מאפייה",
    "Hummus": "חומוס",
    "Asian": "אסייתי",
    "Grill": "גריל",
    "Cafe / Quick Bite": "בית קפה / ביס מהיר",
    "Mexican": "מקסיקני",
    "Yemenite": "תימני",
    "Dessert": "קינוח",
}

# Region translations
REGIONS = {
    "Tel Aviv": "תל אביב",
    "Jerusalem": "ירושלים",
    "Center": "מרכז",
    "North": "צפון",
    "South": "דרום",
    "National": "ארצי",
}

# City translations
CITIES = {
    "Tel Aviv": "תל אביב",
    "Jerusalem": "ירושלים",
    "Haifa": "חיפה",
    "Eilat": "אילת",
    "Beer Sheva": "באר שבע",
    "Ramat Gan": "רמת גן",
    "Petah Tikva": "פתח תקווה",
    "Rishon LeZion": "ראשון לציון",
    "Netanya": "נתניה",
    "Nazareth": "נצרת",
    "Acre (Akko)": "עכו",
    "Bnei Brak": "בני ברק",
    "Kafr Qasim": "כפר קאסם",
    "Jaffa (Tel Aviv-Yafo)": "יפו",
    "National": "ארצי",
}

# Kosher translations
KOSHER = {
    "Kosher": "כשר",
    "Kosher Mehadrin": "כשר למהדרין",
    "Not Kosher": "לא כשר",
    "Unknown": "לא ידוע",
}


def split_name(name):
    """Split 'English / עברית' format into (en, he)."""
    if " / " in name:
        parts = name.split(" / ", 1)
        # Detect which part is Hebrew
        if any("\u0590" <= c <= "\u05FF" for c in parts[1]):
            return parts[0].strip(), parts[1].strip()
        else:
            return parts[1].strip(), parts[0].strip()
    # All Hebrew
    if any("\u0590" <= c <= "\u05FF" for c in name):
        return name, name
    # All English
    return name, name


def transliterate_dish(dish_en):
    """Keep English dish names as-is, they're descriptive enough."""
    return dish_en


def transform(entry):
    en_name, he_name = split_name(entry["restaurant_name"])

    # For dish names - keep English, generate Hebrew where possible
    dish_en = entry["dish_name"]
    dish_he = entry["dish_name"]  # Fallback to same

    # Common dish translations
    DISH_MAP = {
        "Falafel in Pita": "פלאפל בפיתה",
        "Falafel in Pita with Salads & Chips": "פלאפל בפיתה עם סלטים וצ'יפס",
        "Sabich": "סביח",
        "Sabich in Pita": "סביח בפיתה",
        "Sabich Wrap": "סביח בלאפה",
        "Sabich Half Portion": "חצי מנה סביח",
        "Half Portion Sabich": "חצי מנה סביח",
        "Hummus Plate": "מנת חומוס",
        "Hummus / Ful Plate": "מנת חומוס / פול",
        "Half Portion Hummus Plate": "חצי מנה חומוס",
        "Hummus with Ful": "חומוס עם פול",
        "Shawarma in Pita": "שווארמה בפיתה",
        "Shawarma (lamb & beef)": "שווארמה (כבש ובקר)",
        "Large Pizza Slice": "משולש פיצה גדול",
        "Pizza Slice (plain)": "משולש פיצה (רגיל)",
        "Quarter Pan Pizza": "רבע מגש פיצה",
        "Family Pizza Pan": "מגש פיצה משפחתי",
        "NY-Style Pizza Slice": "משולש פיצה ניו יורקי",
        "Pizza Tray": "מגש פיצה",
        "Pizza": "פיצה",
        "Mini Rib Entrecote Burger": "מיני בורגר אנטריקוט",
        "Pair of Mini Burgers (beef or lamb)": "זוג מיני בורגרס (בקר או כבש)",
        "Slider / Mini Burger": "סליידר / מיני בורגר",
        "Pasta (250ml)": "פסטה (250 מ\"ל)",
        "Turkish Burekas": "בורקס טורקי",
        "Turkish / Spanish Burekas": "בורקס טורקי / ספרדי",
        "Burekas": "בורקס",
        "Burekas (Kashkaval/Bulgarian/Spinach/Potato)": "בורקס (קשקבל/בולגרי/תרד/תפוח אדמה)",
        "Turkish Baked Goods / Burekas": "מאפים טורקיים / בורקס",
        "Two Pastries": "שני מאפים",
        "Turkish Pastry": "מאפה טורקי",
        "Fried Sambousak": "סמבוסק מטוגן",
        "Potato Kuba in Pita": "קובה תפוח אדמה בפיתה",
        "Meat Kuba": "קובה בשרית",
        "Hot Prepared Dishes (Asian)": "מנות אסייתיות חמות",
        "Skewer (chicken/kebab/liver/hearts)": "שיפוד (עוף/קבב/כבד/לבבות)",
        "Grilled Meat Skewer": "שיפוד בשר על הגריל",
        "Sausage with Coleslaw & Mustard": "נקניקייה עם קולסלו וחרדל",
        "Schnitzel in Pita": "שניצל בפיתה",
        "Katsu Sandwich": "כריך קאטסו",
        "Vegetable Noodles": "נודלס ירקות",
        "Ramen Bowl": "קערת ראמן",
        "Dumplings": "כיסוני בצק (דאמפלינגס)",
        "Steamed Bao Bun (beef/veggie)": "באו מאודה (בקר/ירקות)",
        "Soup Bowl": "קערת מרק",
        "Sandwich / Focaccia / Omelet": "כריך / פוקצ'ה / חביתה",
        "Hand-made Empanada": "אמפנדה בעבודת יד",
        "Taco": "טאקו",
        "Jachnun with Tomato & Schug": "ג'חנון עם עגבנייה ושחוג",
        "Falafel Balls Plate": "צלחת כדורי פלאפל",
        "Fresh Pita / Zaatar Bread": "פיתה טרייה / לחם זעתר",
        "Cloud Pita Meal": "ארוחת פיתה ענן",
        "Fish Shawarma Wrap": "שווארמת דגים בלאפה",
        "Jerusalem Mixed Grill (Meorav Yerushalmi)": "מעורב ירושלמי",
        "Falafel Kinder (giant falafel ball with egg inside)": "פלאפל קינדר (כדור ענק עם ביצה)",
        "Falafel Plate": "מנת פלאפל",
        "Knafeh Portion": "מנת כנאפה",
        "Spinach Burekas with Coffee": "בורקס תרד עם קפה",
    }

    dish_he = DISH_MAP.get(dish_en, dish_en)

    city_en = entry["location"]["city"]
    city_he = CITIES.get(city_en, city_en)

    region_en = entry["location"]["region"]
    region_he = REGIONS.get(region_en, region_en)

    cat_en = entry["category"]
    cat_he = CATEGORIES.get(cat_en, cat_en)

    kosher_en = entry["kosher_status"]
    kosher_he = KOSHER.get(kosher_en, kosher_en)

    # Notes translation - keep as-is (mixed content)
    notes_en = entry.get("notes") or ""
    notes_he = notes_en  # fallback

    return {
        "id": None,  # will be set later
        "name": {"he": he_name, "en": en_name},
        "dish_name": {"he": dish_he, "en": dish_en},
        "price": entry["price"],
        "category": {"he": cat_he, "en": cat_en},
        "location": {
            "city": {"he": city_he, "en": city_en},
            "address": {"he": entry["location"]["address"], "en": entry["location"]["address"]},
            "region": {"he": region_he, "en": region_en},
        },
        "kosher_status": {"he": kosher_he, "en": kosher_en},
        "source_url": entry.get("source_url", ""),
        "verified_date": entry.get("verified_date", ""),
        "notes": {"he": notes_he, "en": notes_en} if notes_en else None,
    }


def main():
    with open("data/restaurants.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed = []
    for i, entry in enumerate(data, 1):
        t = transform(entry)
        t["id"] = str(i)
        transformed.append(t)

    with open("data/restaurants_i18n.json", "w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)

    print(f"Transformed {len(transformed)} entries -> data/restaurants_i18n.json")


if __name__ == "__main__":
    main()
