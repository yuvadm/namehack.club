import json
import requests

from pathlib import Path
from os import makedirs, listdir

ROOT_PATH = Path(__file__).parents[1]

DATA_DIR = ROOT_PATH / "data"

TLDS_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"

NAMES_ENDPOINT = "https://nameberry.com/nameberry/api/v1/search"


class NameScanner:
    def fetch_tlds(self):
        with open(DATA_DIR / "tlds.txt", "w") as f:
            print("Fetching TLDs...")
            res = requests.get(TLDS_URL)
            tlds = [
                tld.lower() for tld in res.text.strip().split("\n")[1:] if len(tld) < 4
            ]
            f.write("\n".join(tlds).strip())
            TLDS = set(tlds)

    def fetch_homepage(self, domain):
        print(f"Fetching {domain}...", end="")
        res = requests.get(f"http://{domain}", timeout=5)
        if res.ok:
            print(f"Found {domain}!")
            with open(DATA_DIR / "homepages" / f"{domain}.html", "w") as f:
                f.write(res.text)
        else:
            print("x")

    def fetch_names(self, suffix, count=5000):
        res = requests.post(
            NAMES_ENDPOINT,
            json={
                "starts_with": "",
                "ends_with": suffix,
                "contains": "",
                "syllables": "",
                "origin_id": "",
                "derivation": "",
                "page": 1,
                "per_page": count,
            },
        )
        if res.ok:
            j = res.json()
            print(f"found {j['advanced_name_count']}")
            makedirs(DATA_DIR / "names", exist_ok=True)
            with open(DATA_DIR / "names" / f"{suffix}.json", "w") as f:
                f.write(res.text)

    def fetch_all(self):
        with open(DATA_DIR / "tlds.txt", "r") as f:
            for line in f:
                d = line.strip()
                print(f"Fetching {d}...", end="")
                self.fetch_names(d)

    def consolidate_names(self):
        with open(DATA_DIR / "allnames.txt", "w") as out:
            for fn in listdir(DATA_DIR / "names"):
                with open(DATA_DIR / "names" / fn, "r") as f:
                    j = json.load(f)
                    names = j["advanced"]
                    if names:
                        suffix = fn.split(".")[0]
                        for name in names:
                            n = name["name"].lower().split(suffix)[0]
                            if n:
                                out.write(n + f".{suffix}\n")


ns = NameScanner()
ns.consolidate_names()
