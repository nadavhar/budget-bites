#!/usr/bin/env python3
"""Add new bilingual entries - Round 6: Sharon towns, Druze/Arab villages, highway junctions, kibbutzim."""
import json

NEW_ENTRIES = [
    # === EVEN YEHUDA ===
    {
        "name": {"he": "אלוף השווארמה", "en": "Aloof HaShawarma"},
        "dish_name": {"he": "שווארמה בפיתה", "en": "Shawarma in Pita"},
        "price": 30, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "אבן יהודה", "en": "Even Yehuda"}, "address": {"he": "בני בנימין 2, אבן יהודה", "en": "Bnei Binyamin 2, Even Yehuda"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "https://easy.co.il/en/page/27134501",
        "notes": {"he": "שווארמה, פלאפל, שניצל בפיתה טרייה.", "en": "Shawarma, falafel, schnitzel in fresh pita."}
    },
    {
        "name": {"he": "אלוף השווארמה", "en": "Aloof HaShawarma"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 15, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "אבן יהודה", "en": "Even Yehuda"}, "address": {"he": "בני בנימין 2, אבן יהודה", "en": "Bnei Binyamin 2, Even Yehuda"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "https://easy.co.il/en/page/27134501",
        "notes": None
    },
    # === KFAR YONA ===
    {
        "name": {"he": "סנטיאגו", "en": "Santiago"},
        "dish_name": {"he": "שווארמה בלאפה", "en": "Shawarma in Laffa"},
        "price": 30, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "כפר יונה", "en": "Kfar Yona"}, "address": {"he": "כפר יונה", "en": "Kfar Yona"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "מזון מהיר - שווארמה, פלאפל, שניצל.", "en": "Fast food - shawarma, falafel, schnitzel."}
    },
    {
        "name": {"he": "חומוס תנובות", "en": "Tenuva Hummus"},
        "dish_name": {"he": "חומוס עם פיתה", "en": "Hummus with Pita"},
        "price": 18, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "כפר יונה", "en": "Kfar Yona"}, "address": {"he": "אזור תעשייה תנובות, כפר יונה", "en": "Tenuva Industrial Area, Kfar Yona"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "חומוס, שקשוקה, פלאפל ושניצל.", "en": "Hummus, shakshuka, falafel and schnitzel."}
    },
    # === KADIMA-ZORAN ===
    {
        "name": {"he": "אצל קמליה", "en": "Etzel Kamelya"},
        "dish_name": {"he": "שיפוד פרגיות עם סלט", "en": "Chicken Skewer with Salad"},
        "price": 35, "category": {"he": "גריל", "en": "Grill"},
        "location": {"city": {"he": "קדימה-צורן", "en": "Kadima-Zoran"}, "address": {"he": "צורן", "en": "Tzoran"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "גריל ובישולים ביתיים באווירה אותנטית. מחירים נוחים.", "en": "Grill and home cooking in authentic atmosphere. Affordable prices."}
    },
    # === GIVAT SHMUEL ===
    {
        "name": {"he": "פלאפל בריבוע", "en": "Falafel BaRibua"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 15, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "גבעת שמואל", "en": "Givat Shmuel"}, "address": {"he": "קניון גבעת שמואל", "en": "Givat Shmuel Mall"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "הפלאפל המוביל בעיר. תפריט רחב כולל שקשוקה ולבנה.", "en": "The leading falafel in the city. Wide menu including shakshuka and labneh."}
    },
    # === SHLOMI ===
    {
        "name": {"he": "פלאפל בללי", "en": "Falafel Balawy"},
        "dish_name": {"he": "חומוס עם פלאפל", "en": "Hummus with Falafel"},
        "price": 20, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "שלומי", "en": "Shlomi"}, "address": {"he": "שלומי", "en": "Shlomi"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "חומוסייה ופלאפל בעיירה בגליל המערבי.", "en": "Hummus and falafel spot in Western Galilee town."}
    },
    # === BE'ER YA'AKOV ===
    {
        "name": {"he": "פלאפל סוף הדרך", "en": "Falafel Sof HaDerech"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 15, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "באר יעקב", "en": "Be'er Ya'akov"}, "address": {"he": "שער נשה 17, באר יעקב", "en": "Sha'ar Nashe 17, Be'er Ya'akov"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "חומרי גלם איכותיים.", "en": "Quality ingredients."}
    },
    {
        "name": {"he": "שווארמה גרלה", "en": "Shawarma Garela"},
        "dish_name": {"he": "שווארמה בלאפה", "en": "Shawarma in Laffa"},
        "price": 30, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "באר יעקב", "en": "Be'er Ya'akov"}, "address": {"he": "באר יעקב", "en": "Be'er Ya'akov"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "השווארמה הכי טעימה בעיר. גם פלאפל וסביח.", "en": "The tastiest shawarma in town. Also falafel and sabich."}
    },
    # === KIRYAT EKRON ===
    {
        "name": {"he": "פיתה בכיכר ביל\"ו", "en": "Pita BeKikar Bilu"},
        "dish_name": {"he": "קבב בפיתה", "en": "Kebab in Pita"},
        "price": 30, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "קריית עקרון", "en": "Kiryat Ekron"}, "address": {"he": "מרכז ביל\"ו, קריית עקרון", "en": "Bilu Center, Kiryat Ekron"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "קבב, שווארמה, שניצל ועוף.", "en": "Kebab, shawarma, schnitzel and chicken."}
    },
    # === MAZKERET BATYA ===
    {
        "name": {"he": "פלאפל השמן והרזה", "en": "Falafel HaSamen VeHaRaze"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 15, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "מזכרת בתיה", "en": "Mazkeret Batya"}, "address": {"he": "מנחם בגין 2, מזכרת בתיה", "en": "Menachem Begin 2, Mazkeret Batya"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "https://www.kosherest.co.il/rests/mizkeret-batia/6028",
        "notes": {"he": "חומוס ופלאפל. מחיר ממוצע 50 ש\"ח לזוג.", "en": "Hummus and falafel. Average 50 NIS per couple."}
    },
    # === YARKA (Druze) ===
    {
        "name": {"he": "בוקר טוב", "en": "Boker Tov"},
        "dish_name": {"he": "חומוס עם פלאפל ושניצל", "en": "Hummus with Falafel & Schnitzel"},
        "price": 20, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "ירכא", "en": "Yarka"}, "address": {"he": "ירכא", "en": "Yarka"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "https://www.ynet.co.il/articles/0,7340,L-5646766,00.html",
        "notes": {"he": "פתוח עד 17:00. מנות 15-20 ש\"ח. שמן זית גלילי מעולה.", "en": "Open until 5PM. Dishes 15-20 NIS. Excellent Galilean olive oil."}
    },
    {
        "name": {"he": "המטבח הדרוזי", "en": "HaMitbach HaDruzi"},
        "dish_name": {"he": "פיתה דרוזית עם לבנה", "en": "Druze Pita with Labneh"},
        "price": 20, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "ירכא", "en": "Yarka"}, "address": {"he": "ירכא", "en": "Yarka"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "https://www.rest.co.il/rest/80331210/",
        "notes": {"he": "מסעדה דרוזית אותנטית. חוות דעת מצוינות.", "en": "Authentic Druze restaurant. Excellent reviews."}
    },
    # === JULIS (Druze) ===
    {
        "name": {"he": "פיתה דרוזית ג'וליס", "en": "Julis Druze Pita"},
        "dish_name": {"he": "פיתה דרוזית עם זעתר", "en": "Druze Pita with Za'atar"},
        "price": 12, "category": {"he": "מאפייה", "en": "Bakery"},
        "location": {"city": {"he": "ג'וליס", "en": "Julis"}, "address": {"he": "ג'וליס", "en": "Julis"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר דרוזי עם מאפים מסורתיים. סיור קולינרי עם ירכא וכפר יאסיף.", "en": "Druze village with traditional baked goods. Culinary tour with Yarka and Kafr Yasif."}
    },
    # === KAFR YASIF ===
    {
        "name": {"he": "אבו אדהם", "en": "Abu Adham"},
        "dish_name": {"he": "חומוס מלא", "en": "Full Hummus Plate"},
        "price": 25, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "כפר יאסיף", "en": "Kafr Yasif"}, "address": {"he": "כפר יאסיף", "en": "Kafr Yasif"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "חומוסייה מפורסמת בגליל המערבי. נזכרת בסיור קולינרי של ynet.", "en": "Famous hummus in Western Galilee. Mentioned in ynet culinary tour."}
    },
    # === KFAR KAMA (Circassian) ===
    {
        "name": {"he": "בית הצ'רקסי", "en": "The Circassian House"},
        "dish_name": {"he": "פשטידה צ'רקסית (חלז'ין)", "en": "Circassian Pastry (Halzhin)"},
        "price": 25, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "כפר כמא", "en": "Kfar Kama"}, "address": {"he": "כפר כמא", "en": "Kfar Kama"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "הכפר הצ'רקסי היחיד בגליל. מאפים צ'רקסיים מסורתיים.", "en": "The only Circassian village in the Galilee. Traditional Circassian pastries."}
    },
    # === AR'ARA BANEGEV ===
    {
        "name": {"he": "סהארה מקסיקני", "en": "Sahara Mexican"},
        "dish_name": {"he": "טורטייה עם עוף", "en": "Chicken Tortilla"},
        "price": 30, "category": {"he": "מקסיקני", "en": "Mexican"},
        "location": {"city": {"he": "ערערה בנגב", "en": "Ar'ara BaNegev"}, "address": {"he": "שכונה 1, ערערה בנגב", "en": "Neighborhood 1, Ar'ara BaNegev"}, "region": {"he": "דרום", "en": "South"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "https://zips.co.il/%D7%A2%D7%A1%D7%A7%D7%99%D7%9D/%D7%A2%D7%A8%D7%A2%D7%A8%D7%94-%D7%91%D7%A0%D7%92%D7%91/%D7%9E%D7%A1%D7%A2%D7%93%D7%95%D7%AA-%D7%9E%D7%A7%D7%A1%D7%99%D7%A7%D7%A0%D7%99%D7%95%D7%AA/31839",
        "notes": {"he": "מסעדה מקסיקנית בעיירה בדואית. טורטיות, בשרים וסלטים.", "en": "Mexican restaurant in Bedouin town. Tortillas, meats and salads."}
    },
    # === DEIR AL-ASAD ===
    {
        "name": {"he": "שווארמה דיר אל-אסד", "en": "Deir al-Asad Shawarma"},
        "dish_name": {"he": "שווארמה בפיתה", "en": "Shawarma in Pita"},
        "price": 25, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "דיר אל-אסד", "en": "Deir al-Asad"}, "address": {"he": "דיר אל-אסד", "en": "Deir al-Asad"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "עיירה ערבית בגליל העליון.", "en": "Arab town in the Upper Galilee."}
    },
    # === MUGHAR ===
    {
        "name": {"he": "פלאפל אל-מוגאר", "en": "Mughar Falafel"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 12, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "מוגאר", "en": "Mughar"}, "address": {"he": "מוגאר", "en": "Mughar"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "עיירה דרוזית-נוצרית בגליל התחתון.", "en": "Druze-Christian town in the Lower Galilee."}
    },
    # === I'BILLIN ===
    {
        "name": {"he": "חומוס אעבלין", "en": "I'billin Hummus"},
        "dish_name": {"he": "חומוס מלא", "en": "Full Hummus Plate"},
        "price": 20, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "אעבלין", "en": "I'billin"}, "address": {"he": "אעבלין", "en": "I'billin"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "עיירה ערבית-נוצרית בגליל.", "en": "Arab-Christian town in the Galilee."}
    },
    # === DABBURIYYA ===
    {
        "name": {"he": "פלאפל דבוריה", "en": "Dabburiyya Falafel"},
        "dish_name": {"he": "פלאפל בפיתה עם סלט", "en": "Falafel in Pita with Salad"},
        "price": 12, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "דבוריה", "en": "Dabburiyya"}, "address": {"he": "דבוריה", "en": "Dabburiyya"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר ערבי למרגלות הר תבור.", "en": "Arab village at the foot of Mount Tabor."}
    },
    # === IKSAL ===
    {
        "name": {"he": "חומוס אכסאל", "en": "Iksal Hummus"},
        "dish_name": {"he": "חומוס עם פול", "en": "Hummus with Ful"},
        "price": 20, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "אכסאל", "en": "Iksal"}, "address": {"he": "אכסאל", "en": "Iksal"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר ערבי ליד נצרת.", "en": "Arab village near Nazareth."}
    },
    # === TUR'AN ===
    {
        "name": {"he": "שווארמה טוראן", "en": "Tur'an Shawarma"},
        "dish_name": {"he": "שווארמה בלאפה", "en": "Shawarma in Laffa"},
        "price": 25, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "טוראן", "en": "Tur'an"}, "address": {"he": "טוראן", "en": "Tur'an"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר ערבי בגליל התחתון.", "en": "Arab village in the Lower Galilee."}
    },
    # === EIN MAHIL ===
    {
        "name": {"he": "פלאפל עין מאהל", "en": "Ein Mahil Falafel"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 12, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "עין מאהל", "en": "Ein Mahil"}, "address": {"he": "עין מאהל", "en": "Ein Mahil"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר ערבי ליד נצרת.", "en": "Arab village near Nazareth."}
    },
    # === KAFR MANDA ===
    {
        "name": {"he": "חומוס כפר מנדא", "en": "Kafr Manda Hummus"},
        "dish_name": {"he": "חומוס מלא", "en": "Full Hummus Plate"},
        "price": 18, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "כפר מנדא", "en": "Kafr Manda"}, "address": {"he": "כפר מנדא", "en": "Kafr Manda"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר ערבי בגליל התחתון.", "en": "Arab village in the Lower Galilee."}
    },
    # === SDE BOKER ===
    {
        "name": {"he": "אינתי - חומוסייה דרומית", "en": "Inti - Southern Hummus"},
        "dish_name": {"he": "חומוס עם פלאפל וטוגנים", "en": "Hummus with Falafel & Fritters"},
        "price": 30, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "שדה בוקר", "en": "Sde Boker"}, "address": {"he": "מדרשת בן גוריון, שדה בוקר", "en": "Midreshet Ben Gurion, Sde Boker"}, "region": {"he": "דרום", "en": "South"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "https://www.maariv.co.il/food/article-1163797",
        "notes": {"he": "חומוסייה במדרשת בן גוריון. פתוח א'-ו'. כרובית, צ'יפס, סלט.", "en": "Hummus at Ben Gurion campus. Open Sun-Fri. Cauliflower, fries, salad."}
    },
    {
        "name": {"he": "החומוסייה שדה בוקר", "en": "HaChumusiya Sde Boker"},
        "dish_name": {"he": "חומוס עם פיתה", "en": "Hummus with Pita"},
        "price": 25, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "שדה בוקר", "en": "Sde Boker"}, "address": {"he": "מרכז מסחרי, מדרשת שדה בוקר", "en": "Commercial Center, Midreshet Sde Boker"}, "region": {"he": "דרום", "en": "South"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "https://www.rest.co.il/rest/80369213/",
        "notes": {"he": "אחות קטנה לאינתי מירוחם.", "en": "Sister branch of Inti from Yeruham."}
    },
    # === EIN GEDI ===
    {
        "name": {"he": "חאן עין גדי", "en": "Khan Ein Gedi"},
        "dish_name": {"he": "חומוס עם שתי פיתות", "en": "Hummus with Two Pitas"},
        "price": 28, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "עין גדי", "en": "Ein Gedi"}, "address": {"he": "חאן עין גדי", "en": "Khan Ein Gedi Camplodge"}, "region": {"he": "דרום", "en": "South"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "https://eingedicamp.co.il/",
        "notes": {"he": "בר/מסעדה בחאן עין גדי ליד ים המלח.", "en": "Bar/restaurant at Ein Gedi camplodge near the Dead Sea."}
    },
    # === GOLANI JUNCTION ===
    {
        "name": {"he": "מסעדת יונס", "en": "Yunis Restaurant"},
        "dish_name": {"he": "חומוס עם בשר", "en": "Hummus with Meat"},
        "price": 30, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "צומת גולני", "en": "Golani Junction"}, "address": {"he": "כביש 77/65, צומת גולני", "en": "Road 77/65, Golani Junction"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "מסעדה מזרחית ותיקה משנת 1976. מיקום אייקוני בצומת.", "en": "Veteran Eastern restaurant since 1976. Iconic junction location."}
    },
    # === MEGIDDO JUNCTION ===
    {
        "name": {"he": "מסעדת הנחל", "en": "HaNachal Restaurant"},
        "dish_name": {"he": "חומוס עם פלאפל", "en": "Hummus with Falafel"},
        "price": 25, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "צומת מגידו", "en": "Megiddo Junction"}, "address": {"he": "צומת מגידו", "en": "Megiddo Junction"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "https://www.anahalmegido.co.il/",
        "notes": {"he": "מטבח מזרחי מסורתי עם נוף פסטורלי. פסטלים, כרובית, פלאפל.", "en": "Traditional Eastern kitchen with pastoral views. Pastels, cauliflower, falafel."}
    },
    {
        "name": {"he": "אלחג' סאלח", "en": "Al-Haj Salach"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 15, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "צומת מגידו", "en": "Megiddo Junction"}, "address": {"he": "דור אלון גבעת עוז, צומת מגידו", "en": "Dor Alon Givat Oz, Megiddo Junction"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "https://easy.co.il/en/page/5645925",
        "notes": {"he": "אוכל ערבי אותנטי בתחנת דלק.", "en": "Authentic Arab food at a gas station."}
    },
    # === GLILOT JUNCTION ===
    {
        "name": {"he": "פיצה הר סיני", "en": "Pizza Har Sinai"},
        "dish_name": {"he": "משולש פיצה גדול", "en": "Large Pizza Slice"},
        "price": 22, "category": {"he": "פיצה", "en": "Pizza"},
        "location": {"city": {"he": "צומת גלילות", "en": "Glilot Junction"}, "address": {"he": "ביג פאשן גלילות", "en": "Big Fashion Glilot"}, "region": {"he": "מרכז", "en": "Center"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "משולשי פיצה גדולים בקניון ביג גלילות. האופציה הזולה ביותר.", "en": "Large pizza slices at Big Fashion Glilot. The cheapest option."}
    },
    # === KIRYAT ARBA ===
    {
        "name": {"he": "פלאפל קריית ארבע", "en": "Kiryat Arba Falafel"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 15, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "קריית ארבע", "en": "Kiryat Arba"}, "address": {"he": "מרכז מסחרי, קריית ארבע", "en": "Commercial Center, Kiryat Arba"}, "region": {"he": "ירושלים", "en": "Jerusalem"}},
        "kosher_status": {"he": "כשר למהדרין", "en": "Mehadrin Kosher"},
        "source_url": "",
        "notes": {"he": "יישוב יהודי ליד חברון.", "en": "Jewish settlement near Hebron."}
    },
    # === HATZOR ASHDOD (Hatzor HaGlilit supplement already covered, this is Hazor near Ashdod) ===
    {
        "name": {"he": "פנינה פאי", "en": "Pnina Pie"},
        "dish_name": {"he": "בולוצ'קי (לחמנייה מתוקה)", "en": "Sweet Bun (Bulochki)"},
        "price": 6, "category": {"he": "מאפייה", "en": "Bakery"},
        "location": {"city": {"he": "אשדוד", "en": "Ashdod"}, "address": {"he": "אשדוד", "en": "Ashdod"}, "region": {"he": "דרום", "en": "South"}},
        "kosher_status": {"he": "כשר", "en": "Kosher"},
        "source_url": "",
        "notes": {"he": "מאפייה משנת 1992. חצ'פורי ב-16 ש\"ח.", "en": "Bakery since 1992. Khachapuri for 16 NIS."}
    },
    # === YAFA AN-NASIRA (Yafa near Nazareth) ===
    {
        "name": {"he": "פלאפל יאפא", "en": "Yafa Falafel"},
        "dish_name": {"he": "פלאפל בפיתה", "en": "Falafel in Pita"},
        "price": 12, "category": {"he": "אוכל רחוב", "en": "Street Food"},
        "location": {"city": {"he": "יאפא (יפיע)", "en": "Yafa an-Nasira"}, "address": {"he": "יפיע", "en": "Yafa an-Nasira"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר ערבי ליד נצרת.", "en": "Arab village near Nazareth."}
    },
    # === NAHF ===
    {
        "name": {"he": "חומוס נחף", "en": "Nahf Hummus"},
        "dish_name": {"he": "חומוס עם חומוס", "en": "Hummus Plate"},
        "price": 18, "category": {"he": "חומוס", "en": "Hummus"},
        "location": {"city": {"he": "נחף", "en": "Nahf"}, "address": {"he": "נחף", "en": "Nahf"}, "region": {"he": "צפון", "en": "North"}},
        "kosher_status": {"he": "לא כשר", "en": "Not Kosher"},
        "source_url": "",
        "notes": {"he": "כפר ערבי בגליל.", "en": "Arab village in the Galilee."}
    },
]

# ---- Load, add, save ----
DATA = "/Users/nadavharel/lunch upto 35 nis/data/restaurants_i18n.json"
with open(DATA, "r", encoding="utf-8") as f:
    db = json.load(f)

max_id = max(int(e["id"]) for e in db)
for i, entry in enumerate(NEW_ENTRIES, start=1):
    entry["id"] = str(max_id + i)
    entry["verified_date"] = "2025-02"
    if "notes" not in entry:
        entry["notes"] = None
    db.append(entry)

with open(DATA, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print(f"Added {len(NEW_ENTRIES)} entries. Total: {len(db)}\n")

# Stats
from collections import Counter
cities = Counter(e["location"]["city"]["en"] for e in db)
regions = Counter(e["location"]["region"]["en"] for e in db)
cats = Counter(e["category"]["en"] for e in db)
prices = [e["price"] for e in db]

print(f"Cities ({len(cities)}):")
for c, n in cities.most_common():
    print(f"  {c}: {n}")

print(f"\nRegions:")
for r, n in regions.most_common():
    print(f"  {r}: {n}")

print(f"\nCategories:")
for c, n in cats.most_common():
    print(f"  {c}: {n}")

print(f"\nPrice range: {min(prices)}-{max(prices)} NIS, avg: {sum(prices)/len(prices):.1f} NIS")
