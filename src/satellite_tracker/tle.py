"""Fetch, cache, and parse TLE data for one satellite.

The only module in the package allowed to touch the network.
"""
import math
from pathlib import Path

from skyfield.api import EarthSatellite, Loader

ISS_CATNR = 25544
_CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR={catnr}&FORMAT=TLE"
DATA_DIR = Path("data")          # gitignored since Phase 0
MAX_CACHE_AGE_DAYS = 3.0


def load_satellite(catnr: int = ISS_CATNR,
                   max_cache_age_days: float = MAX_CACHE_AGE_DAYS) -> EarthSatellite:
    """Return the satellite, downloading a fresh TLE only when the
    cached copy is missing or older than max_cache_age_days.
    CelesTrak asks clients to cache; hammering the API gets you blocked.
    """
    loader = Loader(str(DATA_DIR))          # creates data/ if needed
    filename = f"{catnr}.tle"
    if not loader.exists(filename) or loader.days_old(filename) > max_cache_age_days:
        loader.download(_CELESTRAK_URL.format(catnr=catnr), filename=filename)
    satellites = loader.tle_file(filename)
    if not satellites:
        raise ValueError(f"no TLE parsed from {DATA_DIR / filename}")
    return satellites[0]


def describe(sat: EarthSatellite) -> str:
    """Human-readable orbital elements.

    UNIT WARNING: sgp4 stores angles in RADIANS and mean motion in
    RADIANS PER MINUTE. Every line converts to the unit on its label.
    """
    m = sat.model
    rev_per_day = m.no_kozai * 1440.0 / (2.0 * math.pi)
    return "\n".join([
        f"{sat.name}  (catalog {m.satnum})",
        f"epoch (UTC):         {sat.epoch.utc_iso()}",
        f"inclination:         {math.degrees(m.inclo):10.4f} deg",
        f"RAAN:                {math.degrees(m.nodeo):10.4f} deg",
        f"eccentricity:        {m.ecco:10.7f}",
        f"argument of perigee: {math.degrees(m.argpo):10.4f} deg",
        f"mean anomaly:        {math.degrees(m.mo):10.4f} deg",
        f"mean motion:         {rev_per_day:10.4f} rev/day",
        f"orbital period:      {1440.0 / rev_per_day:10.2f} min",
    ])