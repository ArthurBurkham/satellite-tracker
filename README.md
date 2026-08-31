# satellite-tracker

A real-time satellite tracker in Python, built in phases as a learning project in orbital mechanics and aerospace software practice. Ground station: Phoenix, Arizona (configurable). Long-term goal: amateur-radio satellite operation and a physical ground station.

## Status

Phase 0 complete: development environment, package skeleton, smoke test. No orbital mechanics yet.

## Pipeline

    TLE
     ↓
    SGP4
     ↓
    TEME / ECI state vector
     ↓
    Earth rotation
     ↓
    ECEF
     ↓
    Observer-relative position
     ↓
    ENU / topocentric
     ↓
    Azimuth + elevation + range
     ↓
    Pass prediction
     ↓
    Visualization

## Install

    git clone https://github.com/ArthurBurkham/satellite-tracker.git
    cd satellite-tracker
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1      # Windows (macOS/Linux: source .venv/bin/activate)
    pip install -e ".[dev]"

## Run

    python -m satellite_tracker

## Test

    pytest

## Engineering log

The build process, including what broke and why decisions went the way they did, is in [docs/engineering-log.md](docs/engineering-log.md).