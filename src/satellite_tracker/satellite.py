"""Propagate a satellite: TLE elements plus a UTC instant -> where it is.

Two pipeline arrows live here:
    TLE -> SGP4 -> TEME state vector          propagate()
    TEME -> Earth rotation -> lat/lon/alt     geodetic_position()  (Skyfield, for now)
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import cache

from sgp4.api import SGP4_ERRORS, jday
from skyfield.api import EarthSatellite, load, wgs84


@dataclass(frozen=True)
class TemeState:
    """SGP4 output at one instant, in TEME: Earth-centered, non-rotating."""

    time_utc: datetime
    position_teme_km: tuple[float, float, float]
    velocity_teme_km_s: tuple[float, float, float]


@dataclass(frozen=True)
class GeodeticPosition:
    """The point on the WGS84 ellipsoid beneath the satellite, and its height."""

    time_utc: datetime
    latitude_deg: float   # north positive
    longitude_deg: float  # east positive, -180 to 180
    altitude_km: float    # above the WGS84 ellipsoid, not sea level or terrain


def _as_utc(when: datetime) -> datetime:
    """Accept any timezone-aware datetime and return it in UTC. Reject naive ones."""
    if when.tzinfo is None:
        raise ValueError(f"{when!r} has no timezone; use datetime.now(timezone.utc)")
    return when.astimezone(timezone.utc)


def propagate(sat: EarthSatellite, when: datetime) -> TemeState:
    """Run SGP4: mean elements at epoch + elapsed time -> position and velocity.

    Calls the sgp4 library directly so the propagation step is visible here.
    """
    when_utc = _as_utc(when)
    # Julian Date: astronomy's one continuous day count (day 0 was in 4713 BC;
    # today is about 2,461,300). sgp4 wants it split into whole days + fraction.
    # The TLE epoch is UTC, so the propagation time is UTC too.
    jd, fr = jday(
        when_utc.year, when_utc.month, when_utc.day,
        when_utc.hour, when_utc.minute,
        when_utc.second + when_utc.microsecond / 1e6,
    )
    error_code, position_teme_km, velocity_teme_km_s = sat.model.sgp4(jd, fr)
    if error_code != 0:
        raise ValueError(f"SGP4 error {error_code}: {SGP4_ERRORS[error_code]}")
    return TemeState(when_utc, tuple(position_teme_km), tuple(velocity_teme_km_s))


@cache
def _timescale():
    """Skyfield's time tables (leap seconds, UT1-UTC), built once on first use
    from data bundled with the library. No download, no work at import time."""
    return load.timescale()


def geodetic_position(sat: EarthSatellite, when: datetime) -> GeodeticPosition:
    """Where the satellite is over the Earth.

    Skyfield rotates TEME into the Earth-fixed frame and solves the WGS84
    ellipsoid geometry. Phases 5 and 12 rebuild those two steps by hand.
    """
    when_utc = _as_utc(when)
    t = _timescale().from_datetime(when_utc)
    subpoint = wgs84.geographic_position_of(sat.at(t))
    return GeodeticPosition(
        time_utc=when_utc,
        latitude_deg=subpoint.latitude.degrees,
        longitude_deg=subpoint.longitude.degrees,
        altitude_km=subpoint.elevation.km,
    )