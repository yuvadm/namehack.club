import click

from cli import cli

cli = click.CommandCollection(sources=[cli])

# this file is only required for Netlify build to be able to trigger CLI
if __name__ == "__main__":
    cli()
