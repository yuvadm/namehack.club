import click
import sys

from pathlib import Path
from subprocess import run

from .base import cli

ROOT_PATH = Path(__file__).parents[1]


@cli.command()
@click.argument("path", type=click.Path())
def ghpr(path):
    with open(path, "r") as f:
        for line in f:
            l = line.strip().split(",")
            domain, handle, name = [x.strip() for x in l]
            handle = None if "@" in handle else handle

            fn = domain.replace(".", "")

            path = ROOT_PATH / "names" / f"{fn}.yml"
            if path.exists():
                print(f"{domain} already exists")
                continue

            with open(path, "w") as out:
                s = f"domain: {domain}\nname: {name}\n"
                if handle:
                    s += f"github: {handle}\n"
                s += "candidate: true\n"
                out.write(s)

            # run(["git", "checkout", "-b", domain])
            # run(["git", "add", f"names/{fn}.yml"])
            # run(["git", "commit", "-m", f"Add {domain}"])
            # run(["git", "push", "-u", "origin", domain])
            # run(["gh", "pr", "create", "-t", f"Add {domain}", "-b", f"Hey @{handle}, would you like to merge this PR adding you to https://namehack.club?"])
            # run(["git", "checkout", "main"])
