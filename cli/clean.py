from .base import cli, STASH


@cli.command()
def clean():
    names = STASH.list_keys()
    for name in names:
        obj = STASH.load(name)
        STASH.save(obj)
