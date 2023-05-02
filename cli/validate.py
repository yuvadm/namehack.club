import requests
import yaml

from pathlib import Path
from os import makedirs, listdir

from .base import cli

ROOT_PATH = Path(__file__).parents[1]

NAMES_DIR = ROOT_PATH / "names"


@cli.command()
def validate():
    print("Validating...")
    for name in listdir(NAMES_DIR):
        with open(NAMES_DIR / name, "r") as f:
            fields = yaml.load(f.read(), Loader=yaml.Loader)
            url = fields.get("url") or "https://" + fields.get("domain")
            try:
                res = requests.get(url)
                if res.ok:
                    continue
            except:
                pass
            if res:
                print(f"Failure in {url}...")
                print(res.text)
