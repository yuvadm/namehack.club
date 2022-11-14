import yaml

from jinja2 import Environment, PackageLoader, select_autoescape
from os import listdir, mkdir
from pathlib import Path
from shutil import copyfile

ROOT_PATH = Path(__file__).parent

NAMES_DIR = ROOT_PATH / "names"
BUILD_DIR = ROOT_PATH / "build"
STATIC_DIR = ROOT_PATH / "static"

REQUIRED_FIELDS = set(["domain", "name"])
OPTIONAL_FIELDS = set(["url", "title", "email", "github"])

TEMPLATES = ["index.html"]

# copy static files
if not BUILD_DIR.exists():
    mkdir(BUILD_DIR)
for f in listdir(STATIC_DIR):
    copyfile(STATIC_DIR / f, BUILD_DIR / f)

# process all name yamls
names = []
for name in listdir(NAMES_DIR):
    with open(NAMES_DIR / name, "r") as f:
        fields = yaml.load(f.read(), Loader=yaml.Loader)
        field_set = set(fields.keys())
        missing_fields = REQUIRED_FIELDS - field_set
        if missing_fields:
            raise Exception(f"Missing required fields {missing_fields} in {name}")
        invalid_fields = field_set - OPTIONAL_FIELDS - REQUIRED_FIELDS
        if invalid_fields:
            raise Exception(f"Invalid fields {invalid_fields} in {name}")
        names.append(fields)
names = list(sorted(names, key=lambda x: x["domain"]))


def render_link(value, classes):
    name = value["name"].lower().split(" ")
    domain = value["domain"].replace(".", "")
    res = []
    for part in name:
        if part == domain:
            url = value.get("url") or "https://" + value.get("domain")
            res.append(f'<a href="{url}" class="{classes}">{value["domain"]}</a>')
        else:
            res.append(part)
    return " ".join(res)


# render templates
env = Environment(loader=PackageLoader("build"), autoescape=select_autoescape())
env.filters["render_link"] = render_link
for template in TEMPLATES:
    t = env.get_template(template)
    index = t.render(names=names)
    with open(BUILD_DIR / "index.html", "w") as f:
        f.write(index)
