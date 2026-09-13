#from satellite_tracker import __version__
#from satellite_tracker.tle import describe, load_satellite

#def main() -> None:
#    print("satellite-tracker {__version__} (Phase 0 skeleton)")

#if __name__ == "__main__":
#    main()

"""Command-line entry point: run with `python -m satellite_tracker`."""
from satellite_tracker.tle import describe, load_satellite


def main() -> None:
    """Load the satellite and print its orbital elements."""
    print(describe(load_satellite()))


if __name__ == "__main__":
    main()