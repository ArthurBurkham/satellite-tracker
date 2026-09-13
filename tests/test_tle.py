"""Parse a fixed, known TLE and check fields. No network in tests, ever."""
import math

import pytest
from skyfield.api import EarthSatellite

LINE1 = "1 25544U 98067A   26256.17555434  .00004898  00000+0  96695-4 0  9992"
LINE2 = "2 25544  51.6307 224.6171 0004917 134.6730 225.4659 15.49096932585393"


def test_parse_known_iss_tle() -> None:
    sat = EarthSatellite(LINE1, LINE2, "ISS (ZARYA)")
    assert sat.model.satnum == 25544
    assert math.degrees(sat.model.inclo) == pytest.approx(51.6307, abs=1e-4)
    rev_per_day = sat.model.no_kozai * 1440.0 / (2.0 * math.pi)
    assert rev_per_day == pytest.approx(15.49096932, abs=1e-6)