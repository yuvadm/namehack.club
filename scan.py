import requests

from pathlib import Path

ROOT_PATH = Path(__file__).parent

DATA_DIR = ROOT_PATH / "data"

TLDS_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"

with open(DATA_DIR / "tlds.txt", "w") as f:
    res = requests.get(TLDS_URL)
    tlds = [tld.lower() for tld in res.text.split("\n")[1:] if len(tld) < 4]
    f.write("\n".join(tlds).strip())