import os

from .base import cli

from .build import build

__all__ = [cli, build]

# ugly workaround to avoid build failures in Python 3.8
if "NETLIFY" not in os.environ:
    from .clean import clean
    from .ghpr import ghpr
    from .scan import scan

    __all__ += [clean, ghpr, scan]
