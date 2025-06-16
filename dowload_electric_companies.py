import requests
import json
import time

API_TOKEN = "BURAYA_KENDI_PAPPERS_API_KEY'INI_YAZ"  # https://pappers.fr/api adresinden ücretsiz alabilirsin
NAF_CODE = "4669A"  # Commerce de gros de matériel électrique
PER_PAGE = 100
MAX_PAGES = 1000  # Pappers limiti, toplamda 100.000 şirket çekebilirsin

all_results = []

for page in range(1, MAX_PAGES+1):
    params = {
        "api_token": API_TOKEN,
        "activite": NAF_CODE,
        "page": page,
        "par_page": PER_PAGE,
    }
    try:
        resp = requests.get("https://api.pappers.fr/v2/recherche", params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if "resultats" not in data or not data["resultats"]:
            print(f"Bitti: {len(all_results)} şirket toplandı.")
            break
        all_results.extend(data["resultats"])
        print(f"{len(all_results)} şirket toplandı (sayfa {page})")
        time.sleep(0.5)  # API limitine takılmamak için
    except Exception as e:
        print(f"Hata: {e}")
        break

# Temel alanları sadeleştirip kaydet
out = []
for c in all_results:
    out.append({
        "nom": c.get("nom_entreprise"),
        "siren": c.get("siren"),
        "naf": c.get("code_naf"),
        "adresse": c.get("siege", {}).get("adresse_ligne_1", ""),
        "ville": c.get("siege", {}).get("ville", ""),
        "cp": c.get("siege", {}).get("code_postal", ""),
        "site": c.get("site_internet"),
        "date_creation": c.get("date_creation"),
        "statut": c.get("statut_entreprise"),
    })

with open("electricite_france.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"\nToplam {len(out)} elektrik şirketi kaydedildi (electricite_france.json)")
