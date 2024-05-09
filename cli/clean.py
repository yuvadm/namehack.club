import ymlstash

from .base import cli, NAMES_DIR
from .model import Name


@cli.command()
def clean():
    stash = ymlstash.YmlStash(Name, NAMES_DIR, filter_none=True)
    names = stash.list_keys()
    for name in names:
        obj = stash.load(name)
        stash.delete(obj.domain.replace(".", ""))
        stash.save(obj)
