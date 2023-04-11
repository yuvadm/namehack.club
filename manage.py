import os
import click

from cli import clean

cli = click.CommandCollection(sources=[clean])

if __name__ == "__main__":
    cli()
