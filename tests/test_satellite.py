"""Phase 2: propagation is reproducible and physically sensible.

Same pinned TLE as test_tle.py. Expected numbers were computed once with
Skyfield and frozen here, so the test fails only if our code changes.
"""
import math
from datetime import datetime, timezone

import pytest
from skyfield.api import EarthSatellite

from satellite_tracker.satellite import geodetic_position, propagate

LINE1 = "1 25544U 98067A   26256.17555434  .00004898  00000+0  96695-4 0  9992"
LINE2 = "2 25544  51.6307 224.6171 0004917 134.6730 225.4659 15.49096932585393"
WHEN = datetime(2026, 9, 13, 12, 0, 0, tzinfo=timezone.utc)  # ~8 h after epoch


@pytest.fixture
def iss() -> EarthSatellite:
    return EarthSatellite(LINE1, LINE2, "ISS (ZARYA)")


def test_geodetic_position_matches_pinned_values(iss) -> None:
    pos = geodetic_position(iss, WHEN)
    assert pos.latitude_deg == pytest.approx(8.3003, abs=1e-3)
    assert pos.longitude_deg == pytest.approx(57.1123, abs=5e-3)
    assert pos.altitude_km == pytest.approx(421.33, abs=0.05)


def test_position_is_physically_sensible(iss) -> None:
    pos = geodetic_position(iss, WHEN)
    assert 300 < pos.altitude_km < 500          # the ISS lives near 400 km
    assert abs(pos.latitude_deg) <= 51.64       # never poleward of inclination
    assert -180 <= pos.longitude_deg <= 180


def test_teme_state_radius_and_speed(iss) -> None:
    state = propagate(iss, WHEN)
    r_km = math.hypot(*state.position_teme_km)
    v_km_s = math.hypot(*state.velocity_teme_km_s)
    assert r_km == pytest.approx(6799.0, abs=1.0)   # Earth radius + altitude
    assert 7.5 < v_km_s < 7.8                       # LEO speed; Phase 3 explains


def test_naive_datetime_is_rejected(iss) -> None:
    with pytest.raises(ValueError):
        geodetic_position(iss, datetime(2026, 9, 13, 12, 0, 0))