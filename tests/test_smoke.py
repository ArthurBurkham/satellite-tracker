"""Phase 0 smoke test: the package is installed and importable."""
from importlib.metadata import version

import satellite_tracker


def test_version_matches_installed_metadata() -> None:
    assert satellite_tracker.__version__ == version("satellite-tracker")