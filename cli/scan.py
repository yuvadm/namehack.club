import aiohttp
import asyncio
import json
import requests

from pathlib import Path
from os import makedirs, listdir

from .base import cli

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
        res = set()
        for fn in listdir(DATA_DIR / "names"):
            with open(DATA_DIR / "names" / fn, "r") as f:
                j = json.load(f)
                names = j["advanced"]
                if names:
                    suffix = fn.split(".")[0]
                    for name in names:
                        n = name["name"].lower().split(suffix)[0]
                        if n:
                            res.add(n)
        with open(DATA_DIR / "allnames.txt", "w") as out:
            for n in res:
                out.write(n + f".{suffix}\n")

    async def get_homepage(self, session, domain):
        try:
            url = f"http://{domain}"
            async with session.get(url) as res:
                res = await res.text()
                if res:
                    print(f"Got {len(res)} bytes from {domain}")
                    with open(DATA_DIR / "homepages" / f"{domain}.html", "w") as out:
                        out.write(res)
                return len(res)
        except Exception as e:
            return 0

    async def fetch_homepages(self, N):
        with open(DATA_DIR / "allnames.txt", "r") as f:
            names = [x.strip() for x in f.readlines()][N * 1000 : 1000 * (N + 1)]

        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            for name in names:
                tasks.append(asyncio.ensure_future(self.get_homepage(session, name)))

            resps = await asyncio.gather(*tasks)

    def find_homepages(self):
        res = {}
        for fn in listdir(DATA_DIR / "homepages"):
            with open(DATA_DIR / "homepages" / fn, "r") as f:
                domain = fn[:-5]
                name = domain.replace(".", "")
                text = f.read()
                nip = name in text
                github = "github" in text
                li = "linkedin" in text
                sale = "for sale" in text or "register" in text or "parking" in text
                res["domain"] = {
                    "name": name,
                    "name_in_page": nip,
                    "github": github,
                    "linkedin": li,
                }
                ge = "✅" if github else "  "
                le = "✅" if li else "  "
                ne = "✅" if nip else "  "
                se = "❌" if sale else "  "
                print(f"{ne}{ge}{le}{se}{name:20}")


@cli.command()
def scan():
    ns = NameScanner()
    # for i in range(0, 26):
    #     asyncio.run(ns.fetch_homepages(i))
    # ns.consolidate_names()
    ns.find_homepages()
