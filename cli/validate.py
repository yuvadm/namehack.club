from pathlib import Path

from .base import cli, STASH

ROOT_PATH = Path(__file__).parents[1]

NAMES_DIR = ROOT_PATH / "names"


@cli.command()
def validate():
    print("Validating...")
    names = STASH.list_keys()
    for name in names:
        try:
            obj = STASH.load(name)
            STASH.save(obj)
        except Exception as e:
            print(f"Error {e} when attempting to clean {name=}")
