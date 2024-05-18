from .base import cli, STASH


@cli.command()
def clean():
    names = STASH.list_keys()
    for name in names:
        try:
            obj = STASH.load(name)
            STASH.save(obj)
        except Exception as e:
            print(f"Error {e} when attempting to clean {name=}")
