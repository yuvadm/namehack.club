import os

from .base import cli

from .build import build
from .serve import serve

__all__ = [cli, build, serve]

# ugly workaround to avoid build failures in Python 3.8
if "NETLIFY" not in os.environ:
    from .validate import validate
    from .ghpr import ghpr
    from .scan import scan

    __all__ += [validate, ghpr, scan]
