from jinja2 import Environment, PackageLoader, select_autoescape
from os import listdir, mkdir
from pathlib import Path
from shutil import copyfile
from unidecode import unidecode

from .base import cli, STASH

ROOT_PATH = Path(__file__).parents[1]

NAMES_DIR = ROOT_PATH / "names"
BUILD_DIR = ROOT_PATH / "build"
STATIC_DIR = ROOT_PATH / "static"

TEMPLATES = ["index.html"]


@cli.command()
def build():
    # copy static files
    if not BUILD_DIR.exists():
        mkdir(BUILD_DIR)
    for f in listdir(STATIC_DIR):
        copyfile(STATIC_DIR / f, BUILD_DIR / f)

    # process all name yamls
    names = []
    candidates = []

    for key in STASH.list_keys():
        name = STASH.load(key)
        if name.invalid is True:
            continue
        if name.candidate is True:
            candidates.append(name)
        else:
            names.append(name)

    names = list(sorted(names, key=lambda x: x.domain))
    candidates = list(sorted(candidates, key=lambda x: x.domain))

    def render_link(value, classes):
        name = unidecode(value.name).lower().split(" ")
        domain = unidecode(value.domain).replace(".", "")
        res = []
        for part in name:
            if part == domain:
                url = value.url or "https://" + value.domain
                res.append(f'<a href="{url}" class="{classes}">{value.domain}</a>')
            else:
                res.append(part)
        return " ".join(res)

    # render templates
    env = Environment(
        loader=PackageLoader("manage"),
        autoescape=select_autoescape(),
    )
    env.filters["render_link"] = render_link
    for template in TEMPLATES:
        t = env.get_template(template)
        index = t.render(names=names, candidates=candidates)
        with open(BUILD_DIR / "index.html", "w") as f:
            f.write(index)
