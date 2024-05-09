import click

from pathlib import Path

ROOT_PATH = Path(__file__).parents[1]
NAMES_DIR = ROOT_PATH / "names"


@click.group
def cli():
    pass
