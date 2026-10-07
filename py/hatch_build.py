"""Bundle the repository's shared ``data/`` directory into the Python package.

The JSON data (schemes, name lexicon, rules) lives once at the repository
root and is shared with the TypeScript package in ``js/``.  Wheels get it as
``translit_names/data``; source distributions carry it under
``src/translit_names/data`` so that a wheel can later be built from the sdist
alone.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):  # type: ignore[type-arg]
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        if self.target_name == "wheel" and version == "editable":
            return  # development install: data is read from <repo>/data
        root = Path(self.root)
        shared = root.parent / "data"
        bundled = root / "src" / "translit_names" / "data"
        if shared.is_dir():
            target = "translit_names/data" if self.target_name == "wheel" else "src/translit_names/data"
            build_data["force_include"][str(shared)] = target
        elif not bundled.is_dir():
            raise RuntimeError(f"translit-names data not found: neither {shared} nor {bundled} exists")
