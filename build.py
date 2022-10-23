import yaml

from jinja2 import Environment, PackageLoader, select_autoescape
from os import listdir, mkdir
from pathlib import Path
from shutil import copyfile

ROOT_PATH = Path(__file__).parent

NAMES_DIR = ROOT_PATH / "names"
BUILD_DIR = ROOT_PATH / "build"
STATIC_DIR = ROOT_PATH / "static"

REQUIRED_FIELDS = set(["domain", "name", "email"])

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
        missing_fields = REQUIRED_FIELDS - set(fields.keys())
        if missing_fields:
            raise Exception(f"Missing required fields {missing_fields} in {name}")
        names.append(fields)

# render templates
env = Environment(
    loader=PackageLoader("build"),
    autoescape=select_autoescape()
)
for template in TEMPLATES:
    t = env.get_template(template)
    index = t.render(names=names)
    with open(BUILD_DIR / "index.html", "w") as f:
        f.write(index)