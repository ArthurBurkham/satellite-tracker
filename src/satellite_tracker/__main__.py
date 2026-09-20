#from satellite_tracker import __version__
#from satellite_tracker.tle import describe, load_satellite

#def main() -> None:
#    print("satellite-tracker {__version__} (Phase 0 skeleton)")

#if __name__ == "__main__":
#    main()

"""Command-line entry point: run with `python -m satellite_tracker`."""
from datetime import datetime, timezone

from satellite_tracker.tle import describe, load_satellite
from satellite_tracker.satellite import geodetic_position



def main() -> None:
    """Load the satellite, orbital elements, and where it is at right now."""
    sat = load_satellite()
    print(describe(sat))

    now_utc = datetime.now(timezone.utc)
    pos = geodetic_position(sat, now_utc)
    print()
    print(f"position at {pos.time_utc:%H:%M:%S} UTC")
    print(f"latitude: {pos.latitude_deg:9.4f} deg")
    print(f"longitude: {pos.longitude_deg:9.4f} deg")
    print(f"altitude: {pos.altitude_km:9.2f} km")


if __name__ == "__main__":
    main()