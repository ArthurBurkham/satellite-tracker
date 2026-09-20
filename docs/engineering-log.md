# Engineering Log

Running record of the build: what was attempted, what worked, what broke, and why decisions went the way they did. Newest entry at the bottom.

## 2026-08-30 — Phase 0: development environment

**Goal**
Want to build a satellite tracker. Phase 0 goal was a skeleton that installs, runs, and passes one test with zero physics in it. Building each step isolates each phase of learning for me. 

**What I did**
Sequence: build folder > git __init__ > venv > gitignore + pyproject > package skeleton > editable install > smoke test > README/log and then three commits

**Decisions and alternatives**
- Build backend: hatchling — because folder has to be turned into a standard package file (alternative: setuptools)
- Layout: src/ — because this layout puts code one foler deeper so tests can't import your working folder by accident
- Dependencies: none yet — because nothing is needed at this time, will install when we get to those phases. Every library is a commitment, so each gets added when it makes sense
- Map library: Plotly — because I am eventually going to plot the satellite during tracking. Plotly is one library covering the map plus every later chart (alternative: Folium)
- TLE download: Skyfield's loader — because skyfield already downloads and caches TLE files (alternative: requests)

**What broke or surprised me**
Nothing broke, yay! But the hard part is learning all the nuances starting an abitious project like this

**Tests**
The smoke test checks the version __init__ matches the metadata pip wrote at install

**What I learned**
I learned a more complete way to structure the start of my python program. Haven't built something this ambitious before

**Open items**
- Python 3.14: compiled dependencies may lack wheels — verify at the Phase 1 install

## 2026-09-13 — Phase 1: TLE fetch, cache, and parse

**What I did**
Sequence: browser fetch + hand-decoding > skyfield dependency > tle.py > rewired __main__ > pinned test > tie-out

**Decisions**
- Cache before refetch, 3-day default — cache-before-refetch because CelesTrak refits only every couple of hours and blocks clients that poll
- No network in tests, pinned TLE with pinned expected values

**Measurements**
- RAAN 224.6171 -> 223.6594 in 4.6 h, about 5 deg/day
- Python 3.14 wheel verdict: (what the install actually printed — this closes the Phase 0 open item)

**What I learned**
Hand-decoding an epoch once was enough to justify describe()

**Open items**
- Staleness should be measured from the TLE epoch, not the file's download time
- No handling yet for CelesTrak being unreachable

## 2026-09-20 — Phase 2: SGP4 propagation and sub-satellite point

**Goal**
(UTC instant -> TEME state vector -> lat/lon/alt; why TEME doesn't rotate with Earth)

**Decisions**
- Call sgp4 directly rather than only through Skyfield — because the TEME state vector becomes our own visible and testable output
- Frozen dataclasses with frame and units in the field names
- Refuse naive datetimes — because of the ambiguity in the time. The TLE epoch is UTC. So if I show 9:38am in Phoenix time it reads as 9:38 UTC which is incorrect

**What broke or surprised me**
- Excel COS takes radians: cos(51.63) gave 0.2048 instead of 0.6207 ...
- Tie-out was 8 km off; turned out to be the printed timestamp dropping fractional seconds

**Measurements**
- RAAN drift: measured -4.949 deg/day over 6.8 days; J2 formula gives -4.95
- Independent propagation agreed to 10 m in altitude, ~1 s of flight in lat/lon
- Kepler-only latitude estimate -9.93 vs SGP4 -10.15

**Open items**
- Staleness from TLE epoch, not file age
- CelesTrak unreachable: no handling yet
- Print fractional seconds in the position timestamp