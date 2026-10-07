"""Location of the shared JSON data (schemes, name lexicon, rules).

In an installed package the data is bundled as ``translit_names/data`` (the
build hook copies the repository's top-level ``data/`` directory into the
wheel).  In a development checkout the package is imported from
``py/src/translit_names`` and the data is read from ``<repo>/data``.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # importlib.abc.Traversable is removed at runtime in Python 3.14
    from importlib.abc import Traversable

__all__ = ["data_path"]


def data_path() -> Traversable:
    """Directory containing ``schemes/``, ``names/``, ``defaults.json`` …"""
    bundled = resources.files("translit_names") / "data"
    if bundled.is_dir():
        return bundled
    repo = Path(__file__).resolve().parents[3] / "data"
    if repo.is_dir():
        return repo
    raise FileNotFoundError("translit_names data directory not found (expected translit_names/data or <repo>/data)")
