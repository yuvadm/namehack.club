import click
import ymlstash

from pathlib import Path
from .model import Name

ROOT_PATH = Path(__file__).parents[1]
NAMES_DIR = ROOT_PATH / "names"

STASH = ymlstash.YmlStash(Name, NAMES_DIR, filter_none=True)


@click.group
def cli():
    pass
