import requests

from pathlib import Path

ROOT_PATH = Path(__file__).parents[1]

DATA_DIR = ROOT_PATH / "data"

TLDS_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
MALE_NAMES_URL = "https://raw.githubusercontent.com/DictionaryHouse/EnglishName/master/top_1000_EN_%E7%94%B7%E6%80%A7names_english.txt"
FEMALE_NAMES_URL = "https://raw.githubusercontent.com/DictionaryHouse/EnglishName/master/top_1000_EN_%E5%A5%B3%E6%80%A7names_english.txt"

with open(DATA_DIR / "tlds.txt", "w") as f:
    print("Fetching TLDs...")
    res = requests.get(TLDS_URL)
    tlds = [tld.lower() for tld in res.text.strip().split("\n")[1:] if len(tld) < 4]
    f.write("\n".join(tlds).strip())
    TLDS = set(tlds)

NAMES = []

with open(DATA_DIR / "names.txt", "w") as f:
    print("Fetching female names...")
    res = requests.get(FEMALE_NAMES_URL)
    f.write(res.text)
    NAMES += res.text.split("\n")
    print("Fetching male names...")
    res = requests.get(MALE_NAMES_URL)
    f.write(res.text)
    NAMES += res.text.split("\n")

# print(NAMES)
# print(TLDS)

CANDIDATES = []

for name in NAMES:
    if name[-2:] in TLDS:
        CANDIDATES.append(f"{name[:-2]}.{name[-2:]}")
    if name[-3:] in TLDS:
        CANDIDATES.append(f"{name[:-3]}.{name[-3:]}")

with open(DATA_DIR / "domains.txt", "w") as f:
    f.write("\n".join(CANDIDATES).strip())

for c in CANDIDATES:
    try:
        print(f"Fetching {c}...", end="")
        res = requests.get(f"http://{c}", timeout=5)
        if res.ok:
            print(f"Found {c}!")
            with open(DATA_DIR / "homepages" / f"{c}.html", "w") as f:
                f.write(res.text)
        else:
            print("x")
    except:
        print("x")