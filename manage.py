import click

from cli import cli

cli = click.CommandCollection(sources=[cli])

if __name__ == "__main__":
    cli()
