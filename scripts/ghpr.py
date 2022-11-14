import sys

from pathlib import Path
from subprocess import run

ROOT_PATH = Path(__file__).parent

path = sys.argv[1]

with open(path, "r") as f:
    for line in f:
        l = line.strip().split(",")
        domain, handle, name = [x.strip() for x in l]

        fn = domain.replace(".", "")
        with open(ROOT_PATH / "names" / f"{fn}.yml", "w") as out:
            s = f"domain: {domain}\nname: {name}\ngithub: {handle}\n"
            out.write(s)

        run(["git", "checkout", "-b", domain])
        run(["git", "add", f"names/{fn}.yml"])
        run(["git", "commit", "-m", f"Add {domain}"])
        run(["git", "push", "-u", "origin", domain])
        run(["gh", "pr", "create", "-t", f"Add {domain}", "-b", f"Hey @{handle}, would you like to merge this PR adding you to https://namehack.club?"])
        run(["git", "checkout", "main"])
